from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent


INITIATING_VOICE_PATH = "static/voices/initiating.mp3"
NOTIFICATION_SOUND_PATH = "static/voices/notification.mp3"
NOTIFICATION_END_SOUND_PATH = "static/voices/notification_end.mp3"

CUSTOM_MODEL_PATH = "Hey-vox/Hey-vox.ppn"
ACCESS_KEY = "IDNKisYX0LHFNlmcYsLMAq/CIWpvtwB2pej066atlK9RLCDCiOz4QQ=="

OPENAI_KEY = "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"

import platform

OS_INFO = str(platform.uname())

### Langchain

import getpass
import os


os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "vox"
os.environ["LANGCHAIN_API_KEY"] = "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"

## Omniparser
ICONDETECT_WEIGHTS_PATH = str(ROOT_DIR/"static/weights/icon_detect/best.pt")
FLORENCE_WEIGHT_PATH = str(ROOT_DIR/"static/weights/icon_caption_florence")
BOX_TRESHOLD=0.05

SCREENSHOT_PATH = str(ROOT_DIR / "static/screenshots")
