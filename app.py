# app.py

import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

st.set_page_config(page_title="Speech App", layout="centered")
st.title("🗣️ Speech App")

option = st.selectbox("Choose an Operation", ["Select", "Text to Speech (OP1)", "Speech to Text (OP2)"])

# TEXT TO SPEECH
if option == "Text to Speech (OP1)":
    text = st.text_area("Enter text to speak:")
    if st.button("Convert to Speech"):
        if text:
            tts = gTTS(text)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format="audio/mp3")
        else:
            st.warning("Please enter some text.")

# SPEECH TO TEXT
elif option == "Speech to Text (OP2)":
    st.info("🎤 Record your voice using a microphone-enabled browser.")
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write(" Listening...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                st.success(f" You said: {text}")
            except sr.UnknownValueError:
                st.error(" Could not understand audio.")
            except sr.RequestError:
                st.error("Google service unavailable.")
