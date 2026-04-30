import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from _audio import text_to_speech

st.session_state['farsi_word'] = ""

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


st.title('English ⇨ Farsi Translator')
english = st.text_input('Enter English (word or phrase) to translate to Finglish')
if st.button('Translate ⇨ Finglish') or english:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    stream = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "system", "content": "translate this to Farsi in phonetics. Only state the phonetics."}
            ,{"role": "user", "content": english}],
        stream=True,
    )
    write_stream = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            write_stream += chunk.choices[0].delta.content
    st.write(write_stream)

    farsi = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "system", "content": "translate this to Farsi. Only state the farsi."}
            ,{"role": "user", "content": write_stream}],
        stream=True,
    )
    write_farsi = ""

    for chunk in farsi:
        if chunk.choices[0].delta.content is not None:
            write_farsi += chunk.choices[0].delta.content
    st.write(write_farsi)
    st.session_state['farsi_word'] = write_farsi

    # Audio Gen
    if st.button('Speak'):
        try:
            aud = text_to_speech(st.session_state['farsi_word'])
            st.audio(aud, format="audio/mp3", start_time=0)
        except Exception as e:
            st.error(f"Failed to generate speech: {e}")

st.divider()


st.title('Farsi ⇨ English Translator')
phonetic = st.text_input('Enter farsi phonetic (word or phrase) to translate to English')
if st.button('Translate ⇨ English') or phonetic:

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    stream = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "system", "content": "help me translate the Farsi phonetics to english. Only state the english meaning."}
            ,{"role": "user", "content": phonetic}],
        stream=True,
    )
    write_stream = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            write_stream += chunk.choices[0].delta.content
    st.write(write_stream)
