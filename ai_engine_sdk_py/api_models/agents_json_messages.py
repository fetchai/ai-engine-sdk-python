import logging
from enum import StrEnum
from typing import Union, Dict, Any, Literal, get_args, get_origin

from pydantic import BaseModel

from .api_message import AiEngineMessage, AgentMessage, StopMessage, AgentJsonMessage

logger = logging.getLogger(__name__)


class TaskOption(BaseModel):
    # model_config = ConfigDict(coerce_numbers_to_str=True)
    # TODO: should be more picky (int, uuid and union of literals).
    key: str
    title: str


# TODO: This is wrong, they should not inherit from AgentJsonMessage, they should be
#  included in the AgentJsonMessage schema; so we do not know how complex it can become and
#  the current approach is stiff and does not ease change or add.
#  In addition we should differentiate between incoming data parsers (deserializers),
#  outgoing (serializers) and internal entities.


class AgentJsonMessageTypes(StrEnum):
    TASK_LIST = "TASK_LIST"
    OPTIONS = "OPTIONS"
    CONFIRMATION = "CONFIRMATION"
    DATE = "DATE"


DataRequestTypes = Union[
    Literal[AgentJsonMessageTypes.DATE],
]

TaskSelectionTypes = Union[
    Literal[AgentJsonMessageTypes.TASK_LIST],
    Literal[AgentJsonMessageTypes.OPTIONS],
]


class TaskSelectionMessage(AgentJsonMessage):
    type: TaskSelectionTypes
    text: str
    options: Dict[str, TaskOption]


    def get_options_keys(self) -> list[TaskOption]:
        return [option for option in self.options]


class DataRequestMessage(AgentJsonMessage):
    type: DataRequestTypes
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


def is_agent_json_confirmation_message(message_type: str) -> bool:
    # is_confirmation_type: bool = message_type == AgentJsonMessageTypes.CONFIRMATION
    return message_type == AgentJsonMessageTypes.CONFIRMATION


def is_task_selection_message(message_type: str) -> bool:
    union_of_type = TaskSelectionTypes
    allowed_values = [literal for lit in get_args(union_of_type) for literal in get_args(lit)]
    logger.debug(f"Allowed values: {allowed_values}")
    logger.debug(f"Message type : {message_type}")
    return message_type.upper() in allowed_values


def is_data_request_message(message_type: str) -> bool:
    union_of_type = DataRequestTypes
    if get_origin(union_of_type) is Union:
        allowed_values = [literal for lit in get_args(union_of_type) for literal in get_args(lit)]
    elif get_origin(union_of_type) is Literal:
        allowed_values = get_args(union_of_type)

    return message_type.upper() in allowed_values
