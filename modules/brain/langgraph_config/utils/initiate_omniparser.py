from config import SCREENSHOT_PATH
from tools.get_screenshot import get_screenshot


def initiate_omniparser():
    file_path = get_screenshot(output_type="saved_path")

    with open(SCREENSHOT_PATH + "/start.txt", "w") as file:
        file.write(file_path)
