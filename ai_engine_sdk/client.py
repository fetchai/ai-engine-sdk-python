import asyncio
import json
import logging
import re
from pprint import pformat
from typing import Optional, List, Union
from uuid import uuid4

import aiohttp
from pydantic import BaseModel

from .api_models.agents_json_messages import (
    ConfirmationMessage,
    TaskOption,
    TaskSelectionMessage,
    is_task_selection_message,
    is_data_request_message,
    DataRequestMessage
)
from .api_models.api_message import (
    is_api_agent_json_message,
    is_api_agent_info_message,
    is_api_agent_message_message,
    is_api_stop_message,
    ApiBaseMessage, AgentMessage, AiEngineMessage, StopMessage
)
from .api_models.api_models import (
    ApiNewSessionRequest,
    is_api_context_json,
    ApiStartMessage, ApiMessagePayload, ApiUserJsonMessage, ApiUserMessageMessage
)
from .api_models.parsing_utils import get_indexed_task_options_from_raw_api_response
from .llm_models import (
    CustomModel,
    DefaultModelId,
    DefaultModelIds,
    get_model_id,
    get_model_name,
    KnownModelId
)

logger = logging.getLogger(__name__)

default_api_base_url = "https://agentverse.ai"


class CreditBalance(BaseModel):
    totalCredits: int
    usedCredits: int
    availableCredits: int


class Model(BaseModel):
    id: str
    name: str
    credits: int


class FunctionGroup(BaseModel):
    uuid: str
    name: str
    isPrivate: bool


class CreateFunctionGroupSchema(BaseModel):
    name: str
    isPrivate: bool


async def make_api_request(
        api_base_url: str,
        api_key: str,
        method: str,
        endpoint: str,
        payload: Optional[dict] = None
) -> dict:
    body = json.dumps(payload) if payload else None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with aiohttp.ClientSession() as session:
        logger.debug(f"\n\n 📤 Request triggered : {method} {api_base_url}{endpoint}")
        logger.debug(f"{body=}")
        logger.debug("---------------------------\n\n")
        async with session.request(method, f"{api_base_url}{endpoint}", headers=headers, data=body) as response:
            if not bool(re.search(pattern="^2..$", string=str(response.status))):
                raise Exception(f"Request failed with status {response.status} to {endpoint}")
            return await response.json()


class Session:
    def __init__(self, api_base_url: str, api_key: str, session_id: str, function_group: str):
        self._api_base_url = api_base_url
        self._api_key = api_key
        self.session_id = session_id
        self.function_group = function_group
        self._messages: List[ApiBaseMessage] = []
        self._message_ids: set[str] = set()

    async def _submit_message(self, payload: ApiMessagePayload):
        await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='POST',
            endpoint=f"/v1beta1/engine/chat/sessions/{self.session_id}/submit",
            payload={'payload': payload.dict()}
        )

    async def start(self, objective: str, context: Optional[str] = None):
        await self._submit_message(
            payload=ApiStartMessage.parse_obj({
                'session_id': self.session_id,
                'bucket_id': self.function_group,
                'message_id': str(uuid4()).lower(),
                'objective': objective,
                'context': context or ''
            })
        )

    async def submit_task_selection(self, selection: TaskSelectionMessage, options: list[TaskOption]):
        await self._submit_message(
            payload=ApiUserJsonMessage.parse_obj({
                'session_id': self.session_id,
                'message_id': str(uuid4()).lower(),
                'referral_id': selection.id,
                'user_json': {
                    'type': selection.type.lower(),
                    'selection': [o.key for o in options],
                }
            })
        )

    async def submit_response(self, query: AgentMessage, response: str):
        await self._submit_message(
            payload=ApiUserMessageMessage.parse_obj(
                {
                    'session_id': self.session_id,
                    'message_id': str(uuid4()).lower(),
                    'referral_id': query.id,
                    'user_message': response
                }
            )
        )

    async def submit_confirmation(self, confirmation: ConfirmationMessage):
        await self._submit_message(
            payload=ApiUserMessageMessage.parse_obj({
                'session_id': self.session_id,
                'message_id': str(uuid4()).lower(),
                'referral_id': confirmation.id,
                'user_message': 'confirm'
            })
        )

    async def reject_confirmation(self, confirmation: ConfirmationMessage, reason: str):
        await self._submit_message(
            payload=ApiUserMessageMessage.parse_obj({
                'session_id': self.session_id,
                'message_id': str(uuid4()).lower(),
                'referral_id': confirmation.id,
                'user_message': reason
            })
        )

    async def get_messages(self) -> List[ApiBaseMessage]:
        queryParams = f"?last_message_id={self._messages[-1]['message_id']}" if self._messages else ""
        response = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint=f"/v1beta1/engine/chat/sessions/{self.session_id}/new-messages{queryParams}"
        )

        newMessages: List[ApiBaseMessage] = []
        for item in response['agent_response']:
            message: dict = json.loads(item)
            if message['message_id'] in self._message_ids:
                continue
            logger.debug(f"\n 📥 Message received: {pformat(message)} \n")
            logger.debug(f"----------------- \n")
            if is_api_agent_json_message(message):
                agent_json: dict = message['agent_json']
                agent_json_type: str = agent_json['type'].upper()
                if is_task_selection_message(message_type=agent_json_type):
                    indexed_task_options: dict = get_indexed_task_options_from_raw_api_response(raw_api_response=message)
                    newMessages.append(
                        TaskSelectionMessage.parse_obj({
                            'type': agent_json_type,
                            'id': message['message_id'],
                            'timestamp': message['timestamp'],
                            'text': agent_json['text'],
                            'options':indexed_task_options
                        })
                    )
                elif is_api_context_json(message_type=agent_json_type, agent_json_text=agent_json['text']):
                    newMessages.append(
                        ConfirmationMessage.parse_obj({
                            'id': message['message_id'],
                            'timestamp': message['timestamp'],
                            'text': agent_json['text'],
                            'model': agent_json['context_json']['digest'],
                            'payload': agent_json['context_json']['args'],
                        })
                    )
                elif is_data_request_message(message_type=agent_json_type):
                    newMessages.append(
                        DataRequestMessage.parse_obj({
                            "id": message['message_id'],
                            "text": agent_json['text'],
                            "type": agent_json_type,
                            "options": agent_json['options'],
                            "timestamp": message['timestamp']
                        })
                    )
                else:
                    print(f"UNKNOWN-JSON: {message}")
            elif is_api_agent_info_message(message):
                newMessages.append(
                    AiEngineMessage.parse_obj({
                        'id': message['message_id'],
                        'type': 'ai-engine',
                        'timestamp': message['timestamp'],
                        'text': message['agent_info'],
                    })
                )
            elif is_api_agent_message_message(message):
                newMessages.append(
                    AgentMessage.parse_obj({
                        'id': message['message_id'],
                        'type': 'agent',
                        'timestamp': message['timestamp'],
                        'text': message['agent_message'],
                    })
                )
            elif is_api_stop_message(message):
                print(f"STOP: {message}")
                newMessages.append(
                    StopMessage.parse_obj({
                        'id': message['message_id'],
                        'timestamp': message['timestamp'],
                        'type': 'stop',
                    })
                )
            else:
                print(f"UNKNOWN: {message}")

            if message['message_id'] not in self._message_ids:
                self._messages.append(message)
                self._message_ids.add(message['message_id'])

        return newMessages

    async def delete(self):
        await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='DELETE',
            endpoint=f"/v1beta1/engine/chat/sessions/{self.session_id}"
        )


class AiEngine:
    def __init__(self, api_key: str, options: Optional[dict] = None):
        self._api_base_url = options.get('apiBaseUrl') if options and 'apiBaseUrl' in options else default_api_base_url
        self._api_key = api_key

    ####
    # Function groups
    ####

    async def get_function_groups(self) -> List[FunctionGroup]:
        logger.debug("get_function_groups")
        publicGroups, privateGroups = await asyncio.gather(
            self.get_public_function_groups(),
            self.get_private_function_groups()
        )
        return privateGroups + publicGroups

    async def get_public_function_groups(self) -> List[FunctionGroup]:
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint="/v1beta1/function-groups/public/"
        )
        return list(
            map(
                lambda item: FunctionGroup.parse_obj(item),
                raw_response
            )
        )

    async def get_private_function_groups(self) -> List[FunctionGroup]:
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint="/v1beta1/function-groups/"
        )
        return list(
            map(
                lambda item: FunctionGroup.parse_obj(item),
                raw_response
            )
        )

    async def create_function_group(
            self,
            is_private: bool,
            name: str
    ) -> FunctionGroup:
        payload = {
            "isPrivate": is_private,
            "name": name
        }
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='POST',
            endpoint="/v1beta1/function-groups/",
            payload=payload
        )
        return FunctionGroup(**raw_response)

    ####
    # Model
    ####
    async def get_models(self) -> List[Model]:
        pending_credits = [self.get_model_credits(model_id) for model_id in DefaultModelIds]

        models = [Model(
            id=model_id,
            name=get_model_name(model_id),
            credits=0
        ) for model_id in DefaultModelIds]

        credits = await asyncio.gather(*pending_credits)

        if len(credits) != len(models):
            raise Exception("Credit count mismatch")

        for i, credit in enumerate(credits):
            models[i].credits = credit

        return models

    ####
    # Credit
    ####
    async def get_credits(self) -> CreditBalance:
        response = await make_api_request(self._api_base_url, self._api_key, 'GET', "/v1beta1/engine/credit/info")
        return CreditBalance(
            totalCredits=response['total_credit'],
            usedCredits=response['used_credit'],
            availableCredits=response['available_credit']
        )

    async def get_model_credits(self, model: Union[KnownModelId, CustomModel]) -> int:
        model_id = get_model_id(model)
        response = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint=f"/v1beta1/engine/credit/remaining_tokens?models={model_id}"
        )
        return response['model_tokens'].get(model_id, 0)

    ####
    # Session
    ####
    async def create_session(self, function_group: str, opts: Optional[dict] = None) -> Session:
        request_payload = ApiNewSessionRequest(
            email=opts.get('email') if opts else "",
            functionGroup=function_group,
            preferencesEnabled=False,
            requestModel=opts.get('model') if opts and 'model' in opts else DefaultModelId
        )
        response = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='POST',
            endpoint="/v1beta1/engine/chat/sessions",
            payload=request_payload.dict()
        )

        return Session(self._api_base_url, self._api_key, response['session_id'], function_group)

    ####
    # Permissions
    ####
    async def share_function_group(
        self,
        function_group_id: str,
        target_user_id: str | None = None,
        target_user_email: str | None = None,
    ) -> dict:

        # TODO: uncomment and take care of every case
        if not any([target_user_id, target_user_email]):
            raise Exception("You must provide user_id OR email")

        payload = {
            # "user_id_to_add_permission": "",
            "user_email_to_add_permission": target_user_email,
            "action": "RETRIEVE"
        }
        # function_group_id = ...
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='PUT',
            endpoint=f"/v1beta1/function-groups/{function_group_id}/permissions/",
            payload=payload
        )
        return raw_response
