# MultiModal AI

Vision,Audio(STT,TTS),Thinking(LLM) 3가지 기능을 기존 모델들을 사용하여 완성시키고, 기존 모델에서 직접 만든 모델로 교체하는 방식으로 프로젝트를 진행할 계획.

**Goal**
* 이게 뭐야? -> ** 입니다
* **이 몇개야? -> ** 은 n 개가 보이네요 

1. 무언가를 인식하고 무언가의 이름을 출력 -> 해당 개념: object detection 과 object recognition

2026/07/23 - Vision 기능을 YOLO26모델로 구현해보겠습니다.
> YOLO26 models are pretrained on COCO dataset(COCO = Common Objects in Context). YOLO26 모델들은 COCO 데이터셋을 기반으로 사전학습 되었습니다. (COCO = 생활 속 흔한 객체)

2026/07/25 - 카메라를 opencv 라이브러리를 사용하여 제어하는것이 아닌 라이브러리없이 하는 방식을 구현해보는것을 계획중




---
참고 자료
https://docs.ultralytics.com/datasets/detect/coco#coco-dataset

https://www.ultralytics.com/glossary/computer-vision-cv#implementing-computer-vision-with-python

https://github.com/ultralytics/ultralytics/tree/main