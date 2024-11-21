from uuid import uuid4

from modules.soundcapture.utils.utils import NamedBytesIO
from openai import OpenAI

from config import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)


def openai_speech_to_text(audio_data):
    file_name = f"{str(uuid4())}.wav"
    named_audio_file = NamedBytesIO(audio_data, name=file_name)
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=named_audio_file, language="en"
    )

    return transcription.text
