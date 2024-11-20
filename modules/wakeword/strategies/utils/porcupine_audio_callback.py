from typing import Callable

import numpy as np

from config import NOTIFICATION_SOUND_PATH
from modules.wakeword.strategies.wakeword import WakeWordDetectStrategy
from modules.wakeword.strategies.audio_capture import AudioCaptureStrategy
from tools.play_sound import play_mp3_in_background


class PorcupineAudioCallback:
    def __init__(
        self,
        wake_word_detector: WakeWordDetectStrategy,
        action_callback: Callable,
    ):
        self.wake_word_detector = wake_word_detector
        self.action_callback = action_callback

    def __call__(
        self, indata, frames, time, status, audio_capture: AudioCaptureStrategy
    ):
        if status:
            print(f"Audio status: {status}")

        # porcupine acceptable audio data
        pcm = np.int16(indata[:, 0] * 32767).tolist()

        if self.wake_word_detector.detect_wake_word(pcm):
            print("wake word detected")
            play_mp3_in_background(NOTIFICATION_SOUND_PATH)
            audio_capture.stop_capture()
            self.action_callback()
            audio_capture.start_capture()
