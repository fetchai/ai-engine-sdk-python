from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ApiMessageType(str, Enum):
    AGENT_JSON = "agent_json"
    AGENT_MESSAGE = "agent_message"
    AGENT_STOP = "stop"
    AGENT_INFO = "agent_info"


class ApiBaseMessage(BaseModel):
    session_id: Optional[str] = None
    id: str  # uuid
    type: str  # enum
    timestamp: str  # date


class AgentJsonMessage(ApiBaseMessage):
    ...


class AiEngineMessage(ApiBaseMessage):
    type: str = "ai-engine"
    text: str


class AgentMessage(ApiBaseMessage):
    type: str = "agent"
    text: str


class StopMessage(ApiBaseMessage):
    type: str = "stop"


# ---- RAW DATA CHECKERS ----
def is_api_agent_json_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_JSON


def is_api_agent_info_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_INFO


def is_api_agent_message_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_MESSAGE


def is_api_stop_message(m: dict) -> bool:
    return m["type"] == ApiMessageType.AGENT_STOP


def is_ai_engine_message(m: ApiBaseMessage) -> bool:
    return m.type == "ai-engine"


def is_stop_message(m: ApiBaseMessage) -> bool:
    return m.type == ApiMessageType.AGENT_STOP
