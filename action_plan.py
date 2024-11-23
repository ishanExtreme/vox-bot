import time

from config import NOTIFICATION_END_SOUND_PATH
from modules.soundcapture import InstructionDecoder
from tools.play_sound import play_mp3_blocking
from modules.brain import VoxGraph


class ActionPlan:

    def __call__(self):
        instruction_decoder = InstructionDecoder()
        instruction = instruction_decoder.listen_and_get_instructions()

        print(instruction)

        if len(instruction) == 0 or instruction == "you":
            play_mp3_blocking(NOTIFICATION_END_SOUND_PATH)
            return

        vox_graph = VoxGraph()
        vox_graph.get_mermaid_image()
        vox_graph.start_vox_brain(human_instruction=instruction)
        print("Finished action")
