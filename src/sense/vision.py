# src\sense\vision.py

import cv2 as cv
# from model import Perception
class Eye():
    """
    vision.py의 단일 역할: 카메라 처리
    """
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
    
        return self.frame

    def rasp_cam(self):
        pass
