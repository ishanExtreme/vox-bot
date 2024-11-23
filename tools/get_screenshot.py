from typing import Literal

import base64
from io import BytesIO

from PIL import Image
import mss


def get_screenshot(output_type: Literal["base_64"], monitor=1):
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    if output_type == "base_64":
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{image_base64}"
