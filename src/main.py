#src\main.py

# import openwakeword
# from openwakeword.model import Model
from sense.vision  import Vision
from sense.speech import Voice

vs = Vision()
vo = Voice()

frame = vs.cam()
detected = vs.vision(frame)
vo.speech(detected)


