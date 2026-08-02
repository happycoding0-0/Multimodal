# MultiModal AI

Vision,Audio(STT,TTS),Thinking(LLM) 3가지 기능을 기존 모델들을 사용하여 완성시키고, 기존 모델에서 직접 만든 모델로 교체하는 방식으로 프로젝트를 진행할 계획.

**Goal**
* 이게 뭐야? -> ** 입니다
* **이 몇개야? -> ** 은 n 개가 보이네요 

1. 무언가를 인식하고 무언가의 이름을 출력 -> 해당 개념: object detection 과 object recognition

2026/07/23 - Vision 기능을 YOLO26모델로 구현해보겠습니다.
> YOLO26 models are pretrained on COCO dataset(COCO = Common Objects in Context). YOLO26 모델들은 COCO 데이터셋을 기반으로 사전학습 되었습니다. (COCO = 생활 속 흔한 객체)

2026/07/25 - 카메라를 opencv 라이브러리를 사용하여 제어하는것이 아닌 라이브러리없이 하는 방식을 구현해보는것을 계획중




프로젝트 동기
사실 이 전에 SAM audio나 메타 AI 글래스를 보면서 이미 이런 방향이 있다는 걸 어렴풋이 알고 있었다. 근데 그때는 일부러 안 보려고 했다 — 내 아이디어가 아니게 될 것 같아서. 지금 생각해보면 비효율적인 고집이었던 것 같다.
현재 사람처럼 보고 듣고 말하는 멀티모달 인공지능을 만들고싶다는생각이 들었으며 , 좀 더 간단한 두가지 기능으로 더 단순화했고 내가 눈을 감고 앞이 보이지않는 상태에서 걸어다닐수도있는 정도의 보조도 할수있도록 만들고싶다는 아이디어가 떠올랐다. 이 아이디어는 밤에 불을 끈 상태에서 야맹증때문인지 앞이 안보여서 세게 부딫힌적이있었는데 시각장애인은 매일이런 느낌이지않을까라는 생각이들었었던적이있어서 이게 아이디어를 만든 원인중 하나라고생각한다


---
참고 자료
https://docs.ultralytics.com/datasets/detect/coco#coco-dataset

https://www.ultralytics.com/glossary/computer-vision-cv#implementing-computer-vision-with-python

https://github.com/ultralytics/ultralytics/tree/main