import streamlit as st
from st_audiorec import st_audiorec
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import tempfile

st.set_page_config(page_title="🎙 Live Voice to Text & TTS", layout="centered")
st.title("🗣️ Live Speech to Text and Text-to-Speech App")

# 🎤 Record audio using streamlit-audio-recorder
wav_audio_data = st_audiorec()

recognized_text = ""

if wav_audio_data:
    # Save the recorded audio to a temp WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(wav_audio_data)
        tmp_path = tmp.name
        st.audio(wav_audio_data, format='audio/wav')

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        st.success(f" Recognized Text: **{recognized_text}**")
    except sr.UnknownValueError:
        st.error(" Could not understand audio.")
    except sr.RequestError:
        st.error(" Speech recognition service is unavailable.")

# 🔘 Convert recognized text to speech
if recognized_text and st.button(" Convert to Speech"):
    tts = gTTS(recognized_text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3")
