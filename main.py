from config import CUSTOM_MODEL_PATH, ACCESS_KEY
from modules.wakeword import SoundDeviceCapture
from modules.wakeword import PorcupineWakeWordDetection
from modules.wakeword.strategies.utils.porcupine_audio_callback import (
    PorcupineAudioCallback,
)
from modules.wakeword.wakeword_detector import WakeWordDetector
from action_plan import ActionPlan

porcupine_wake_word_detection = PorcupineWakeWordDetection(
    access_key=ACCESS_KEY, keyword_paths=[CUSTOM_MODEL_PATH]
)

action_callback = ActionPlan()
callback = PorcupineAudioCallback(
    porcupine_wake_word_detection, action_callback=action_callback
)
audio_capture = SoundDeviceCapture(
    sample_rate=porcupine_wake_word_detection.porcupine.sample_rate,
    block_size=porcupine_wake_word_detection.porcupine.frame_length,
    callback=lambda indata, frames, time, status: callback(
        indata, frames, time, status, audio_capture
    ),
)

detector = WakeWordDetector(audio_capture, porcupine_wake_word_detection)

if __name__ == "__main__":
    try:
        detector.listen_for_wake_word()
    except KeyboardInterrupt:
        pass
