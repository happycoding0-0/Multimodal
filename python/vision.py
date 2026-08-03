from ultralytics import YOLO
import cv2
from speech import speech
#import matplotlib.pyplot as plt


model = YOLO(model ="../models/yolo26n.pt")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() # ret is bool(0 or 1) , frame is latest caputer videoframe
    if not ret:
        break
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = model.predict(source = frame, verbose= False)
    for r in result:
        print(r.verbose())
    break

cap.release()



 # verbose 는 기본 출력 켜기 True 끄기 False
# for r in result:
    
#     print(r.verbose())
    # class_id  = r.boxes.cls.int().tolist()
    # if len(class_id) > 0: # 아무 객체를 인식하지 못했을때 오류 발생(Traceback (most recent call last): IndexError: list index out of range)

    #     name = r.names[class_id[0]]
    #     print(name)
    #     speech("i can see "+name)




