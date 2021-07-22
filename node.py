

class Node():
    def __init__(self, pos, parent):
        self.neighbors = [(-1,0),(0,-1),(1,0),(0,1)]
        self.parent = parent
        self.pos = pos
        self.active = 0
        self.g = 0
        self.h = 0
        self.f = 0
    
    