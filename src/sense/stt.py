
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



# STT 모델(Whisper) 세팅
WHISPER_LANGUAGE = "en"
WHISPER_THREADS = 4 # 모델이 사용할 cpu 코어(스레드) 개수

# 시각화 (터미널에 출력되는 텍스트)

start = time.time()
# STT 모델 불러오기
MODEL =  faster_whisper_small
model = WhisperModel('small',download_root= MODEL,device= "cuda",compute_type="int8") # 모델, 연산 장치(cpu,cuda[gpu]),CPU 상세 설정 ,다운로드 경로, 연산 타입
print("STT 모델 불러오는데 소요되는 시간:", time.time() - start)

start = time.time()
# VAD 모델 불러오기
torch.hub.set_dir(vad)

vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',model='silero_vad',force_reload=False)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
print("vad 모델 불러오는데 소요되는 시간:", time.time() - start)

# 마이크 입력 데이터 저장할 큐

vad_q = queue.Queue()
stt_q = queue.Queue()

data = []



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
    정수를 소수로
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

def mic_thread():
    """
    마이크 입력 수집
    """
    # pyaudio 객체 초기화(os의 오디오 시스템에 연결)
    p = pyaudio.PyAudio()
    stream = p.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=1024)
    while True:
        vad_raw = stream.read(512)


        vad_q.put(vad_raw)





condition = threading.Condition()
def vad_thread():
        """
        start -> stand by -> end
        1. 인간의 음성인가?
        2.
        """
        global data

        continue_recording = True
        was_speaking = False # 말하는 중이었다
        while continue_recording: 
            with condition:
                audio_int16 = np.frombuffer(vad_q.get(), np.int16); # bytes -> int16

                audio_float32 = int2float(audio_int16) # int16 -> float32

                tensor_input  = torch.from_numpy(audio_float32) # float32 -> Tensor

                new_confidence = validate(model= vad_model, inputs=tensor_input).item() # Tensor -> VAD -> Score (this is voice?) 

                is_speaking = new_confidence > 0.5 # VAD 판단 결과가 0.5이상이면 "말하고 있다"로 상태 변환

                if is_speaking and not was_speaking:  # 발화 시작 감지
                    
                    data = []
                    #print("voice detected")
                    data.append(audio_float32)


                elif is_speaking and was_speaking:# 발화 유지
                    #print("stateful")
                    data.append(audio_float32)

                elif not is_speaking and was_speaking: # 발화 끝 감지
                    was_stopped = True
                    if was_stopped:
                        speak_stopped = time.time()
                    if time.time() - speak_stopped > 0.5:

                        # print("end of speech")
                        data.append(audio_float32)
                        data = np.concatenate(data)
                        condition.notify()
                        
                    else: 
                        data.append(audio_float32)
                        data = np.concatenate(data)
                else : # 발화 시작이 아님 감지 
                    #print("None")
                    pass


                was_speaking = is_speaking

def stt_thread():
    global data
    while True:
        with condition:
            condition.wait()
        print(data.ndim, data.shape)
        start = time.time()
        segments ,info = model.transcribe(data, language= 'ko', beam_size= 1)
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