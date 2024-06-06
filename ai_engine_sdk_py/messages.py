from typing import List, Union, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class BaseMessage(BaseModel):
    id: str
    type: str
    timestamp: datetime


class TaskOption(BaseModel):
    key: int
    title: str


class TaskSelectionMessage(BaseMessage):
    type: str = "task_selection"
    text: str
    options: List[TaskOption]


class AiEngineMessage(BaseMessage):
    type: str = "ai-engine"
    text: str


class AgentMessage(BaseMessage):
    type: str = "agent"
    text: str


class ConfirmationMessage(BaseMessage):
    type: str = "confirmation"
    text: str
    model: str
    payload: Dict[str, Any]


class StopMessage(BaseMessage):
    type: str = "stop"


Message = Union[
    TaskSelectionMessage,
    AiEngineMessage,
    AgentMessage,
    ConfirmationMessage,
    StopMessage
]


def is_task_selection_message(m: Message) -> bool:
    return m.type == "task_selection"


def is_ai_engine_message(m: Message) -> bool:
    return m.type == "ai-engine"


def is_agent_message(m: Message) -> bool:
    return m.type == "agent"


def is_confirmation_message(m: Message) -> bool:
    return m.type == "confirmation"


def is_stop_message(m: Message) -> bool:
    return m.type == "stop"
