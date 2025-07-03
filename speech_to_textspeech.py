import streamlit as st
from PIL import Image
import pytesseract
from langdetect import detect
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="🧠 OCR + Text-to-Speech", layout="centered")
st.title("📷 OCR Text Reader with Voice")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR directly with Pillow image (no OpenCV)
    text = pytesseract.image_to_string(image).strip()

    if text:
        st.subheader("📝 Extracted Text")
        st.text_area("Detected Text", value=text, height=200)

        # Detect Language
        try:
            lang = detect(text)
        except:
            lang = "en"
        st.markdown(f"🌐 **Detected Language:** `{lang}`")

        # Button to speak the text
        if st.button("🔊 Read Text Aloud"):
            tts = gTTS(text=text, lang=lang)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            st.audio(mp3_fp, format="audio/mp3")
    else:
        st.warning("❗ No text found in the image.")
