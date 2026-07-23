from ultralytics import YOLO

model = YOLO("yolo26n.pt")

model("C:/AI/multimodal/data/keyboard1.jpg")