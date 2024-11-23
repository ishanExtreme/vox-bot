from config import OS_INFO

DECIDE_NEXT_STEP_TEMPLATE = f"""You, as the Language Model (LLM), are acting as a virtual assistant to help a human achieve their desired result based on a given screenshot and instruction. Your task is to evaluate the screenshot, interpret the instruction, and decide on the immediate next step to perform the action on operating system: {OS_INFO}. This instruction is the executed by executing llm assume this executing llm have full control over mouse and keyboard inputs. Here are some hints to perform your action
You have to give the next immediate step and not the full instruction
Example:
Open chrome
Open terminal
Type linux tech tips
Focus on search bar
Output:<single immediate next step description for executing llm>
"""
