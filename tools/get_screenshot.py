from typing import Literal
import base64
from io import BytesIO
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont
import mss

from config import SCREENSHOT_PATH


def draw_text(image: Image, text: str):
    draw = ImageDraw.Draw(image)
    position = (0, 0)
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        # Default font if specific font not available
        font = ImageFont.load_default()
    color = "black"
    draw.text(position, text, fill=color, font=font)

    return image


def get_openai_path(image: Image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{image_base64}"


def get_screenshot(output_type: Literal["base_64", "saved_path"], monitor=1, text=""):
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[monitor])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        if text:
            img = draw_text(img, text)

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
