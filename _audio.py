import os
import io
import requests
from dotenv import load_dotenv

load_dotenv()
VOICE_API_KEY = os.getenv('VOICE_API_KEY')

def text_to_speech(text):

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/LaaUN1T7Yu9yqBIZjz5c"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": VOICE_API_KEY
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    # "language_code": "tr", # For some reason 'fa' isn't supported, but 'tr' (Turkish) is close enough for Farsi phonetics
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "speed": 0.7
    }
    }

    response = requests.post(url, json=data, headers=headers)
    # with open('output.mp3', 'wb') as f:
    #     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    #         if chunk:
    #             f.write(chunk)
    if response.status_code == 200:
        audio_content = io.BytesIO()
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                audio_content.write(chunk)
        audio_content.seek(0)
        return audio_content
    else:
        raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
