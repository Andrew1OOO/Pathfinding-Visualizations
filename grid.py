
from sre_constants import SUCCESS
from node import Node
import pygame, copy

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.startingPos = (0,0)
        self.endPos = (0,0)
    def draw(self,screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if(self.grid[i][j].active == 1):
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect((self.decrypt((i,j)), (15,15))))
                if(self.grid[i][j].active == 2):
                    pygame.draw.rect(screen, (0,255,0), pygame.Rect((self.decrypt((i,j)), (15,15))))
                    self.startingPos = (i,j)
                if(self.grid[i][j].active == 3):
                    pygame.draw.rect(screen, (255,0,0), pygame.Rect((self.decrypt((i,j)), (15,15))))
                    self.endPos = (i,j)
                if(self.grid[i][j].active ==4):
                    pygame.draw.rect(screen, (0,0,255), pygame.Rect((self.decrypt((i,j)), (15,15))))
    def encrypt(self, position):
        start = (0,0)
        size = 15
        for j in range(1,41):
            for i in range(1,41):
                if position[0] <= (start[0]+size*i) and position[1] <= (start[1] + (size*j)) and position[0] > (start[0]+(size*(i-1)) and position[1] > start[1]+size*(j-1)):
                    return j-1,i-1
    def decrypt(self, pos):
        try:
            return pos[1]*15, pos[0]*15
        except(TypeError):
            return (-15,-15)
    def astar(self, diagonals, screen):
        open_list = [self.grid[self.startingPos[0]][self.startingPos[1]]]

        closed_list = []
        end = False
        count=0
        endNode = self.grid[self.endPos[0]][self.endPos[1]]
        while(len(open_list) > 0):

            q = open_list[0]
            q_i = 0
            for index, item in enumerate(open_list):
                if item.f < q.f:
                    q = item
                    q_i = index
            

            open_list.pop(q_i)           


            neighbors = [self.grid[q.pos[0]+1][q.pos[1]],self.grid[q.pos[0]-1][q.pos[1]],self.grid[q.pos[0]][q.pos[1]+1],self.grid[q.pos[0]][q.pos[1]-1]]
            suc = []
            for i in range(4):
                if(q != None and neighbors[i] not in closed_list and neighbors[i].active != 1):
                    suc.append(neighbors[i])
            
            for i in range(len(suc)):
                suc[i].parent = q

            for i in range(len(suc)):
                if(q == endNode):
                    path = []
                    current = q
                    count = 0
                    path.append(current)
                    while (current.parent != None):
                        path.append(current.parent)
                        current = current.parent
                        count +=1
                    return path[::-1]
                
                    
                suc[i].g = abs(suc[i].pos[0] - self.startingPos[0])+ abs(suc[i].pos[1] - self.startingPos[0] )

                suc[i].h = ((suc[i].pos[0] - self.endPos[0])**2) + ((suc[i].pos[1] - self.endPos[1])**2)

                suc[i].f = suc[i].g + suc[i].h

                if(self.samePos(suc[i], open_list)):
                    continue
            
                if(self.samePos(suc[i], closed_list)):
                    continue
                else:
                    open_list.append(suc[i])



            closed_list.append(q)
        #for i in range(len(closed_list)):
            #pygame.draw.rect(screen, (0,0,255), pygame.Rect((self.decrypt((closed_list[i].pos[0], open_list[i].pos[1])), (15,15))))
    

    
    def findMin(self,list1):
        min1 = Node((0,0), None)
        min1.f = 10000
        for i in range(len(list1)):
            if(list1[i].f < min1.f):
                min1 = list1[i]
        return min1

    def samePos(self, suc, list1):
        for i in range(len(list1)):
            if(list1[i].pos == suc.pos):
                if(list1[i].f < suc.f):
                    return True

        return False