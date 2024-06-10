from enum import Enum, StrEnum
from typing import Optional, Union, Literal, Type

from pydantic import BaseModel, Field
from pydantic_core.core_schema import JsonType

from api_models.api_models import ApiAgentJson, ApiContextJson


class ApiMessageType(StrEnum):
    AGENT_JSON = "agent_json"
    AGENT_MESSAGE = "agent_message"
    AGENT_STOP = "stop"
    AGENT_INFO = "agent_info"


class ApiMessage(BaseModel):
    session_id: Optional[str] = None
    id: str  # uuid
    type: str  # enum
    timestamp: str  # date


class ApiAgentInfoMessage(ApiMessage):
    type: Literal["agent_info"] = Field(init=False, default="agent_info")

    message_id: str
    score: int
    referral_id: Optional[str] = None
    agent_info: str


class ApiAgentMessageMessage(ApiMessage):
    type: str = "agent_message"

    message_id: str
    score: int
    referral_id: Optional[str] = None
    agent_message: str


class ApiAgentMessageMessage(ApiMessage):
    type: str = "agent_message"

    message_id: str
    score: int
    referral_id: Optional[str] = None
    agent_message: str


class ApiStopMessage(ApiMessage):
    type: str = ApiMessageType.AGENT_STOP

    message_id: str
    score: int
    referral_id: str


class ApiAgentJsonMessage(ApiMessage):
    type: Literal[ApiMessageType.AGENT_JSON] = ApiMessageType.AGENT_JSON

    message_id: str
    score: int
    referral_id: Optional[str] = None
    agent_json: Union[ApiAgentJson, ApiContextJson]


# ApiMessageTypes = Union[
#     ApiAgentJsonMessage,
#     ApiStopMessage,
#     ApiAgentInfoMessage,
#     ApiAgentMessageMessage
# ]
#

_type_map: dict[str, type[ApiMessage]] = {
    ApiMessageType.AGENT_JSON: ApiAgentJsonMessage,
    ApiMessageType.AGENT_MESSAGE: ApiAgentMessageMessage,
    ApiMessageType.AGENT_INFO: ApiAgentInfoMessage,
    ApiMessageType.AGENT_STOP: ApiStopMessage,
}


def api_message_factory(data: dict, message_type: str) -> ApiMessage:
    return _type_map[message_type].parse_obj(data)


def is_api_agent_json_message(m: dict) -> bool:
    return m["type"] == "agent_json"


def is_api_agent_info_message(m: dict) -> bool:
    return m["type"] == "agent_info"


def is_api_agent_message_message(m: dict) -> bool:
    return m["type"] == "agent_message"


def is_api_stop_message(m: dict) -> bool:
    return m["type"] == "stop"
