from Classes.event import *
from Classes.communication import *
from Classes.treatment import *
from Classes.degradation import *
from Classes.refusedcommunication import *
class trajectory:


    def __init__(self, id_uc, id_events, type_events, communicability, dictionaries, cluster=-1):

        self.events = []
        self.id_uc = id_uc
        self.communicability = communicability
        self.cluster=cluster
        self.old_cluster=-1
        max_low = 2
        max_medium = 5
        for idx, x in enumerate(type_events):
            if x == "treatment":
                self.events.append(treatment("T"+str(id_events[idx]),dictionaries["class name of id "+"T"+str(id_events[idx])]))
            elif x == "degradation":
                self.events.append(degradation("D"+str(id_events[idx]),dictionaries["class name of id "+"D"+str(id_events[idx])]))
            else:
                if id_events[idx] <= max_low:
                    level = "low"
                elif id_events[idx] <= max_medium:
                    level = "medium"
                else:
                    level = "high"
                if x == "refus":
                    self.events.append(refusedcommunication(level))
                elif x == "communication":
                    self.events.append(communication(level))


    def print(self):
        p="["
        print("[",end =" ")
        for event in self.events:
            p+=event.print()
        print("]")
        p+="]"
        return p