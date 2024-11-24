from typing import Annotated, List, Dict
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langgraph.prebuilt.chat_agent_executor import AgentState


class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    bounding_box_hash: Dict

