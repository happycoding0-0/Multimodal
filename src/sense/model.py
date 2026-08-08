# src\sense\model.py

from ultralytics import YOLO
import json
from pathlib import Path 

SENSE_DIR = Path(__file__).resolve().parent
path_json = str(SENSE_DIR / "models/path.json")
with open(path_json, "r", encoding="utf-8") as f:
    path_ = json.load(f)
    # print(path_)



yolo_model = str(SENSE_DIR / path_["yolo_model"])   

class Perception(): 
    """
        #### Perception: Visual Perception, Auditory Perception
    """
    def __init__(self): 
        """

            vm: vision model
        """
        #self.vm = YOLO("./sense/models/yolo26n.pt") # vm= vision model
        #self.vm = YOLO("./models/yolo26n.pt") # vm= vision model
        self.vm = YOLO(yolo_model)

    def vision(self,data):
        """
            #### return: " (count) (object name) ," -> 1 person ,
        """
        result = self.vm(source=data,verbose = False)

        return result[0].verbose()



class Generation():
    """
        Generation: Speech
    """
    pass

# if __name__ == "__main__":
#     ai = Perception()
#     ai.vision()
        

