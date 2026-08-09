import cv2
from ultralytics import YOLO
from sense.path import yolo_model
class Vision():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = None,None

        self.yolo_model = yolo_model
        self.model = YOLO(model=yolo_model)

    def __del__(self):
        self.cap.release()

    def cam(self):
        self.ret , self.frame = self.cap.read()
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        return self.frame

    def vision(self, frame):
        self.detected = self.model(source=frame,verbose = False)
        return self.detected[0].verbose()

if __name__ == "__main__":
    vs = Vision()
    frame = vs.cam()
    result = vs.vision(frame)
    print(result)

        