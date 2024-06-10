from enum import StrEnum
from typing import List, Union, Dict, Any, Optional, Literal
from pydantic import BaseModel


class ApiNewSessionRequest(BaseModel):
    email: str
    functionGroup: Optional[str] = None
    preferencesEnabled: bool
    requestModel: str


class ApiNewSessionResponse(BaseModel):
    session_id: str
    user: str
    num_messages: int
    last_message_timestamp: Optional[str] = None
    messages: List[Any]  # Depends on actual structure of messages
    function_group: str
    model: str
    remaining_tokens: int
    status: Optional[str] = None
    preferences_enabled: bool


class ApiSelectedTasks(BaseModel):
    type: str = "task_list"
    selection: List[int]


class ApiMessagePayload(BaseModel):
    session_id: str


class ApiMessagePayloadTypes(StrEnum):
    START = "start"
    USER_JSON = "user_json"
    USER_MESSAGE = "user_message"


class ApiStartMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.START] = ApiMessagePayloadTypes.START

    objective: str
    message_id: str
    context: str
    bucket_id: str


class ApiUserJsonMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.USER_JSON] = ApiMessagePayloadTypes.USER_JSON

    message_id: str
    referral_id: str
    user_json: ApiSelectedTasks


class ApiUserMessageMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.USER_MESSAGE] = ApiMessagePayloadTypes.USER_MESSAGE

    message_id: str
    referral_id: str
    user_message: str


class ApiMessageTypes(StrEnum):
    TAKS_LIST = "task_list"
    CONTEXT_JSON = "context_json"


class ApiSubmitMessage(BaseModel):
    payload: ApiMessagePayload


class ApiNewMessages(BaseModel):
    agent_response: List[str]


# TODO : missing fields and
# TODO: Change base class
#  id, type, timestamp
class ApiAgentJson(BaseModel):
    type: str


class ApiOption(BaseModel):
    key: int
    value: str


class ApiTaskList(ApiAgentJson):
    type: Literal[ApiMessageTypes.TAKS_LIST] = ApiMessageTypes.TAKS_LIST
    text: str
    options: List[ApiOption]
    context_json: Optional[Any] = None


class ApiContextJson(BaseModel):
    type: Literal[ApiMessageTypes.CONTEXT_JSON] = ApiMessageTypes.CONTEXT_JSON
    text: str
    options: Optional[None] = None
    context_json: Dict[str, Any]


def is_api_task_list(d: dict) -> bool:
    return d["type"] == "task_list"


def is_api_context_json(d: dict) -> bool:
    return d["type"] == "context_json"



