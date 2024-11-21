import time
from modules.soundcapture import InstructionDecoder


class ActionPlan:

    def __call__(self):
        instruction_decoder = InstructionDecoder()
        instructions = instruction_decoder.listen_and_get_instructions()

        print(instructions)
