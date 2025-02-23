from typing import Literal
import json
import re

from langchain_core.messages import HumanMessage, RemoveMessage

from tools.get_screenshot import get_screenshot
from modules.brain.langgraph_config.state import State
from modules.brain.langgraph_config.llm import (
    get_decide_next_step_llm,
    get_decide_executable_llm,
    get_execution_status_llm,
    get_task_status_llm,
)

####################################################### NODES #################################################################################

def decide_next_step_node(state: State):
    llm = get_decide_next_step_llm()

    message = llm.invoke(state["messages"])

    initial_screenshot = get_screenshot(output_type="saved_path")

    data = {
        "messages": [message],
    }

    if state.get("complete_action", None) is None:
        data["complete_action"] = state["messages"][-1].content
    if state.get("initial_screenshot", None) is None:
        data["initial_screenshot"] = initial_screenshot

    return data


def decide_executable_node(state: State):

    action = state["messages"][-1].content
    execution_list = state["execution_list"]

    llm, return_list, file_path = get_decide_executable_llm(
        action=action, performed_executions=execution_list
    )

    message = llm.invoke(
        {
            "history": [],
        }
    )

    return {
        "messages": [message],
        "bounding_box_hash": return_list,
        "execution_action": action,
        "previous_state_screenshot": file_path,
    }


def check_execution_status_node(state: State):

    execution_action = state["execution_action"]
    tool_output = state["messages"][-1].content
    previous_state_screenshot = state["previous_state_screenshot"]

    llm = get_execution_status_llm(
        execution_action=execution_action,
        previous_state_screenshot=previous_state_screenshot,
    )

    message = llm.invoke({"history": []})

    return {"messages": [message], "execution_list": [tool_output]}


def clean_messages_node(state: State):
    """Deleting last three messages which are AI tool call request, tool call, AI status check message"""

    messages = state["messages"]
    return {"messages": [RemoveMessage(id=m.id) for m in messages[-3:]]}


def check_task_status_node(state: State):

    complete_action = state["complete_action"]
    initial_state_screenshot = state["initial_screenshot"]

    llm = get_task_status_llm(
        complete_action=complete_action, initial_screenshot=initial_state_screenshot
    )

    message = llm.invoke({"history": []})

    return {"messages": [message]}


def prepare_for_reiterate_node(state: State):
    one_cycle_complete_message = state["execution_action"] + " done successfully"

    messages = state["messages"]

    new_messages = [RemoveMessage(id=m.id) for m in messages[1:]]
    return {
        "messages": new_messages + [HumanMessage(content=one_cycle_complete_message)],
        "execution_list": ["clear"],
    }


####################################################### EDGES #################################################################################
def execution_or_end(state) -> Literal["executing_tools", "__end__"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "executing_tools"
    ### TODO: Error handling
    return "__end__"


def cleanmessages_or_task_status(
    state,
) -> Literal["clean_messages", "check_task_status"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    ai_message: str = ai_message.content
    json_pattern = r"\{.*?\}"
    match = re.search(json_pattern, ai_message, re.DOTALL)
    execution_status = json.loads(match.group())

    if execution_status["action_completed"]:
        return "check_task_status"
    else:
        return "clean_messages"


def reiterate_or_end(state) -> Literal["prepare_for_reiterate", "__end__"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    ai_message: str = ai_message.content
    json_pattern = r"\{.*?\}"
    match = re.search(json_pattern, ai_message, re.DOTALL)
    execution_status = json.loads(match.group())

    if execution_status["task_completed"]:
        return "__end__"
    else:
        return "prepare_for_reiterate"
