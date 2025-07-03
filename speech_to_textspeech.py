import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
from langdetect import detect
from gtts import gTTS
from io import BytesIO
import tempfile

st.set_page_config(page_title="🧠 OCR Text Reader", layout="centered")
st.title("📸 OCR + Text-to-Speech Web App")

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # OCR Text extraction
    text = pytesseract.image_to_string(thresh).strip()
    st.subheader("📝 Extracted Text")
    st.text_area("Text", value=text, height=200)

    # Detect language
    lang = detect(text) if text else "unknown"
    st.markdown(f"🌐 **Detected Language:** `{lang}`")

    # Text to Speech
    if st.button("🔊 Speak Text"):
        try:
            tts = gTTS(text=text, lang=lang)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            st.audio(mp3_fp, format="audio/mp3")
        except Exception as e:
            st.error(f"Error in TTS: {e}")
