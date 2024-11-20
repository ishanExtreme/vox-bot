from modules.wakeword.strategies.audio_capture import AudioCaptureStrategy
from modules.wakeword.strategies.wakeword import WakeWordDetectStrategy


class WakeWordDetector:
    def __init__(
        self,
        audio_capture_strategy: AudioCaptureStrategy,
        wake_word_strategy: WakeWordDetectStrategy,
    ):
        self.audio_capture_strategy = audio_capture_strategy
        self.wake_word_strategy = wake_word_strategy

    def listen_for_wake_word(self):
        print("Listening for wake word...")
        self.audio_capture_strategy.start_capture()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Listening stopped")
