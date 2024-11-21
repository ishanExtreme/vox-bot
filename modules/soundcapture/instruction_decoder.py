from typing import List
import time
import io
import wave

import numpy as np
import sounddevice as sd
import webrtcvad

from modules.soundcapture.speech_to_text import openai_speech_to_text


class InstructionDecoder:
    def __init__(
        self, sample_rate=16000, channels=1, inactivity_timeout=2.5, max_duration=2
    ):
        """
        :param sample_rate: sample rate of audio
        :param channels: channels for audio input
        :inactivity_timeout: max inactivity in seconds
        :max_duration: max duration in minutes
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.inactivity_timeout = inactivity_timeout
        self.max_duration = max_duration

        # initialize WebRTC VAD
        self.vad = webrtcvad.Vad()
        # aggressiveness level (0 to 3) - higher is more aggressive
        self.vad.set_mode(3)
        self.frame_size = int(self.sample_rate * 0.02)  # lets take 20 ms frames

        # waits extra time when no first word is spoken (in seconds)
        self.spare_time = 10

    def __is_speech(self, frame: bytes) -> bool:
        return self.vad.is_speech(frame, self.sample_rate)

    def listen_and_get_instructions(self):
        start_time = time.time()
        last_active_time = start_time + self.spare_time
        max_duration_seconds = self.max_duration * 60

        recorded_frames: List[np.ndarray] = []
        audio_buffer = np.zeros((0,), dtype=np.int16)

        def audio_callback(indata: np.ndarray, frames, stream_time, status):
            # using variables of parent function(since they are reassigned)
            nonlocal last_active_time
            nonlocal audio_buffer

            audio_chunk = (indata * 32767).astype(np.int16).flatten()
            audio_buffer = np.concatenate((audio_buffer, audio_chunk))

            while len(audio_buffer) >= self.frame_size:
                frame = audio_buffer[: self.frame_size]
                audio_buffer = audio_buffer[self.frame_size :]

                if self.__is_speech(frame.tobytes()):
                    last_active_time = time.time()
                    recorded_frames.append(frame)

        print("started instruction listening")
        with sd.InputStream(
            samplerate=self.sample_rate, channels=self.channels, callback=audio_callback
        ):

            while True:
                current_time = time.time()

                # check for inactivity
                if current_time - last_active_time > self.inactivity_timeout:
                    print("Stopped listening: Inactivity timeout reached.")
                    break
                # check for max duration
                if current_time - start_time > max_duration_seconds:
                    print("Stopped listening: Maximum duration reached.")
                    break

                # prevents high cpu usage
                time.sleep(0.1)

            audio_data = b"".join(chunk.tobytes() for chunk in recorded_frames)

            wav_buffer = io.BytesIO()

            with wave.open(wav_buffer, "wb") as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(np.dtype(np.int16).itemsize)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data)

            wav_bytes = wav_buffer.getvalue()
            return openai_speech_to_text(wav_bytes)
