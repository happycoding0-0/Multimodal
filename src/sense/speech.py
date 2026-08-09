# src\sense\speech.py

from kokoro import KModel, KPipeline
import sounddevice as sd
from sense.path import kokoro_model, kokoro_config ,af_heart

class Voice():
    
    def __init__(self):
        self.model = KModel(config=kokoro_config, model=kokoro_model)
        self.pipeline = KPipeline(lang_code="b", model=self.model)
        
        
    def speech(self,text):
        generator = self.pipeline(text,voice=af_heart)
        for gs,ps,audio in generator:
            print(gs,ps,audio)
        sd.play(audio,samplerate=24000)
        sd.wait()
        
if __name__ == "__main__":
    speech = Voice()
    speech.speech("This is first")
    speech.speech("This is second")
