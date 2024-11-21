import time

from config import NOTIFICATION_END_SOUND_PATH
from modules.soundcapture import InstructionDecoder
from tools.play_sound import play_mp3_blocking


class ActionPlan:

    def __call__(self):
        instruction_decoder = InstructionDecoder()
        instructions = instruction_decoder.listen_and_get_instructions()

        print(instructions)
        if len(instructions) == 0 or instructions == "you":
            play_mp3_blocking(NOTIFICATION_END_SOUND_PATH)
