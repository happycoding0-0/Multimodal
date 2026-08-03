'''
vision.py의 단일 역할: 카메라 처리
카메라 -> vision 모델 -> 예측 결과

'''
import cv2 as cv
from models import model
class Cam():
    def __init__(self):
        self.ret = None
        self.frame = None
        self.cap = cv.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        

    def cam(self):
        self.ret, self.frame = self.cap.read()
        if not self.ret:
            print("Can't receive frame")
            exit()
        self.frame = cv.cvtColor(self.frame,cv.COLOR_BGR2RGB)
        self.cap.release()
        # models = model.AI()
        # models.vision(data = frame)
        return self.frame

# (.venv) PS C:\AI\multimodal\python> python main.py              
# Traceback (most recent call last):
#   File "C:\AI\multimodal\python\main.py", line 7, in <module>
#     frame = Cam.cam()
#             ^^^^^^^^^
# TypeError: Cam.cam() missing 1 required positional argument: 'self'