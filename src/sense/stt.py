import time

import threading
import queue
import numpy as np

import pyaudio
from faster_whisper import WhisperModel
from sense.path import faster_whisper_small, model_download_root, vad
import re
import torch

torch.set_num_threads(1)
import torchaudio


# STT 모델(Whisper) 세팅
WHISPER_LANGUAGE = "en"
WHISPER_THREADS = 4  # 모델이 사용할 cpu 코어(스레드) 개수


# ============================================================
# 지연 측정용 공유 변수
# ============================================================

# VAD가 발화 종료를 감지한 시각
t_vad_end = None

# VAD thread가 STT thread에 notify한 시각
t_notify = None


# ============================================================
# STT 모델 로딩
# ============================================================

start = time.time()

MODEL = faster_whisper_small
model = WhisperModel(
    'small',
    download_root=MODEL,
    device="cuda",
    compute_type="int8"
)

print("STT 모델 불러오는데 소요되는 시간:", time.time() - start)


# ============================================================
# VAD 모델 로딩
# ============================================================

start = time.time()

torch.hub.set_dir(vad)

vad_model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)

(
    get_speech_timestamps,
    save_audio,
    read_audio,
    VADIterator,
    collect_chunks
) = utils

print("vad 모델 불러오는데 소요되는 시간:", time.time() - start)


# ============================================================
# Queue / 공유 데이터
# ============================================================

vad_q = queue.Queue()
stt_q = queue.Queue()



def validate(model, inputs: torch.Tensor, sr: int = 16000):
    """
    Helper Method: validate()

    torch.no_grad() -> Prevent OOM (Out of Memory)
    & Speed up computation
    """
    with torch.no_grad():
        outs = model(inputs, sr)

    return outs


def int2float(sound):
    """
    int16 -> float32
    VAD가 요구하는 형식으로 변환
    """

    abs_max = np.abs(sound).max()

    sound = sound.astype('float32')

    if abs_max > 0:
        sound *= 1 / 32768

    sound = sound.squeeze()

    return sound


# ============================================================
# MIC THREAD
# ============================================================

def mic_thread():
    """
    마이크 입력 수집
    """

    p = pyaudio.PyAudio()

    stream = p.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=1024
    )

    while True:

        vad_raw = stream.read(512)

        vad_q.put(vad_raw)


# ============================================================
# Condition
# ============================================================

# condition = threading.Condition()

# ============================================================
# VAD THREAD
# ============================================================

def vad_thread():
    global t_vad_end
    global t_notify

    continue_recording = True

    # 현재 발화 데이터를 수집하고 있는가
    recording = False

    # 무음이 처음 감지된 시각
    silence_started_at = None
    data = []

    while continue_recording:
        # with condition:
            audio_int16 = np.frombuffer(
                vad_q.get(),
                np.int16
            )

            audio_float32 = int2float(audio_int16)
            tensor_input = torch.from_numpy(audio_float32)

            new_confidence = validate(
                model=vad_model,
                inputs=tensor_input
            ).item()

            is_speaking = new_confidence > 0.5

            # ==================================================
            # 1. 음성이 감지됨
            # ==================================================
            if is_speaking:

                # 새로운 발화 시작
                if not recording:
                    recording = True
                    data = []

                    print("[VAD] voice detected")

                data.append(audio_float32)

                # 잠깐 무음이었다가 다시 말한 경우
                # 발화 종료를 취소
                silence_started_at = None

            # ==================================================
            # 2. 무음
            # ==================================================
            else:

                # 현재 발화를 수집 중인 경우에만 처리
                if recording:

                    data.append(audio_float32)

                    # ------------------------------------------
                    # 무음이 처음 나타난 순간
                    # ------------------------------------------
                    if silence_started_at is None:

                        silence_started_at = time.perf_counter()

                        print(
                            f"[VAD] silence started : "
                            f"{silence_started_at:.6f}"
                        )

                    # ------------------------------------------
                    # 현재까지의 연속 무음 길이
                    # ------------------------------------------
                    silence_duration = (
                        time.perf_counter()
                        - silence_started_at
                    )

                    # ------------------------------------------
                    # 0.5초 이상 무음이면 발화 종료 확정
                    # ------------------------------------------
                    if silence_duration >= 0.5:

                        t_vad_end = time.perf_counter()

                        print(
                            f"[VAD] end of speech   : "
                            f"{t_vad_end:.6f}"
                        )

                        print(
                            f"[LATENCY] SILENCE -> VAD_END: "
                            f"{t_vad_end - silence_started_at:.6f}s"
                        )

                        # list -> 하나의 numpy array
                        stt_q.put(np.concatenate(data))

                        t_notify = time.perf_counter()

                        print(
                            f"[TIMING] notify()      : "
                            f"{t_notify:.6f}"
                        )

                        print(
                            f"[LATENCY] VAD_END -> NOTIFY: "
                            f"{t_notify - t_vad_end:.6f}s"
                        )

                        # condition.notify()

                        # 다음 발화를 위한 상태 초기화
                        recording = False
                        silence_started_at = None


# ============================================================
# STT THREAD
# ============================================================

def stt_thread():
    while True:

        # condition.wait() 대신
        # 처리할 발화를 Queue에서 가져오기
        audio = stt_q.get()

        print(audio.ndim, audio.shape)

        segments, info = model.transcribe(
            audio,
            language='ko',
            beam_size=1
        )
        for segment in segments:
            print(segment.text)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    mic = threading.Thread(
        target=mic_thread,
        daemon=True
    )
    mic.start()

    stt = threading.Thread(
        target=stt_thread,
        daemon=True
    )
    stt.start()

    vad = threading.Thread(
        target=vad_thread,
        daemon=True
    )
    vad.start()

    while True:

        try:
            time.sleep(0.05)

        except KeyboardInterrupt:

            print("Exiting...")
            exit()