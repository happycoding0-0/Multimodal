from sense.path import jarvis_model, jarvis_json
import numpy as np
import sounddevice as sd
from piper import PiperVoice
import wave
import soundfile as sf


voice = PiperVoice.load(model_path=jarvis_model, config_path=jarvis_json)
def tts(text):
    
    a = voice.phonemize(text)
    b = voice.phonemes_to_ids(a)
    c = voice.phoneme_ids_to_audio(b)
    print(a)
    print(b)
    print(c)

    # sd.play(data,fs)
    # sd.wait()

if __name__ == "__main__":

    text = "good morning, sir"
    tts(text)



