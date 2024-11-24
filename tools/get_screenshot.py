from typing import Literal
import base64
from io import BytesIO
from uuid import uuid4

from PIL import Image
import mss

from config import SCREENSHOT_PATH

def get_screenshot(output_type: Literal["base_64", "saved_path"], monitor=1):
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[monitor])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    if output_type == "base_64":
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{image_base64}"
    if output_type == "saved_path":
        file_path = f"{SCREENSHOT_PATH}/{uuid4()}.png"
        img.save(file_path)
        return file_path
