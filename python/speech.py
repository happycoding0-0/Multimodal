import pyttsx3 as tts


def speech(text):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()