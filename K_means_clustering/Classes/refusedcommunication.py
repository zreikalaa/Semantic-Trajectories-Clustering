from contextlib import nullcontext

from Classes.event import *
class refusedcommunication(event):
    def __init__(self, level):
        super().__init__()
        self.level=level

    def print(self):
        print(self.level," communication refus -->",end =" ")
        return self.level+" communication refus -->"