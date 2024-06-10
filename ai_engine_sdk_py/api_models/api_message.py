from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class ApiMessageType(StrEnum):
    AGENT_JSON = "agent_json"
    AGENT_MESSAGE = "agent_message"
    AGENT_STOP = "stop"
    AGENT_INFO = "agent_info"


class ApiBaseMessage(BaseModel):
    session_id: Optional[str] = None
    id: str  # uuid
    type: str  # enum
    timestamp: str  # date


def is_api_agent_json_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_JSON


def is_api_agent_info_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_INFO


def is_api_agent_message_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_MESSAGE


def is_api_stop_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_STOP
