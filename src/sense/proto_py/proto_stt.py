
import time

import threading 
import queue
import numpy as np

import pyaudio
from faster_whisper import WhisperModel
from sense.path import faster_whisper_small
import re

# 오디오 세팅
STEP_IN_SEC : int = 1 # 마이크 입력 데이터를  STEP_IN_SEC 만큼 끊어서 넣는다
LENGTH_IN_SEC : int = 10 # 한번에 묶어서 모델에 전달할 최대 오디오 길이는 LENGTH_IN_SEC
CHANNELS = 1

RATE = 16000
CHUNK  = RATE

# STT 모델(Whisper) 세팅
WHISPER_LANGUAGE = "en"
WHISPER_THREADS = 4 # 모델이 사용할 cpu 코어(스레드) 개수

# 시각화 (터미널에 출력되는 텍스트)
MAX_SENTENCE_CHARACTERS = 80
# queue: 모든 1초 길이의 오디오 청크가 담겨짐
audio_queue = queue.Queue()

length_queue = queue.Queue(maxsize=LENGTH_IN_SEC)

# 모델 불러오기
MODEL =  faster_whisper_small
model = WhisperModel(MODEL,device= "cuda",compute_type="int8") # 모델, 연산 장치(cpu,cuda[gpu]),CPU 상세 설정 ,다운로드 경로, 연산 타입



p = pyaudio.PyAudio()
stream = p.open(rate=RATE,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=CHUNK)


def producer_thread():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format= pyaudio.paInt16,
        channels= CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer= CHUNK # chunk 가 rate 랑 같다면 한번에 읽을때 1초 분량을 읽는다.
    )
    print("-"*80)
    print("마이크 초기화됨, 녹음 시작....")
    print("-"*80)
    print("TRANSCRIPTION") # TRANSCRIPTION (음성 전사:음성을 텍스트로 변환하는 작업
    print("-"*80)

    while True:
        audio_data = b""
        for _ in range(STEP_IN_SEC):
            chunk = stream.read(RATE) # 1초 분량의 오디오 데이터를 읽음
            audio_data += chunk # 데이터를 이어붙임, 반복횟수만큼 분량을 이어 붙일수있음. (예: b"AAAA" += b"BBBB" = b"AAAABBBB")
        audio_queue.put(audio_data)

def consumer_thread():
    while True:
        if length_queue.qsize() >= LENGTH_IN_SEC:
            with length_queue.mutex:
                length_queue.queue.clear()
                print()

        
        audio_data = audio_queue.get() # 요소 1개 꺼냄
        length_queue.put(audio_data) 

        audio_data_to_process = b""
        for i in range(length_queue.qsize()):
            # We index it so it won't get removed
            audio_data_to_process += length_queue.queue[i]

        
        # 바이트 -> numpy array (STT 모델이 요구하는 데이터 타입) 변환 해주기
        audio_data_array: np.ndarray = np.frombuffer(audio_data_to_process,np.int16 ).astype(np.float32) /32768.0 
        segments , _ = model.transcribe(audio_data_array,
                                        language=WHISPER_LANGUAGE,
                                        beam_size=5,
                                        vad_filter=True,
                                        vad_parameters=dict(min_silence_duration_ms=500)
                                        )
        segments = [s.text for s in segments]
        transcription = " ".join(segments)
        transcription = re.sub(r"\[.*\]", "", transcription)
        transcription = re.sub(r"\(.*\)", "", transcription)
        transcription = transcription.ljust(MAX_SENTENCE_CHARACTERS," ")
        print(transcription, end='\r', flush=True)
        audio_queue.task_done()

if __name__ == "__main__":
    producer = threading.Thread(target= producer_thread,daemon=True)
    producer.start()

    consumer = threading.Thread(target= consumer_thread,daemon=True)
    consumer.start()
    while True:
        
        try:
            time.sleep(0.05)
        except KeyboardInterrupt:
            print("Exiting...")
            exit()