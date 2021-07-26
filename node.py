import pygame,sys

class Node():
    def __init__(self, parent, pos):
        self.neighbors = [(-1,0),(0,-1),(1,0),(0,1)]
        self.parent = parent
        self.pos = pos
        self.active = 0
        self.g = 0
        self.h = 0
        self.f = 0
        self.distance = sys.maxsize
    def set_parent(self, node):
        self.parent = node
        
    def draw(self, screen):
        #pygame.draw.rect(screen, (int(self.g*3), int(self.h/11), int(self.f/11)),pygame.Rect(self.decrypt(self.pos), (15,15)))
        if(self.distance < 100000):
            pygame.draw.rect(screen, (0, self.distance*3.5,self.distance*3.5),pygame.Rect(self.decrypt(self.pos), (15,15)))
        
        else:
            pygame.draw.rect(screen, (0, 255-int(self.f/11),255- int(self.f/11)),pygame.Rect(self.decrypt(self.pos), (15,15)))
       
    def decrypt(self, pos):
            try:
                return pos[1]*15, pos[0]*15
            except(TypeError):
                return (-15,-15)