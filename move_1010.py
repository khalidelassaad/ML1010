from shapes_1010 import *

class Move():
    def __init__(self):
        self.col = int()
        self.row = int()
        self.shape = Shape()
    def __str__(self):
    	return "Col:{} Row:{} Shape:{}".format(self.col, self.row, self.shape)
    def __repr__(self):
    	return self.__str__()