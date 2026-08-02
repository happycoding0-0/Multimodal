from ultralytics import YOLO

model = YOLO("yolo26n.pt")   

model("../data/keyboard1.jpg")

# 테스트 결과
# 배경이 완전히 깨끗하지않을경우, 정답 객체와 다른 객체의 이름도 함께 출력함.
#