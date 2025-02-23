from typing import Annotated, List, Dict
from typing_extensions import TypedDict
import operator

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


def custom_list_add_operator(left: List[str], right: List[str]):

    if right[0] == "clear":
        return []

    return left + right


class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    execution_list: Annotated[List[str], custom_list_add_operator]
    bounding_box_hash: Dict
    execution_action: str
    complete_action: str
    previous_state_screenshot: str
    initial_screenshot: str
