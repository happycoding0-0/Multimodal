
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
# audio_queue = queue.Queue()
# length_queue = queue.Queue(maxsize=LENGTH_IN_SEC)

# STT 모델 불러오기
MODEL =  faster_whisper_small
model = WhisperModel('small',download_root= MODEL,device= "cuda",compute_type="int8") # 모델, 연산 장치(cpu,cuda[gpu]),CPU 상세 설정 ,다운로드 경로, 연산 타입

# VAD 모델 불러오기
torch.hub.set_dir(vad)

vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',model='silero_vad',force_reload=False)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

condition = threading.Condition()
# 마이크 입력 데이터 저장할 큐
## mic_q = queue.Queue()
vad_q = queue.Queue()
stt_q = queue.Queue()
#data = np.ndarray(dtype=np.float32)
data = []
def mic_thread():
    """
    ### mic input data producer
    raw(bytes) -> variable(memory) (ex. vad_q & stt_q)
    only read and put
    no preprocessing

    마이크 입력 데이터 생산자
    원시(바이트) -> 변수(메모리) (예시. 음성활동감지_큐 & 음성텍스트변환_큐)

    """
    # pyaudio 객체 초기화(os의 오디오 시스템에 연결)
    p = pyaudio.PyAudio()
    stream = p.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=1024)
    while True:
        vad_raw = stream.read(512)
        # stt_raw = stream.read(1080)
        vad_q.put(vad_raw)

        #stt_q.put(raw)



def stop():
    global continue_recording
    continue_recording = False


def validate(model, inputs: torch.Tensor,sr: int = 16000):
    """ 
    Helper Method: validate()
    torch.no_grad() -> Prevent OOM (Out of Memory) & Speed up computation
    메모리 누수 방지 & 처리 속도 증가
    reference: https://github.com/snakers4/silero-vad/blob/master/examples/pyaudio-streaming/pyaudio-streaming-examples.ipynb
    """
    with torch.no_grad():
        outs = model(inputs,sr)
    return outs

def int2float(sound):
    """ 
    Helper Method: int2float()
    
    int -> float
    VAD가 요구하는 형식으로 변환
    reference: https://github.com/snakers4/silero-vad/blob/master/examples/pyaudio-streaming/pyaudio-streaming-examples.ipynb
    """
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1/32768
    sound = sound.squeeze()  # depends on the use case
    return sound

def vad_thread():
        
        global continue_recording
        continue_recording = True
        global data
        was_speaking = False # 발화 시작 이력 저장
        while continue_recording: 
            with condition:
                audio_int16 = np.frombuffer(vad_q.get(), np.int16); # bytes -> int16

                audio_float32 = int2float(audio_int16) # int16 -> float32

                tensor_input  = torch.from_numpy(audio_float32) # float32 -> Tensor

                new_confidence = validate(model= vad_model, inputs=tensor_input).item() # Tensor -> VAD -> Score (this is voice?) 

                is_speaking = new_confidence > 0.5 # VAD 판단 결과가 0.5이상이면 "말하고 있다"로 상태 변환

                if is_speaking and not was_speaking:  # 발화 시작 감지
                    # 말하고있고 시작 이력이 존재하지않을때 발화시작 출력
                    data = []
                    print("voice detected")
                    data.append(audio_float32)


                elif is_speaking and was_speaking:# 발화 유지
                    # 발화감지 True 및 발화시작이력이 True면 -> 오디오 누적
                    #print("stateful")
                    data.append(audio_float32)





                elif not is_speaking and was_speaking: # 발화 끝 감지
                    #발화감지  False 및 발화시작이력이 True 면 -> 발화가 끝남 -> 오디오 누적 종료 -> stt 변환 -> 변환결과 -> LLM 
                    # 발화 끝 적용
                    print("end of speech")

                    data.append(audio_float32)
                    data = np.concatenate(data)
                    wake_stt = True
                    #print(data.ndim,data.shape)
                    condition.notify()





                else : # 발화 시작이 아님 감지 
                    # not is_speaking and not was_speaking 
                    # 발화감지 False 및 발화시작이력이 False 면 -> 변환 대상이 아님으로 간주 -> 오디오 삭제(현재 (지연발생없는 이상적인 경우 , 현재 요소만 있다고 가정) vad_q 요소 제거)
                    #print("None")
                    pass


                was_speaking = is_speaking

def stt_thread():
    while True:
        with condition:
            
            condition.wait()
        start = time.time()
        audio_data = data.copy()
        print(audio_data.ndim, audio_data.shape)

        segments ,info = model.transcribe(audio_data)
        for segment in segments:

                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        print(time.time() - start)


if __name__ == "__main__":

    mic = threading.Thread(target= mic_thread,daemon=True)
    mic.start()
    stt = threading.Thread(target= stt_thread, daemon= True)
    stt.start()
    vad= threading.Thread(target=vad_thread,daemon=True)
    vad.start()

    while True:
        try:
            time.sleep(0.05)
        except KeyboardInterrupt:
            print("Exiting...")
            exit()