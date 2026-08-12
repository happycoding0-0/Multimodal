
from path import model_download_root
import sounddevice as sd
import openwakeword 
from openwakeword.model import Model
import pyaudio
import time
import threading
from faster_whisper import WhisperModel
import numpy as np

from collections import deque


class Listener:
    def __init__(self):
        self.SAMPLE_RATE =  16000
        self.CHUNK_SIZE = 1280
        self.FORMAT = pyaudio.paInt16
        self.p = pyaudio.PyAudio()
    
        self.stream = self.p.open(format = self.FORMAT, channels= 1, rate = self.SAMPLE_RATE, input=True , frames_per_buffer=self.CHUNK_SIZE)

    def mic_data(self,queue):
        while True:
            raw_data = self.stream.read(self.CHUNK_SIZE)
            data = np.frombuffer(raw_data,dtype=np.int16)
            queue.append(data)
            time.sleep(0.05)
            


class Stt():

    def __init__(self):
        self.is_running = True
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = 1280
        self.mic_queue = deque()
        
        # openwakeword.utils.download_models(target_directory=f"{model_download_root}/openwakeword_models")
        self.wakeword_model = Model(
            wakeword_models=[f"{model_download_root}/openwakeword_models/hey_jarvis_v0.1.onnx"],
            melspec_model_path=f"{model_download_root}/openwakeword_models/melspectrogram.onnx",
            embedding_model_path=f"{model_download_root}/openwakeword_models/embedding_model.onnx",
            inference_framework="onnx"
            )
        self.faster_whisper_model = WhisperModel("small",download_root= model_download_root,compute_type="int8")

    def wake_word(self,queue):
            print("Wake Word is Listening...")
            while True:
                if  queue:
                    self.prediction = self.wakeword_model.predict( queue.popleft())
                    for wake_word , score in self.prediction.items():
                        if score >= 0.5:
                            print(wake_word, score)

                            return
                        else:
                            print("failed: ",wake_word,float(score))
     
                    
        
        

    def stt(self,queue):        
        
        while True:
                time.sleep(0.05)
                
                audio = np.concatenate(queue)
                
                
                queue.clear()
                
                 
                segments , info = self.faster_whisper_model.transcribe(language="ko",audio = audio,beam_size=5)
                   
                for segment in segments:
                    print("STT: ","[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        
        

if __name__ == "__main__":
    
    listener = Listener()
    stt = Stt()
    t1 = threading.Thread(target=listener.mic_data, args=(stt.mic_queue,), daemon=True)
    t1.start()
    stt.stt(stt.mic_queue)
    while True:
        print("???")
        time.sleep(10)
    

    