from typing import Dict, Tuple
import time

from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage

from config import OPENAI_KEY
from tools.get_screenshot import get_screenshot, get_openai_path
from modules.brain.langgraph_config.prompt_templates import (
    DECIDE_NEXT_STEP_TEMPLATE,
    DECIDE_EXECUTABLE_TEMPLATE,
    EXECUTION_STATUS_TEMPLATE,
    TASK_STATUS_TEMPLATE,
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


def get_decide_executable_llm(
    action: str, performed_executions: list, temperature=0.3
) -> Tuple[ChatOpenAI, Dict, str]:
    execution_tools = get_all_execution_tools()
    system_prompt = PromptTemplate(
        template=DECIDE_EXECUTABLE_TEMPLATE,
        input_variables=[],
        template_format="jinja2",
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

    initiate_omniparser()
    file_path_base_64, return_list, simplified_return_list, file_path = (
        result_watchdog()
    )

    ss_message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": file_path_base_64},
            }
        ]
    )
    meta_message = AIMessage(content=f"bounding_box_meta: {simplified_return_list}")
    action_message_content = f"Action to be performed: {action}"
    if len(performed_executions) > 0:
        cumulated_message = "Steps already taken: " + (",").join(performed_executions)
        action_message_content = action_message_content + "\n" + cumulated_message
    action_message = HumanMessage(content=action_message_content)

    message_prompt = MessagesPlaceholder(variable_name="history")
    chat_prompt_messages = [
        system_message_prompt,
        ss_message,
        meta_message,
        action_message,
        message_prompt,
    ]

    print("preparing chat message")
    chat_prompt = ChatPromptTemplate.from_messages(chat_prompt_messages)

    print("initializing llm")
    llm = ChatOpenAI(api_key=OPENAI_KEY, temperature=temperature, model="gpt-4o")
    print("binding tools")
    llm_with_tools = llm.bind_tools(tools=execution_tools)

    print("chaining")
    chain = chat_prompt | llm_with_tools

    print("finished")
    return chain, return_list, file_path


def get_execution_status_llm(
    execution_action: str, previous_state_screenshot: str, temperature=0.3
):
    system_prompt = PromptTemplate(
        template=EXECUTION_STATUS_TEMPLATE,
        input_variables=[],
        template_format="jinja2",
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

    previous_state_img = Image.open(previous_state_screenshot)

    prev_ss_message = HumanMessage(
        content=[
            {"type": "text", "text": "previous state screenshot"},
            {
                "type": "image_url",
                "image_url": {"url": get_openai_path(previous_state_img)},
            },
        ]
    )

    curr_ss_message = HumanMessage(
        content=[
            {"type": "text", "text": "current state screenshot"},
            {
                "type": "image_url",
                "image_url": {"url": get_screenshot(output_type="base_64")},
            },
        ]
    )
    action_message_content = f"Goal action to be performed: {execution_action}"
    action_message = HumanMessage(content=action_message_content)
    message_prompt = MessagesPlaceholder(variable_name="history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            curr_ss_message,
            prev_ss_message,
            action_message,
            message_prompt,
        ]
    )

    llm = ChatOpenAI(api_key=OPENAI_KEY, temperature=temperature, model="gpt-4o")

    chain = chat_prompt | llm

    return chain


def get_task_status_llm(complete_action: str, initial_screenshot: str, temperature=0.5):
    system_prompt = PromptTemplate(
        template=TASK_STATUS_TEMPLATE,
        input_variables=[],
        template_format="jinja2",
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

    initial_state_img = Image.open(initial_screenshot)

    prev_ss_message = HumanMessage(
        content=[
            {"type": "text", "text": "initial state screenshot"},
            {
                "type": "image_url",
                "image_url": {"url": get_openai_path(initial_state_img)},
            },
        ]
    )

    curr_ss_message = HumanMessage(
        content=[
            {"type": "text", "text": "current state screenshot"},
            {
                "type": "image_url",
                "image_url": {"url": get_screenshot(output_type="base_64")},
            },
        ]
    )
    action_message_content = f"Goal task to be performed: {complete_action}"
    action_message = HumanMessage(content=action_message_content)
    message_prompt = MessagesPlaceholder(variable_name="history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            curr_ss_message,
            prev_ss_message,
            action_message,
            message_prompt,
        ]
    )

    llm = ChatOpenAI(api_key=OPENAI_KEY, temperature=temperature, model="gpt-4o")

    chain = chat_prompt | llm

    return chain
