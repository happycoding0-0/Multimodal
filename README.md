# Multimodal 프로젝트
> **작성자(Author):** 이지우 (Jeewoo Lee)

인간처럼 보고, 듣고, 말하는 기능을 수행하는 인공지능을 구현하는 프로젝트입니다.

## what is multimodal?
멀티모달은 다양한 형식의 데이터를 연산하여 결과값을 낼수있는 인공지능을 말합니다.

핵심: 다양한 형식의 데이터 연산이 가능한가?



## Plan

``` 
chained pipeline (Current)
[STT]  --> [LLM] --> [TTS] 

[Mic] -bytes-> [Encoder] -array->  [STT] -array-> [Decoder] -text-> [Encoder] -array-> [LLM] -array-> [Decoder]  -text-> [Encoder] -array-> [TTS] -array-> -audio->  

  

[MultiModal Model]
이미지 + 텍스트
오디오 + 이미지


[VAD]
지금 감지된 음성의 청자가 AI 자신인지 판단해야한다. <- 단순 파형 분석 그 이상


[Phsyical computing]
self-awareness : "arm 움직여봐" -> [arm  접속가능여부 탐색]-> [if True: 동작  else: "아직 움직일수없습니다" ]
```

## Todo(할 일)
- 오디오 데이터 누적 방식 재설계







