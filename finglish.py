import os
import pathlib
import logging
import shutil
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from _audio import text_to_speech
from bs4 import BeautifulSoup

# Initialize session state
if 'farsi_word' not in st.session_state:
    st.session_state['farsi_word'] = ""
if 'finglish_word' not in st.session_state:
    st.session_state['finglish_word'] = ""

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ADSENSE_CLIENT_ID = os.getenv('ADSENSE_CLIENT_ID')

adsense_url = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}"
GA_AdSense_ = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous">></script>
    <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
"""

# Insert the script in the head tag of the static template inside your virtual
index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
logging.info(f'editing {index_path}')
soup = BeautifulSoup(index_path.read_text(), features="html.parser")
if not soup.find(script, src=adsense_url):
    bck_index = index_path.with_suffix('.bck')
    if bck_index.exists():
        shutil.copy(bck_index, index_path)
    else:
        shutil.copy(index_path, bck_index)
    html = str(soup)
    new_html = html.replace('<head>', '<head>\n' + GA_AdSense)
    index_path.write_text(new_html)

st.set_page_config(page_title="English to Farsi Translation", page_icon=":iran:")
st.title('English ⇨ Farsi Translator')
english = st.text_input('Enter English (word or phrase) to translate to Finglish')
if st.button('Translate ⇨ Finglish'):
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
