from enum import Enum, StrEnum
from typing import Optional, Union, Literal, Type

from pydantic import BaseModel, Field
from pydantic_core.core_schema import JsonType

from api_models.api_models import ApiAgentJson, ApiContextJson


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


class ApiStopMessage(ApiMessage):
    type: str = "stop"

    message_id: str
    score: int
    referral_id: str


class ApiAgentJsonMessage(ApiMessage):
    type: str = "agent_json"

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

class ApiMessageType(StrEnum):
    agent_json = "agent_json"
    agent_message = "agent_message"
    agent_stop = "stop"
    agent_info = "agent_info"


_type_map: dict[str, type[ApiMessage]] = {
    ApiMessageType.agent_json: ApiAgentJsonMessage,
    ApiMessageType.agent_message: ApiAgentMessageMessage,
    ApiMessageType.agent_info: ApiAgentInfoMessage,
    ApiMessageType.agent_stop: ApiStopMessage,
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
