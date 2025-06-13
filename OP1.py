import pyttsx3

# Create the engine
speaker = pyttsx3.init()

# Ask user for text input
text = input("Text to Speech: ")
# Speak the text
speaker.say(text)
speaker.runAndWait()

