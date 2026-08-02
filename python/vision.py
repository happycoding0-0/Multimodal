from ultralytics import YOLO
import cv2
import time
from speech import speech
#import matplotlib.pyplot as plt
model = YOLO(model ="../models/yolo26n.pt")
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
     # ret is bool(0 or 1) , frame is latest caputer videoframe
    if not ret:
        break
    #cv2.imshow('test',frame)
    time.sleep(1)
    break

cap.release()
# cv2.destroyAllWindows()
# plt.imshow(frame) ##BGR 확인용
# plt.show()
frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
# plt.imshow(frame) ##RGB 확인용
# plt.show()
result = model.predict(source = frame, verbose= False) # verbose 는 기본 출력 켜기 True 끄기 False
for r in result:
    class_id  = r.boxes.cls.int().tolist()
    name = r.names[class_id[0]]
    print(name)
    speech("i can see "+name)
    
    # for cls_id in class_id:
    #     class_name = r.names[cls_id]
    #     print(class_id,class_name)




