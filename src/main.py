#src\main.py

# import openwakeword
# from openwakeword.model import Model
from sense.vision  import Vision
from sense.tts import Tts

vs = Vision()
tts = Tts()

frame = vs.cam()
detected = vs.vision(frame)
tts.speak(detected)


