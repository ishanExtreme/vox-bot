from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)
from langchain_core.messages import HumanMessage

from config import OPENAI_KEY
from modules.brain.langgraph_config.prompt_templates import DECIDE_NEXT_STEP_TEMPLATE
from tools.get_screenshot import get_screenshot


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
