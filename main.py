from modules.wakeword import SoundDeviceCapture
from modules.wakeword import PorcupineWakeWordDetection
from modules.wakeword.strategies.utils.porcupine_audio_callback import (
    PorcupineAudioCallback,
)
from modules.wakeword.wakeword_detector import WakeWordDetector

custom_model_path = "Hey-vox/Hey-vox.ppn"
access_key = "IDNKisYX0LHFNlmcYsLMAq/CIWpvtwB2pej066atlK9RLCDCiOz4QQ=="

porcupine_wake_word_detection = PorcupineWakeWordDetection(
    access_key=access_key, keyword_paths=[custom_model_path]
)


def action_callback():
    print("action callback called")


callback = PorcupineAudioCallback(porcupine_wake_word_detection, action_callback)
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
