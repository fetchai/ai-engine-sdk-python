from pydantic import BaseModel, Field
from typing import List, Union, Any, Optional, Dict


class ApiNewSessionRequest(BaseModel):
    email: str
    function_group: str = Field(alias='functionGroup')
    preferences_enabled: bool = Field(alias='preferencesEnabled')
    request_model: str = Field(alias='requestModel')


class ApiNewSessionResponse(BaseModel):
    session_id: str = Field(alias='session_id')
    user: str
    num_messages: int = Field(alias='num_messages')
    last_message_timestamp: Optional[str] = Field(alias='last_message_timestamp')
    messages: List[Any]
    bucket_id: Optional[str] = Field(alias='bucket_id')
    model: str
    remaining_tokens: int = Field(alias='remaining_tokens')
    status: Optional[str]
    preferences_enabled: bool = Field(alias='preferences_enabled')


class ApiStartMessage(BaseModel):
    type: str  # should be "start"
    session_id: str = Field(alias='session_id')
    objective: str
    message_id: str = Field(alias='message_id')
    context: str
    bucket_id: str = Field(alias='bucket_id')


class ApiSelectedTasks(BaseModel):
    type: str  # should be "task_list"
    selection: List[int]


class ApiUserJsonMessage(BaseModel):
    type: str  # should be "user_json"
    session_id: str = Field(alias='session_id')
    message_id: str = Field(alias='message_id')
    referral_id: str = Field(alias='referral_id')
    user_json: ApiSelectedTasks = Field(alias='user_json')


class ApiUserMessageMessage(BaseModel):
    type: str  # should be "user_message"
    session_id: str = Field(alias='session_id')
    message_id: str = Field(alias='message_id')
    referral_id: str = Field(alias='referral_id')
    user_message: str = Field(alias='user_message')


ApiMessagePayload = Union[ApiStartMessage, ApiUserJsonMessage, ApiUserMessageMessage]


class ApiSubmitMessage(BaseModel):
    payload: ApiMessagePayload


class ApiNewMessages(BaseModel):
    agent_response: List[str] = Field(alias='agent_response')


class ApiAgentJson(BaseModel):
    type: str

    class Config:
        allow_mutation = False


class ApiOption(BaseModel):
    key: int
    value: str


class ApiTaskList(ApiAgentJson):
    type: str = Field(init=False, default="task_list")  # TODO: Make it immutable
    text: str
    options: List[ApiOption]
    context_json: Optional[Any] = Field(alias='context_json')


class ApiContextJson(ApiAgentJson):
    type: str  # should be "context_json"
    text: str
    options: None
    context_json: Dict[str, Any] = Field(alias='context_json')


def is_api_task_list(obj: ApiAgentJson) -> bool:
    return obj.type == "task_list"


def is_api_context_json(obj: ApiAgentJson) -> bool:
    return obj.type == "context_json"


class ApiAgentJsonMessage(BaseModel):
    session_id: Optional[str] = Field(alias='session_id')
    message_id: str = Field(alias='message_id')
    timestamp: str
    score: int
    referral_id: Optional[str] = Field(alias='referral_id')
    type: str  # should be "agent_json"
    agent_json: Union[ApiAgentJson, ApiContextJson] = Field(alias='agent_json')


class ApiAgentInfoMessage(BaseModel):
    session_id: Optional[str] = Field(alias='session_id')
    message_id: str = Field(alias='message_id')
    timestamp: str
    score: int
    referral_id: Optional[str] = Field(alias='referral_id')
    type: str  # should be "agent_info"
    agent_info: str = Field(alias='agent_info')


class ApiAgentMessageMessage(BaseModel):
    session_id: Optional[str] = Field(alias='session_id')
    message_id: str = Field(alias='message_id')
    timestamp: str
    score: int
    referral_id: Optional[str] = Field(alias='referral_id')
    type: str  # should be "agent_message"
    agent_message: str = Field(alias='agent_message')


ApiMessage = Union[ApiAgentJsonMessage, ApiAgentInfoMessage, ApiAgentMessageMessage]


def is_api_agent_json_message(m: ApiMessage) -> bool:
    return isinstance(m, ApiAgentJsonMessage) and m.type == "agent_json"


def is_api_agent_info_message(m: ApiMessage) -> bool:
    return isinstance(m, ApiAgentInfoMessage) and m.type == "agent_info"


def is_api_agent_message_message(m: ApiMessage) -> bool:
    return isinstance(m, ApiAgentMessageMessage) and m.type == "agent_message"
