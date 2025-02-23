from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from langchain_core.runnables.graph import MermaidDrawMethod


from modules.brain.langgraph_config.state import State
from modules.brain.langgraph_config.nodes import (
    decide_next_step_node,
    decide_executable_node,
    execution_or_end,
    check_execution_status_node,
    cleanmessages_or_task_status,
    clean_messages_node,
    check_task_status_node,
    prepare_for_reiterate_node,
    reiterate_or_end,
)
from modules.brain.langgraph_config.tools import get_all_execution_tools
from modules.brain.langgraph_config.utils.custom_tool_node import CustomToolNode


class VoxGraph:

    def __init__(self):
        graph_builder = StateGraph(State)
        execution_tools = get_all_execution_tools()

        executing_tools_node = CustomToolNode(tools=execution_tools)
        graph_builder.add_node("decide_next_step", decide_next_step_node)
        graph_builder.add_node("decide_executable", decide_executable_node)
        graph_builder.add_node("executing_tools", executing_tools_node)
        graph_builder.add_node("check_execution_status", check_execution_status_node)
        graph_builder.add_node("clean_messages", clean_messages_node)
        graph_builder.add_node("check_task_status", check_task_status_node)
        graph_builder.add_node("prepare_for_reiterate", prepare_for_reiterate_node)

        graph_builder.add_edge("decide_next_step", "decide_executable")
        graph_builder.add_conditional_edges("decide_executable", execution_or_end)
        graph_builder.add_edge("executing_tools", "check_execution_status")
        graph_builder.add_conditional_edges(
            "check_execution_status", cleanmessages_or_task_status
        )
        graph_builder.add_edge("clean_messages", "decide_executable")
        graph_builder.add_conditional_edges("check_task_status", reiterate_or_end)
        graph_builder.add_edge("prepare_for_reiterate", "decide_next_step")

        graph_builder.set_entry_point("decide_next_step")

        self.graph = graph_builder.compile()

    def get_graph(self) -> CompiledGraph:
        return self.graph

    def get_mermaid_image(self) -> str:
        png_in_bytes = self.graph.get_graph().draw_ascii()
        print(png_in_bytes)
        # save the image to a file
        image_data = self.graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        output_file = "graph.png"
        with open(output_file, "wb") as f:
            f.write(image_data)

    def start_vox_brain(self, human_instruction):
        user_message = HumanMessage(human_instruction)

        inputs = {"messages": [user_message]}

        for events in self.graph.stream(input=inputs, config={"recursion_limit": 200}):
            print(events)
