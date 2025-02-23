from typing import Literal
import time

import pyautogui


def get_center(shape):

    center_x = shape["x"] + shape["width"] / 2
    center_y = shape["y"] + shape["height"] / 2
    return center_x, center_y


def move_mouse_to_id_helper(bounding_box_id, omniparser_map: list):
    shape = None
    for data in omniparser_map:
        if data["id"] == bounding_box_id:
            shape = data["shape"]
    if shape == None:
        raise ValueError("Shape not found")
    x, y = get_center(shape)

    pyautogui.moveTo(x, y, duration=0.5)


def click_mouse_button_helper(
    button_type: Literal["left_click", "right_click", "double_click"]
):
    if button_type == "left_click":
        pyautogui.click()
    elif button_type == "right_click":
        pyautogui.click(button="right")
    else:
        pyautogui.doubleClick()

    # Wait for click action to complete, TODO: make it more dynamic in future
    time.sleep(3)


def type_using_keyboard_helper(sentence: str):
    pyautogui.write(sentence, interval=0.1)


def press_hotkeys_or_enter_helper(hotkeys: str):
    if hotkeys == "enter":
        pyautogui.press("enter")
    else:
        keys = hotkeys.split("+")
        pyautogui.hotkey(*keys)

    # Wait for click action to complete, TODO: make it more dynamic in future
    time.sleep(3)
