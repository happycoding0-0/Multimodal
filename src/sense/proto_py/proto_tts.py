from sense.path import jarvis_model, jarvis_json
import numpy as np
import sounddevice as sd
from piper import PiperVoice
import wave
import soundfile as sf


voice = PiperVoice.load(model_path=jarvis_model, config_path=jarvis_json)
def tts(text):
    
    with wave.open("re.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    data ,fs=  sf.read('re.wav') # fs=22050
    sd.play(data,fs)
    sd.wait()

if __name__ == "__main__":

    text = "good morning, sir"
    tts(text)



