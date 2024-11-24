from typing import Dict, Tuple
import time

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage

from config import OPENAI_KEY
from tools.get_screenshot import get_screenshot
from modules.brain.langgraph_config.prompt_templates import (
    DECIDE_NEXT_STEP_TEMPLATE,
    DECIDE_EXECUTABLE_TEMPLATE,
)
from modules.brain.langgraph_config.tools import get_all_execution_tools
from modules.brain.langgraph_config.utils.omniparser_result_watchdog import (
    result_watchdog,
)
from modules.brain.langgraph_config.utils.initiate_omniparser import initiate_omniparser


def get_decide_next_step_llm(temperature=0.5) -> ChatOpenAI:
    system_prompt = PromptTemplate(
        template=DECIDE_NEXT_STEP_TEMPLATE, input_variables=[], template_format="jinja2"
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)
    ss_message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": get_screenshot(output_type="base_64")},
            }
        ]
    )
    message_prompt = MessagesPlaceholder(variable_name="history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, ss_message, message_prompt]
    )

    llm = ChatOpenAI(api_key=OPENAI_KEY, temperature=temperature, model="gpt-4o")

    chain = chat_prompt | llm

    return chain


def get_decide_executable_llm(action: str, temperature=0.3) -> Tuple[ChatOpenAI, Dict]:
    execution_tools = get_all_execution_tools()
    system_prompt = PromptTemplate(
        template=DECIDE_EXECUTABLE_TEMPLATE,
        input_variables=[],
        template_format="jinja2",
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

    print("Starting omniparser")
    st = time.time()
    initiate_omniparser()
    file_path_base_64, return_list, simplified_return_list = result_watchdog()
    print(f"Omniparser took {time.time() - st}")

    ss_message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": file_path_base_64},
            }
        ]
    )
    meta_message = AIMessage(content=f"bounding_box_meta: {simplified_return_list}")
    action_message = HumanMessage(content=f"Action to be performed: {action}")
    message_prompt = MessagesPlaceholder(variable_name="history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            ss_message,
            meta_message,
            action_message,
            message_prompt,
        ]
    )

    llm = ChatOpenAI(api_key=OPENAI_KEY, temperature=temperature, model="gpt-4o")
    llm_with_tools = llm.bind_tools(tools=execution_tools)

    chain = chat_prompt | llm_with_tools

    return chain, return_list
