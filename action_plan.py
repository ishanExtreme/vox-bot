import time

from tools.play_sound import play_mp3_in_background
from config import INITIATING_VOICE_PATH


class ActionPlan:

    def __call__(self):
        print("Starting action")
        time.sleep(10)
        print("Action done")
