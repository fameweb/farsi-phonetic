import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from _audio import text_to_speech

# Initialize session state
if 'farsi_word' not in st.session_state:
    st.session_state['farsi_word'] = ""
if 'finglish_word' not in st.session_state:
    st.session_state['finglish_word'] = ""

# Load environment variables and page configs
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
st.set_page_config(page_title="English to Farsi Translation", page_icon=":iran:")

st.title('English ⇨ Farsi Translator')
with st.form(key='english_to_farsi_form'):
    english = st.text_input('Enter English (word or phrase) to translate to Finglish')
    submit_english = st.form_submit_button('Translate ⇨ Finglish')
    if submit_english:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        stream = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[{"role": "system", "content": "You are a Finglish translator. Translate the English text to Finglish (Farsi written in Latin/Roman alphabet). Only respond with the Finglish transliteration, nothing else. For example: 'How are you' -> 'chetori', 'Thank you' -> 'mersi' or 'mamnoon'."}
                ,{"role": "user", "content": english}],
            stream=True,
        )
        write_stream = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                write_stream += chunk.choices[0].delta.content
        st.session_state['finglish_word'] = write_stream

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
        st.session_state['farsi_word'] = write_farsi

# Display stored results
if st.session_state['finglish_word']:
    st.write(st.session_state['finglish_word'])
if st.session_state['farsi_word']:
    st.write(st.session_state['farsi_word'])

# Audio Gen - outside translation block
if st.session_state['farsi_word'] and st.button('Speak'):
    try:
        aud = text_to_speech(st.session_state['farsi_word'])
        st.audio(aud, format="audio/mp3", start_time=0)
    except Exception as e:
        st.error(f"Failed to generate speech: {e}")

st.divider()


st.title('Farsi ⇨ English Translator')
with st.form(key='farsi_to_english_form'):
    phonetic = st.text_input('Enter farsi phonetic (word or phrase) to translate to English')
    submit_farsi = st.form_submit_button('Translate ⇨ English')
    if submit_farsi and phonetic:
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

st.divider()
st.caption("Credits due: The original application was created by [@mei-chen](https://github.com/mei-chen). This version is a modified fork that fixes some build bugs and utilizes a more efficient translation model.")
