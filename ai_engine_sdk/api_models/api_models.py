from enum import Enum
from typing import List, Union, Dict, Any, Optional, Literal
from pydantic import BaseModel


# Outgoing messages
class ApiMessagePayloadTypes(str, Enum):
    START = "start"
    USER_JSON = "user_json"
    USER_MESSAGE = "user_message"
    EXECUTE_FUNCTIONS = "execute_functions"

class ApiMessagePayload(BaseModel):
    session_id: str


class ApiSubmitMessage(BaseModel):
    payload: ApiMessagePayload


class ApiSelectedTasks(BaseModel):
    type: str = "task_list"
    selection: List[Union[int,str]]


class ApiNewSessionRequest(BaseModel):
    email: str
    functionGroup: Optional[str] = None
    preferencesEnabled: bool
    requestedModel: str


class ApiUserJsonMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.USER_JSON] = ApiMessagePayloadTypes.USER_JSON

    message_id: str
    referral_id: str
    user_json: ApiSelectedTasks


class ApiStartMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.START] = ApiMessagePayloadTypes.START

    objective: str
    message_id: str
    context: str
    bucket_id: str


class ApiUserMessageMessage(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.USER_MESSAGE] = ApiMessagePayloadTypes.USER_MESSAGE

    message_id: str
    referral_id: str
    user_message: str


class ApiUserMessageExecuteFunctions(ApiMessagePayload):
    type: Literal[ApiMessagePayloadTypes.EXECUTE_FUNCTIONS] = ApiMessagePayloadTypes.EXECUTE_FUNCTIONS

    functions: list[str]
    objective: str
    context: str



# -----------

# class ApiNewSessionResponse(BaseModel):
#     session_id: str
#     user: str
#     num_messages: int
#     last_message_timestamp: Optional[str] = None
#     messages: List[Any]  # Depends on actual structure of messages
#     function_group: str
#     model: str
#     remaining_tokens: int
#     status: Optional[str] = None
#     preferences_enabled: bool
#

# class ApiMessageTypes(StrEnum):
#     TAKS_LIST = "task_list"
#     CONTEXT_JSON = "context_json"


# class ApiNewMessages(BaseModel):
#     agent_response: List[str]
#

# class ApiAgentJson(BaseModel):
#     type: str
#

# class ApiOption(BaseModel):
#     key: int
#     value: str


# class ApiTaskList(ApiAgentJson):
#     type: Literal[ApiMessageTypes.TAKS_LIST] = ApiMessageTypes.TAKS_LIST
#     text: str
#     options: List[ApiOption]
#     context_json: Optional[Any] = None


# class ApiContextJson(BaseModel):
#     type: Literal[ApiMessageTypes.CONTEXT_JSON] = ApiMessageTypes.CONTEXT_JSON
#     text: str
#     options: Optional[None] = None
#     context_json: Dict[str, Any]


# ---- DATA CHECKERS ----
def is_api_task_list(message_type: str) -> bool:
    return message_type == "task_list"


def is_api_context_json(message_type: str, agent_json_text: str) -> bool:
    return message_type == "context_json" or "Please confirm" in agent_json_text
# ---------
