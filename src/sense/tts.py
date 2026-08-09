

from kokoro import KModel, KPipeline
import sounddevice as sd
from sense.path import kokoro_model, kokoro_config ,bm_daniel

class Tts():
    
    def __init__(self):
        self.model = KModel(config=kokoro_config, model=kokoro_model)
        self.pipeline = KPipeline(lang_code="b", model=self.model)
        
        
    def speak(self,text):
        generator = self.pipeline(text,voice=bm_daniel)
        for gs,ps,audio in generator:
            print(gs,ps,audio)
        sd.play(audio,samplerate=24000)
        sd.wait()
        
if __name__ == "__main__":
    speech = Tts()
    speech.speak("This is first")  
    speech.speak("This is second")
