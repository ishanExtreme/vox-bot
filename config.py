import os
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")

ROOT_DIR = Path(__file__).resolve(strict=True).parent


INITIATING_VOICE_PATH = "static/voices/initiating.mp3"
NOTIFICATION_SOUND_PATH = "static/voices/notification.mp3"
NOTIFICATION_END_SOUND_PATH = "static/voices/notification_end.mp3"

__get_env = lambda key: config.get(key, os.environ.get(key))

CUSTOM_MODEL_PATH = "Hey-vox/Hey-vox.ppn"
ACCESS_KEY = __get_env("PICOVOICE_ACCESS_KEY")

OPENAI_KEY = __get_env("OPENAI_API_KEY")

import platform

OS_INFO = str(platform.uname())

### Langchain

import getpass
import os


os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "vox"
os.environ["LANGCHAIN_API_KEY"] = __get_env("LANGCHAIN_API_KEY")

## Omniparser
ICONDETECT_WEIGHTS_PATH = str(ROOT_DIR/"static/weights/icon_detect/best.pt")
FLORENCE_WEIGHT_PATH = str(ROOT_DIR/"static/weights/icon_caption_florence")
BOX_TRESHOLD=0.05

SCREENSHOT_PATH = str(ROOT_DIR / "static/screenshots")
