#src\main.py

# import openwakeword
# from openwakeword.model import Model
from sense.vision  import Eye
from sense.model import Perception
from sense.speech import talk

cam = Eye()
ai = Perception()
speech = talk()
frame = cam.cam()
detect_result = ai.vision(frame)
print(detect_result)
speech.speech(detect_result)

