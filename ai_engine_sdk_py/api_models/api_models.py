from typing import List, Union, Dict, Any, Optional
from pydantic import BaseModel


# TODO: This is, apparently, response models..
# TODO: Ideally, create entities (data class) and models (representation, serializers).
#  Nontheless, innecessary right now
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


class ApiStartMessage(BaseModel):
    type: str = "start"
    session_id: str
    objective: str
    message_id: str
    context: str
    bucket_id: str


class ApiSelectedTasks(BaseModel):
    type: str = "task_list"
    selection: List[int]


class ApiUserJsonMessage(BaseModel):
    type: str = "user_json"
    session_id: str
    message_id: str
    referral_id: str
    user_json: ApiSelectedTasks


class ApiUserMessageMessage(BaseModel):
    type: str = "user_message"
    session_id: str
    message_id: str
    referral_id: str
    user_message: str


ApiMessagePayload = Union[
    ApiStartMessage,
    ApiUserJsonMessage,
    ApiUserMessageMessage
]


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
    type: str = "task_list"
    text: str
    options: List[ApiOption]
    context_json: Optional[Any] = None


class ApiContextJson(BaseModel):
    type: str = "context_json"
    text: str
    options: Optional[None] = None
    context_json: Dict[str, Any]


def is_api_task_list(d: dict) -> bool:
    return d["type"] == "task_list"


def is_api_context_json(d: dict) -> bool:
    return d["type"] == "context_json"



