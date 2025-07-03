import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from langdetect import detect
from gtts import gTTS

st.set_page_config(page_title="OCR + TTS (Cloud)", layout="centered")
st.title("📷 Cloud OCR + Text-to-Speech App")

# ⬆ Upload Image
uploaded_file = st.file_uploader("📤 Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to bytes
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # 🔑 Replace this with your API key from ocr.space
    api_key = "helloworld"  # Free demo key (limited)

    # Send to OCR.space API
    with st.spinner("⏳ Performing OCR..."):
        response = requests.post(
            "K83683705188957",
            files={"filename": img_bytes},
            data={"apikey": api_key, "language": "eng"},
        )

    result = response.json()
    text = result['ParsedResults'][0]['ParsedText'].strip() if result['IsErroredOnProcessing'] == False else ""

    if text:
        st.subheader("📝 Extracted Text")
        st.text_area("Detected Text", value=text, height=200)

        # Language Detection
        try:
            lang = detect(text)
        except:
            lang = "en"
        st.markdown(f"🌐 **Detected Language:** `{lang}`")

        # TTS Button
        if st.button("🔊 Speak Text"):
            tts = gTTS(text=text, lang=lang)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            st.audio(mp3_fp, format="audio/mp3")
    else:
        st.error("❌ OCR failed or no text found.")
