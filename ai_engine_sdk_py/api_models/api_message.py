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


class AgentJsonMessage(ApiBaseMessage):
    ...


class AiEngineMessage(ApiBaseMessage):
    type: str = "ai-engine"
    text: str


class AgentMessage(ApiBaseMessage):
    # TODO: I've not seen that type. What it is meant for?
    type: str = "agent"
    text: str


class StopMessage(ApiBaseMessage):
    type: str = "stop"


# ---- RAW DATA CHECKERS ----
# TODO: move/reafctor checkers to proper context. Is not the same identify a api_message (top level)
#  than agent_json ones (even if the diff is only the path of the elements)
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


def is_agent_message(m: ApiBaseMessage) -> bool:
    return m.type == "agent"


def is_stop_message(m: ApiBaseMessage) -> bool:
    return m.type == ApiMessageType.AGENT_STOP


def is_api_confirmation_message(m: ApiBaseMessage) -> bool:
    # TODO: this should use agent_json_messages checkers but cannot be imported (circular imports),
    #  so it requires a dedicated file.
    """
    {
    'session_id': 'bfcdb62b-4e73-42be-9117-f90030d0a1a1',
     'message_id': 'f5ee18aa-7744-4965-8a10-e6c59a0deaf6',
     'timestamp': '2024-06-10T17:47:17.301769',
     'score': 0.0,
     'referral_id': None,
     'type': 'agent_json',
     'agent_json': {
        'type': 'context_json',
        'text': 'Please confirm the following details',
        'options': None,
        'context_json': {
            'digest': 'model:461bc84518c881327cb3a99d37d660d3a9bf4a302898447e57002fcea4e72535',
            'args': {
                'from': 'BCN', 'to': 'WAW', 'trip': 'oneway', 'date': '11.08.2024', 'persons': 1
            }
        },
        'functions': None
        }
    }
    """
    if m.type == ApiMessageType.AGENT_INFO:
        m: AgentJsonMessage = m
        ...

