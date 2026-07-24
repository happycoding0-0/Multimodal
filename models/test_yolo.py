from ultralytics import YOLO

model = YOLO("yolo26n.pt")

model("../data/keyboard1.jpg")