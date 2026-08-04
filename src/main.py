import openwakeword
from openwakeword.model import Model
from vision  import Cam
from models.model import AI


cam =  Cam()
frame = cam.cam()

ai = AI()

ai.vision(frame)


