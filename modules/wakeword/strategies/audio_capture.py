from abc import ABC, abstractmethod

import sounddevice as sd


class AudioCaptureStrategy(ABC):
    @abstractmethod
    def start_capture(self):
        pass

    @abstractmethod
    def stop_capture(self):
        pass

    @abstractmethod
    def get_audio_data(self):
        pass


class SoundDeviceCapture(AudioCaptureStrategy):
    def __init__(self, sample_rate: int, block_size: int, callback):
        self.channels = 1
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.callback = callback
        self.stream = None

    def start_capture(self):
        self.stream = sd.InputStream(
            channels=self.channels,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            callback=self.callback,
        )
        self.stream.start()

    def stop_capture(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def get_audio_data(self):
        pass
