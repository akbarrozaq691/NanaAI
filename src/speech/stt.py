from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client for transcription
openai_client = OpenAI()

def transcribe_audio(audio_file):
    with open(audio_file, "rb") as file:
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            language="en"
        )
    return transcription.text