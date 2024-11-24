from typing import Literal

from langchain.tools import tool

@tool("move_mouse_to_id")
def move_mouse_to_id(bounding_box_id:int) -> str:
  """Move the mouse pointer at the center of given id of bounding box"""

  print(f"Moved to {bounding_box_id}")
  return f"Moved to {bounding_box_id}"

@tool("click_mouse_button")
def click_mouse_button(button_type: Literal["left_click", "right_click"]) -> str:
  """Click the mouse button based on button_type given either left_click or right_click"""

  print(f"Mouse pressed: {button_type}")
  return f"Mouse pressed: {button_type}"

@tool("type_using_keyboard")
def type_using_keyboard(sentence: str) -> str:
  """Type the sentence given using keyboard"""

  print(f"Typed: {sentence}")
  return f"Typed: {sentence}"

@tool("press_keyboard_shortcut")
def press_keyboard_shortcut(keyboard_shortcut: str) -> str:
  """Press the keyboard shortcut using pyautogui, example keyboard_shortcut='ctrl+s'"""

  print(f"Keyboard shortcut pressed: {keyboard_shortcut}")
  return f"Keyboard shortcut pressed: {keyboard_shortcut}"

def get_all_execution_tools():
  return[move_mouse_to_id, click_mouse_button, type_using_keyboard, press_keyboard_shortcut]