# src\sense\speech.py

import pyttsx3 as tts

class talk():
    def __init__(self):
        
        self.engine = tts.init()
    def speech(self,text):
        self.engine = tts.init()
        print("engine id:", id(self.engine))

        if not text:
            print('fuck')
            exit()
        self.engine.say(text)
        self.engine.runAndWait()
        


if __name__ == "__main__":
    speech = talk()
    speech.speech("첫번째")
    print("첫번째 완료")
    speech.speech("두번째")
    print("두번째 완료")
    

        