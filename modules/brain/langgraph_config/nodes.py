from langchain_core.messages import AIMessage

from modules.brain.langgraph_config.state import State
from modules.brain.langgraph_config.llm import get_decide_next_step_llm

####################################################### NODES #################################################################################


def decide_next_step_node(state: State):
    llm = get_decide_next_step_llm()

    message = llm.invoke(state["messages"])
    return {"messages": [message]}


def executing_node(state: State):
    instruction = state["messages"][-1]

    output = AIMessage(content=f"Performed successfully '{instruction}'")
    return {"messages": [output]}
