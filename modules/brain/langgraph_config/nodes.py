from typing import Literal

from langchain_core.messages import HumanMessage

from modules.brain.langgraph_config.state import State
from modules.brain.langgraph_config.llm import (
    get_decide_next_step_llm,
    get_decide_executable_llm,
)

####################################################### NODES #################################################################################


def decide_next_step_node(state: State):
    llm = get_decide_next_step_llm()

    message = llm.invoke(state["messages"])
    return {"messages": [message]}


def decide_executable_nodes(state: State):

    action = state["messages"][-1].content
    llm, return_list = get_decide_executable_llm(action=action)

    message = llm.invoke(
        {
            "history": [],
        }
    )
    return {"messages": [message], "bounding_box_hash": return_list}


####################################################### EDGES #################################################################################
def execution_or_repeat(state) -> Literal["executing_tools", "__end__"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "executing_tools"
    ### TODO: delete last message of tool call and say 'unable to perform x action'
    return "__end__"
