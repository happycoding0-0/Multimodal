# src\sense\speech.py

import pyttsx3 as tts
import time
class talk():
    def __init__(self):
        
        self.engine = tts.init()
        
    def speech(self,text):
        
        if self.engine.isBusy():
                                    print("busy1")
        
        self.engine.say(text)
        if self.engine.isBusy():
                                            print("busy2")
                
        self.engine.runAndWait()
        self.engine.stop()
        if self.engine.isBusy():
                                            print("busy3")
                
        print(text)
        print("끝")


if __name__ == "__main__":
    speech = talk()
    talk().speech("첫번째")
    #speech.speech("첫번째")
    # print("첫번째 완료")
    
    talk().speech("두번째")
    #speech.speech("두번째")
    # print("두번째 완료")
    

        