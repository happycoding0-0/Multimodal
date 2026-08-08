#src\main.py

# import openwakeword
# from openwakeword.model import Model
from sense.vision  import Eye
from sense.model import Perception
from sense.speech import talk

cam = Eye()
model = Perception()
speech = talk()

frame = cam.cam()
detected = model.vision(frame)
speech.speech(detected)


