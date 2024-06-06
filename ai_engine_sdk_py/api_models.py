from typing import List, Union, Dict, Any, Optional
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


class ApiAgentJsonMessage(BaseModel):
    session_id: Optional[str] = None
    message_id: str
    timestamp: str
    score: int
    referral_id: Optional[str] = None
    type: str = "agent_json"
    agent_json: Union[ApiAgentJson, ApiContextJson]


class ApiAgentInfoMessage(BaseModel):
    session_id: Optional[str] = None
    message_id: str
    timestamp: str
    score: int
    referral_id: Optional[str] = None
    type: str = "agent_info"
    agent_info: str


class ApiAgentMessageMessage(BaseModel):
    session_id: Optional[str] = None
    message_id: str
    timestamp: str
    score: int
    referral_id: Optional[str] = None
    type: str = "agent_message"
    agent_message: str


class ApiStopMessage(BaseModel):
    type: str = "stop"
    session_id: str
    message_id: str
    timestamp: str
    score: int
    referral_id: str


ApiMessage = Union[
    ApiAgentJsonMessage,
    ApiStopMessage,
    ApiAgentInfoMessage,
    ApiAgentMessageMessage
]


def is_api_task_list(obj: ApiAgentJson) -> bool:
    return obj.type == "task_list"


def is_api_context_json(obj: ApiAgentJson) -> bool:
    return obj.type == "context_json"


def is_api_agent_json_message(m: ApiMessage) -> bool:
    return m.type == "agent_json"


def is_api_agent_info_message(m: ApiMessage) -> bool:
    return m.type == "agent_info"


def is_api_agent_message_message(m: ApiMessage) -> bool:
    return m.type == "agent_message"


def is_api_stop_message(m: ApiMessage) -> bool:
    return m.type == "stop"
