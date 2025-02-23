from typing import Literal
from typing_extensions import Annotated


from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from modules.brain.langgraph_config.utils.executing_tools_helper import (
    move_mouse_to_id_helper,
    click_mouse_button_helper,
    type_using_keyboard_helper,
    press_hotkeys_or_enter_helper,
)


@tool("move_mouse_to_id")
def move_mouse_to_id(
    bounding_box_id: int, state: Annotated[dict, InjectedState]
) -> str:
    """Move the mouse pointer at the center of given id of bounding box"""

    move_mouse_to_id_helper(bounding_box_id, state["bounding_box_hash"])
    return f"Moved mouse to {bounding_box_id} -> Done"


@tool("click_mouse_button")
def click_mouse_button(
    button_type: Literal["left_click", "right_click", "double_click"]
) -> str:
    """Click the mouse button based on button_type given either left_click, right_click or double_click"""

    click_mouse_button_helper(button_type=button_type)
    return f"Mouse key pressed: {button_type} -> Done"


@tool("type_using_keyboard")
def type_using_keyboard(sentence: str) -> str:
    """Type the sentence given using keyboard"""

    type_using_keyboard_helper(sentence=sentence)
    return f"Typed: {sentence} -> Done"


@tool("press_hotkeys_or_enter")
def press_hotkeys_or_enter(hotkeys: str) -> str:
    """Press the keyboard hotkeys using pyautogui, example hotkeys='ctrl+s' or press enter using hotkeys='enter'"""

    press_hotkeys_or_enter_helper(hotkeys=hotkeys)
    return f"Keyboard shortcut pressed: {hotkeys} -> Done"


## TODO create scroll function


def get_all_execution_tools():
    return [
        move_mouse_to_id,
        click_mouse_button,
        type_using_keyboard,
        press_hotkeys_or_enter,
    ]
