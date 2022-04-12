from Classes.event import *

class communication(event):


    def __init__(self, level):
        super().__init__()
        self.level = level


    def print(self):
        print(self.level," communication --->",end =" ")
        return self.level+" communication --->"