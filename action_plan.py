from tools.play_sound import play_mp3_in_background
from config import INITIATING_VOICE_PATH


class ActionPlan:

    def __call__(self):
        play_mp3_in_background(INITIATING_VOICE_PATH)
