import streamlit as st
import base64
from elevenlabs import VoiceSettings
import uuid
from elevenlabs.client import ElevenLabs

# Initialize ElevenLabs client
client = ElevenLabs()

def autoplay_audio(file_path: str):
    """Function to create an HTML audio player with autoplay"""
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_id = f"audio_{uuid.uuid4().hex}"
    
    html = f'''
        <audio id="{audio_id}" autoplay="true">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>
            document.getElementById("{audio_id}").play();
        </script>
    '''
    return html

def text_to_speech_response(text: str) -> str:
    """Convert text to speech and return the file path"""
    try:
        response = client.text_to_speech.convert(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Rachel voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.8,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True,
                speaking_rate=0.1,
            ),
        )

        save_file_path = f"bot_responses/response_{uuid.uuid4()}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        return save_file_path
    except Exception as e:
        st.error(f"Error generating audio response: {e}")
        return None