from abc import ABC, abstractmethod
from typing import List

import pvporcupine


class WakeWordDetectStrategy(ABC):
    @abstractmethod
    def detect_wake_word(self, audio_data):
        pass


class PorcupineWakeWordDetection(WakeWordDetectStrategy):
    def __init__(self, access_key: str, keyword_paths: List[str]):
        self.porcupine = pvporcupine.create(
            access_key=access_key, keyword_paths=keyword_paths
        )

    def detect_wake_word(self, audio_data):
        keyword_index = self.porcupine.process(audio_data)
        return keyword_index >= 0
