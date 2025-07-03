import tkinter as tk
from tkinter import filedialog, Text, messagebox
from PIL import Image, ImageTk
import pytesseract
import cv2
import numpy as np
from langdetect import detect
from gtts import gTTS
import os
import platform
import tempfile

# Function to extract text from image
def extract_text_from_image(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(thresh)
    return text.strip()

# Function to detect language
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Function to speak text using gTTS
def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            if platform.system() == "Windows":
                os.system(f'start {fp.name}')
            elif platform.system() == "Darwin":
                os.system(f'afplay {fp.name}')
            else:
                os.system(f'mpg123 {fp.name}')
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# Upload image, extract text, detect language, auto-read
def upload_image():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not path:
        return

    # Display image
    img = Image.open(path)
    img.thumbnail((400, 400))
    img_display = ImageTk.PhotoImage(img)
    img_label.config(image=img_display)
    img_label.image = img_display

    # Extract text
    text = extract_text_from_image(path)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)

    # Detect language
    lang = detect_language(text)
    lang_label.config(text=f"🌐 Detected Language: {lang}")

    # Automatically speak detected text
    if text:
        speak_text(text, lang)

# Read (edited) text aloud when button is clicked
def read_text():
    user_text = text_box.get("1.0", tk.END).strip()
    if user_text:
        lang = detect_language(user_text)
        lang_label.config(text=f"🌐 Detected Language: {lang}")
        speak_text(user_text, lang)
    else:
        messagebox.showinfo("Info", "No valid text to read.")

# ---------------- GUI Setup ----------------

root = tk.Tk()
root.title("📖 OCR Text Reader with Voice")
root.geometry("500x600")

# Upload Image Button
tk.Button(root, text="📸 Upload Image", command=upload_image, font=("Arial", 12)).pack(pady=10)

# Image display area
img_label = tk.Label(root)
img_label.pack()

# Text display box
text_box = Text(root, height=10, wrap='word', font=("Arial", 11))
text_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Language label
lang_label = tk.Label(root, text="🌐 Detected Language: ", font=("Arial", 11, "italic"))
lang_label.pack(pady=5)

# Read Aloud button
tk.Button(root, text="🔊 Read Text Aloud", command=read_text, font=("Arial", 12)).pack(pady=10)

# Start GUI
root.mainloop()
