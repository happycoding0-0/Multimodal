# src\sense\speech.py

from kokoro import KModel, KPipeline
import sounddevice as sd
import json
from pathlib import Path

SENSE_DIR = Path(__file__).resolve().parent
path_json = str(SENSE_DIR / "models/path.json") 

with open(path_json, "r",encoding="utf-8") as f:
    path_ = json.load(f)
    # print(path_)
kokoro_model = str(SENSE_DIR / path_["kokoro_model"])
voice_model = str(SENSE_DIR / path_["voice_model"])
kokoro_config = str(SENSE_DIR / path_["kokoro_config"])
#if not path_json or not path_ or not kokoro_model or not voice_model:

class talk():
    
    def __init__(self):
        self.model = KModel(config=kokoro_config, model=kokoro_model)
        self.pipeline = KPipeline(lang_code="b", model=self.model)

        
        
        
    def speech(self,text):
        generator = self.pipeline(text,voice=voice_model)
        for gs,ps,audio in generator:
            print(gs,ps,audio)
        sd.play(audio,samplerate=24000)
        sd.wait()
        
if __name__ == "__main__":
    # print(SENSE_DIR)
    # print(path_json)
    speech = talk()
    speech.speech("This is first")
    speech.speech("This is second")
