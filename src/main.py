#src\main.py

# import openwakeword
# from openwakeword.model import Model
from sense.vision  import Eye
from sense.model import Perception
from sense.speech import talk

cam = Eye()
ai = Perception()
#speech = talk()

frame = cam.cam()
# frame = Eye.cam()
# frame = Eye().cam()
result = ai.vision(frame)
print(result)
talk().speech(result) 

# detect_result = ai.vision(frame)
# #detect_result = Perception.vision(frame)
# #detect_result = Perception().vision(frame)

# speech.speech(detect_result)
# #talk.speech(detect_result)
# #talk().speech(detect_result)

# #frame2 = Eye().cam()
frame2 = cam.cam()

result = ai.vision(frame2)
print(result)
talk().speech(result) 
# print(detect_result)

cam.cap.release()

