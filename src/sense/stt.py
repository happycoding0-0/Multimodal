
"""      
목표: [WAKE WORD] -> [STT] -> back to [WAKE WORD]
    1. STT 모델을 stream 으로 동작하도록 구현하기. { ASR,기능(function) :Real time transcription, 결과물(output):Real time transcript}
    2.  [WAKE WORD 감지시] -> STT

    
마이크는 공기의 진동을 전기신호로 바꾸는 장치이다.
[공기의 진동(소리)] -> [마이크: 전기신호] -> [ADC:0과 1 디지털 변환] -> [OS/드라이버: 제어 및 전처리] -> [STT 프로그램]
"""


import pyaudio
import numpy as np
from collections import deque
import threading 
from faster_whisper import WhisperModel
from path import model_download_root
import time

import queue
model = WhisperModel("base",download_root=model_download_root, compute_type="int8")

p = pyaudio.PyAudio()
stream = p.open(rate=16000,channels=1,format=pyaudio.paInt16, input=True,frames_per_buffer=1024)

<<<<<<< HEAD
q = queue.Queue()

q_buffer = queue.Queue()
=======
q = deque()
q_buffer = deque()
>>>>>>> b605fd73806b656bd03dc87ade8f973a52ab47a6

def mic(q):
    while True:
        raw_data = stream.read(num_frames=1)
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
                print(time.time() - tt1 )
        else:
            print("no q")        
        

if __name__ == "__main__":
    t = threading.Thread(target=mic, args=(q,),daemon=True)
    t.start()
    
    stt(q)
    stream.close()