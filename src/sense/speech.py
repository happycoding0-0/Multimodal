# src\sense\speech.py

import pyttsx3 as tts
import time
class talk():
    def __init__(self):
        
        self.engine = tts.init()
        
    def speech(self,text):
        #self.engine = tts.init()
        #self.engine = tts.init()
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()


if __name__ == "__main__":
    talk().speech("첫번째")
    talk().speech("두번째")