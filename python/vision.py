'''
vision.py의 단일 역할: 카메라 처리
카메라 -> vision 모델 -> 예측 결과
'''
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


ret, frame = cap.read()
if not ret:
    print("Can't receive frame")
    exit()
frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
cap.release()
from models import model

models = model.AI()
models.vision(data = frame)









