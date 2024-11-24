from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode


from modules.brain.langgraph_config.state import State
from modules.brain.langgraph_config.nodes import decide_next_step_node, decide_executable_nodes, execution_or_repeat
from modules.brain.langgraph_config.tools import get_all_execution_tools

class VoxGraph:

    def __init__(self):
        graph_builder = StateGraph(State)
        execution_tools = get_all_execution_tools()

        executing_tools_node = ToolNode(tools=execution_tools)
        graph_builder.add_node("decide_next_step", decide_next_step_node)
        graph_builder.add_node("decide_executable", decide_executable_nodes)
        graph_builder.add_node("executing_tools", executing_tools_node)

        graph_builder.add_edge("decide_next_step", "decide_executable")
        graph_builder.add_conditional_edges("decide_executable", execution_or_repeat)

        graph_builder.set_entry_point("decide_next_step")
        graph_builder.set_finish_point("executing_tools")

        self.graph = graph_builder.compile()

    def get_graph(self) -> CompiledGraph:
        return self.graph

    def get_mermaid_image(self) -> str:
        png_in_bytes = self.graph.get_graph().draw_ascii()
        print(png_in_bytes)

    def start_vox_brain(self, human_instruction):
        user_message = HumanMessage(human_instruction)

        inputs = {"messages": [user_message]}

        for events in self.graph.stream(input=inputs):
            print(events)
