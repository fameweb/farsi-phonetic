import os
import requests
from dotenv import load_dotenv

load_dotenv()
VOICE_API_KEY = os.getenv('VOICE_API_KEY')

def text_to_speech(text):
    
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/uQhw7tLMkUTkio2epxYQ"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": VOICE_API_KEY
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.7,
        "similarity_boost": 0.2
    }
    }

    response = requests.post(url, json=data, headers=headers)
    # with open('output.mp3', 'wb') as f:
    #     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    #         if chunk:
    #             f.write(chunk)
    if response.status_code == 200:
        audio_content = b''
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                audio_content += chunk
        return audio_content
    else:
        return None
