import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import tempfile

st.set_page_config(page_title="🎙️ Voice Recognition + TTS", layout="centered")
st.title("🎧 Voice to Text and Text to Speech App (Web-based)")

# File upload
audio_file = st.file_uploader("📤 Upload a WAV audio file (Mono PCM)", type=["wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    recognizer = sr.Recognizer()

    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.success(f"📝 Recognized Text: **{text}**")

            # Convert recognized text to speech using gTTS
            tts = gTTS(text)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            st.audio(mp3_fp, format="audio/mp3", start_time=0)

        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")

        except sr.RequestError:
            st.error("❌ Speech recognition service is unavailable.")

