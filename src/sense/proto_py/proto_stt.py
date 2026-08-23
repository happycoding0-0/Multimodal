
import time

import threading 
import queue
import numpy as np

import pyaudio
from faster_whisper import WhisperModel
from sense.path import faster_whisper_small,model_download_root,vad
import re
import torch
torch.set_num_threads(1)
import torchaudio


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

# STT 모델 불러오기
MODEL =  faster_whisper_small
model = WhisperModel('small',download_root= MODEL,device= "cpu",compute_type="int8") # 모델, 연산 장치(cpu,cuda[gpu]),CPU 상세 설정 ,다운로드 경로, 연산 타입

# VAD 모델 불러오기
torch.hub.set_dir(vad)

vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',model='silero_vad',force_reload=True)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

p = pyaudio.PyAudio()
stream = p.open(rate=RATE,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=CHUNK)

def validate(model,
             inputs: torch.Tensor):
    with torch.no_grad():
        outs = model(inputs)
    return outs

def int2float(sound):
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1/32768
    sound = sound.squeeze()  # depends on the use case
    return sound
num_samples = 512

def stop():
    input("Press Enter to stop the recording:")
    global continue_recording
    continue_recording = False

def producer_thread():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format= pyaudio.paInt16,
        channels= CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer= CHUNK # chunk 가 rate 랑 같다면 한번에 읽을때 1초 분량을 읽는다.
    )
    data = []
    voiced_confidences = []
    
    global continue_recording
    continue_recording = True
    stop_listener = threading.Thread(target=stop)
    stop_listener.start()
    while continue_recording:
    
        audio_chunk = stream.read(num_samples)
    
        # in case you want to save the audio later
        data.append(audio_chunk)
    
        audio_int16 = np.frombuffer(audio_chunk, np.int16);

        audio_float32 = int2float(audio_int16)
    
        # get the confidences and add them to the list to plot them later
        new_confidence = vad_model(torch.from_numpy(audio_float32), 16000).item()
        print(new_confidence)
        voiced_confidences.append(new_confidence)
        if new_confidence > 0.5:
            print("발화 감지")
            stop()
# def consumer_thread():
#     while True:
#         if length_queue.qsize() >= LENGTH_IN_SEC:
#             with length_queue.mutex:
#                 length_queue.queue.clear()
#                 print()

        
#         audio_data = audio_queue.get() # 요소 1개 꺼냄
#         length_queue.put(audio_data) 

#         audio_data_to_process = b""
#         for i in range(length_queue.qsize()):
#             # We index it so it won't get removed
#             audio_data_to_process += length_queue.queue[i]

        
#         # 바이트 -> numpy array (STT 모델이 요구하는 데이터 타입) 변환 해주기
#         audio_data_array: np.ndarray = np.frombuffer(audio_data_to_process,np.int16 ).astype(np.float32) /32768.0 
#         segments , _ = model.transcribe(audio_data_array,
#                                         language=WHISPER_LANGUAGE,
#                                         beam_size=5,
#                                         vad_filter=True,
#                                         vad_parameters=dict(min_silence_duration_ms=500)
#                                         )
#         segments = [s.text for s in segments]
#         transcription = " ".join(segments)
#         transcription = re.sub(r"\[.*\]", "", transcription)
#         transcription = re.sub(r"\(.*\)", "", transcription)
#         transcription = transcription.ljust(MAX_SENTENCE_CHARACTERS," ")
#         print(transcription, end='\r', flush=True)
#         audio_queue.task_done()

if __name__ == "__main__":
    producer_thread()
    # producer = threading.Thread(target= producer_thread,daemon=True)
    # producer.start()

    # consumer = threading.Thread(target= consumer_thread,daemon=True)
    # consumer.start()
    # while True:
        
    #     try:
    #         time.sleep(0.05)
    #     except KeyboardInterrupt:
    #         print("Exiting...")
    #         exit()