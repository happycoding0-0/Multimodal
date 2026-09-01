# Multimodal 프로젝트
> **작성자(Author):** 이지우 (Jeewoo Lee)

## 로컬 AI 시스템(플러그인 방식)


### 프로젝트 비전
인간처럼 보고, 듣고, 말하는 기능부터 실제 현실세계에서 물리적 기능을 수행하는 인공지능을 구현하는 프로젝트입니다.

### Project Vision
initiative to realize embodied AI that interacts physically with the real world, expanding from core human-like modalities such as sight, sound, and speech.

( 'Embodied AI' is the technical term for AI that interacts with the physical world, like robots).

## what is multimodal?
멀티모달은 다양한 형식의 데이터를 연산하여 결과값을 낼수있는 인공지능을 말합니다.

핵심: 다양한 형식의 데이터 연산이 가능한가?



## Plan

``` 
chained pipeline (Current) - it's not multimodal
[STT]  --> [LLM] --> [TTS] 

[Mic] -bytes-> [Encoder] -array->  [STT] -array-> [Decoder] -text-> [Encoder] -array-> [LLM] -array-> [Decoder]  -text-> [Encoder] -array-> [TTS] -array-> -audio->  

  



[VAD]
지금 감지된 음성의 청자가 AI 자신인지 판단해야한다. <- 단순 파형 분석 그 이상



[GUI]
plugin panel -> model selection

[MultiModal Model]

[Phsyical computing]
self-awareness : "arm 움직여봐" -> [arm  접속가능여부 탐색]-> [if True: 동작  else: "아직 움직일수없습니다" ]

- AI가 각종 제어 가능한 대상을 탐색(사용자 입력에 맞는 대상등등)
- 제어가능한 대상을 이해 (무엇을 어떻게 할수있는지등등)
- 제어가능한 대상을  전기신호로 제어 할수있도록 설계

human -> code -> control(servo, robot....)
AI -> 0,1(Electronic,raw) -> control(servo, robot....)
```

## Todo(할 일)
- 오디오 데이터 누적 방식 재설계







