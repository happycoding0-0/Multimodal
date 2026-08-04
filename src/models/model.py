from ultralytics import YOLO

class AI():
    def __init__(self): 
        
        self.vm = YOLO("./models/yolo26n.pt") # vm= vision model

    def vision(self,data):
        
        result = self.vm(source=data,verbose = False)

        print(result[0].verbose())



        

