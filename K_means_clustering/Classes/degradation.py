from Classes.event import *

class degradation(event):
    def __init__(self,id_event, name_event):
        super().__init__()
        self.id_event=id_event
        self.name_event=name_event
    def print(self):
        print(" degradation: id_degradation: ", self.id_event," -->",end =" ")
        return " D: "+self.name_event.split("#")[-1]+" -->"