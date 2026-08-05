# src\sense\model.py

from ultralytics import YOLO

class Perception(): 
    """
        #### Perception: Visual Perception, Auditory Perception
    """
    def __init__(self): 
        """

            vm: vision model
        """
        self.vm = YOLO("./sense/models/yolo26n.pt") # vm= vision model

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
        

