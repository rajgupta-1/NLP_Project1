import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from langdetect import detect
from gtts import gTTS

st.set_page_config(page_title="OCR + TTS (Cloud)", layout="centered")
st.title("📷 OCR + Text-to-Speech App (OCR.space)")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # API key
    api_key = "K83683705188957"  # ✅ Your key

    # Send to OCR.space
    with st.spinner("⏳ Performing OCR..."):
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": ("image.png", img_bytes, "image/png")},  # <-- FIXED
            data={
                "apikey": api_key,
                "language": "eng",
                "isOverlayRequired": False
            }
        )

    result = response.json()

    # Extract text
    if result.get("IsErroredOnProcessing") == False:
        parsed_text = result["ParsedResults"][0]["ParsedText"].strip()

        if parsed_text:
            st.subheader("📝 Extracted Text")
            st.text_area("Detected Text", value=parsed_text, height=200)

            # Language detection
            try:
                lang = detect(parsed_text)
            except:
                lang = "en"
            st.markdown(f"🌐 **Detected Language:** `{lang}`")

            if st.button("🔊 Speak Text"):
                tts = gTTS(text=parsed_text, lang=lang)
                mp3_fp = BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                st.audio(mp3_fp, format="audio/mp3")
        else:
            st.warning("⚠️ No text detected in the image.")
    else:
        st.error("❌ OCR failed.")
        st.warning(f"🛠 Error: {result.get('ErrorMessage', 'Unknown error')}")
