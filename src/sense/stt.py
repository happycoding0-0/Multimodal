

import pyaudio
import numpy as np
from collections import deque
import threading 
from faster_whisper import WhisperModel
from path import model_download_root
import time

model = WhisperModel("base",download_root=model_download_root, compute_type="int8")

p = pyaudio.PyAudio()
stream = p.open(rate=16000,channels=1,format=pyaudio.paInt16, input=True,frames_per_buffer=1024)

q = deque()

q_buffer = deque()


def mic(q):
    while True:
        raw_data = stream.read(num_frames=1024)
        data = np.frombuffer(raw_data,dtype=np.int16)
        q.append(data)
        
        # volume = np.abs(data).mean()
        # print(int(volume))
        # time.sleep(0.05)
def stt(q):

    while True:
        if q:
            if len(q) < 16*2: #  요소 개수 1개 = 1024 ,1024 * 15.625 = 16000 이며 16000 는 1s
                #print(len(q))
                continue
            else:
                #print(len(q))
                tt1 = time.time()
                q_buffer = np.concatenate(q)
                
                q.clear()
                q_buffer = q_buffer.astype(np.float32) / 32768.0
                segments , info = model.transcribe(q_buffer,vad_filter=True)
                for segment in segments:
                    print(segment.text)
                print(time.time() - tt1)
        else:
            print("no q")        
        

if __name__ == "__main__":
    t = threading.Thread(target=mic, args=(q,),daemon=True)
    t.start()
    time.sleep(0.1)
    stt(q)
    stream.close()