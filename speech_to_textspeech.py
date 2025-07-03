# Install required libraries first:
# pip install SpeechRecognition
# pip install PyAudio
# pip install pyttsx3

import speech_recognition as sr
import pyttsx3

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Use Microphone as Source
with sr.Microphone() as source:
    print(" Speak something...")

    # Listen to input from microphone
    audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said: ", text)

        # Speak the recognized text
        engine.say(f" {text}")
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Sorry, I could not understand audio")
        engine.say("Sorry, I could not understand what you said.")
        engine.runAndWait()

    except sr.RequestError:
        print("Sorry, my speech service is down")
        engine.say("Sorry, my speech service is currently unavailable.")
        engine.runAndWait()
