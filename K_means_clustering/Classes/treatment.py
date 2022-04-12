from Classes.event import *


class treatment(event):
    def __init__(self, id_event, name_event):
        super().__init__()
        self.id_event = id_event
        self.name_event=name_event

    def print(self):
        print(" treatment: id_process: ", self.id_event,"-->",end =" ")
        return " T: "+str(self.name_event).split("#")[-1]+"-->"