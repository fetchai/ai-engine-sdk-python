from enum import StrEnum
from typing import List, Union, Dict, Any, Literal, get_args

from pydantic import BaseModel

from api_models.api_message import AiEngineMessage, AgentMessage, StopMessage, AgentJsonMessage


class TaskOption(BaseModel):
    key: int
    title: str


# TODO: This is wrong, they should not inherit from AgentJsonMessage, they should be
#  included in the AgentJsonMessage schema; so we do not know how complex it can become and
#  the current approach is stiff and does not ease change or add.
#  In addition we should differentiate between incoming data parsers (deserializers),
#  outgoing (serializers) and internal entities.


class AgentJsonMessageTypes(StrEnum):
    TASK_SELECTION = "TASK_SELECTION"
    CONFIRMATION = "CONFIRMATION"
    DATE = "DATE"


DataRequestTypes = Union[
    Literal[AgentJsonMessageTypes.DATE]
]


class TaskSelectionMessage(AgentJsonMessage):
    type: Literal[AgentJsonMessageTypes.TASK_SELECTION] = AgentJsonMessageTypes.TASK_SELECTION
    text: str
    options: List[TaskOption]


class DataRequestMessage(AgentJsonMessage):
    type: DataRequestTypes = AgentJsonMessageTypes.DATE
    text: str


class ConfirmationMessage(AgentJsonMessage):
    type: Literal[AgentJsonMessageTypes.CONFIRMATION] = AgentJsonMessageTypes.CONFIRMATION
    text: str
    model: str
    payload: Dict[str, Any]


# TODO: change this for
Message = Union[
    TaskSelectionMessage,
    AiEngineMessage,
    AgentMessage,
    ConfirmationMessage,
    StopMessage
]


def is_confirmation_message(m: AgentJsonMessage) -> bool:
    return m.type == AgentJsonMessageTypes.CONFIRMATION


def is_task_selection_message(m: AgentJsonMessage) -> bool:
    return m.type == AgentJsonMessageTypes.TASK_SELECTION


def is_data_request_message(m: AgentJsonMessage) -> bool:
    allowed_values = [literal for lit in get_args(DataRequestTypes) for literal in get_args(lit)]
    return m.type in allowed_values
