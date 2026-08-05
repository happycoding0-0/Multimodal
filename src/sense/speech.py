# src\sense\speech.py

import pyttsx3 as tts

class talk():
    def __init__(self):
        self.engine = tts.init()
    def speech(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()