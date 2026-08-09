# src\sense\model.py

from ultralytics import YOLO
import json

from pathlib import Path 

import cv2
from kokoro import KModel,KPipeline
import sounddevice as sd

SENSE_DIR = Path(__file__).resolve().parent


path_json = str(SENSE_DIR / "models/path.json")

with open(path_json, "r", encoding="utf-8") as f:
    path_ = json.load(f)
    # print(path_)


# path : vision model 
yolo_model = str(SENSE_DIR / path_["yolo_model"]) 

# path : speech model(tts, text to speech)
kokoro_model = str(SENSE_DIR / path_["kokoro_model"])
kokoro_config = str(SENSE_DIR / path_["kokoro_config"])
kokoro_voice_model = str(SENSE_DIR / path_["kokoro_voice_model"])

class Vision(): 
    """
        #### Perception: Visual Perception, Auditory Perception
    """
    def __init__(self): 
        """
            Vision 클래스 초기 실행
            vm: vision model
            컴퓨터 비전 모델
            카메라 장치 준비
        """

        # 컴퓨터 비전 관련
        self.vm = YOLO(yolo_model)

        # 카메라 관련
        self.cap = cv2.VideoCapture(0)
        self.ret ,self.frame = None,None

    def cam(self):
        """
         카메라 열어서 프레임 한 장 변수에 로드
         ### return: frame 
        """
        self.ret,self.frame = self.cap.read()
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

        return self.frame

    def vision(self,frame):
        """
            yolo 모델 frame 분석
            ### return: " (count) (object name) ," -> 1 person ,
        """
        result = self.vm(source=frame,verbose = False)
        text = result[0].verbose()
        return text



class Generation():
    """
        Generation: talk
    """
    def __init__(self):
        self.model = KModel(config=kokoro_config,model=kokoro_model)
        self.pipeline = KPipeline(lang_code="b",model=self.model)

    def talk(self,text):
        """
        text를 받아 tts 가 오디오를 출력
        """
        talk = self.pipeline(text,voice=kokoro_voice_model)
        for gs,ps,audio in talk:
            print(audio)
        sd.play(audio,samplerate=24000)
        sd.wait()
         
         
if __name__ == "__main__":
    vs = Vision()
    sp = Generation()
    frame = vs.cam()
    detected = vs.vision(frame)
    talk = sp.talk(detected)
