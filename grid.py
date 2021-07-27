import sys

from pygame.math import disable_swizzling
from node import Node
import pygame, copy

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.startingPos = (0,0)
        self.endPos = (0,0)
    def repaint(self, screen, height):
        titleFont = pygame.freetype.SysFont('Sans', 32)
        screen.fill((255,255,255))
        for i in range(int(height/15)):
            pygame.draw.line(screen, (0,0,0), (i*15,0), (i*15,height))

        for i in range(int(height/15)):
            pygame.draw.line(screen, (0,0,0), (0,i*15), (height,i*15))

        self.draw(screen)

        title1 = titleFont.get_rect("Pathfinding")
        twidth = title1.width
        theight = title1.height
        title1.center = ((600+(200 - twidth)/2),5)
        titleFont.render_to(screen, title1.center, "Pathfinding", (0,0,0))


        title2 = titleFont.get_rect("Visualization")
        t2width = title2.width
        t2height = title2.height
        title2.center = ((600+(200 - t2width)/2),theight + 10)
        titleFont.render_to(screen, title2.center, "Visualization", (0,0,0))

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


            neighbors = [self.grid[q.pos[0]+1][q.pos[1]],self.grid[q.pos[0]-1][q.pos[1]],self.grid[q.pos[0]][q.pos[1]+1],self.grid[q.pos[0]][q.pos[1]-1], self.grid[q.pos[0]+1][q.pos[1]+1],self.grid[q.pos[0]+1][q.pos[1]-1],self.grid[q.pos[0]-1][q.pos[1]-1],self.grid[q.pos[0]-1][q.pos[1]+1]]
            suc = []
            for i in range(len(neighbors)):
                if(q != None and neighbors[i] not in closed_list and neighbors[i] not in open_list and neighbors[i].active != 1):
                    suc.append(neighbors[i])
            
            for i in range(len(suc)):
                suc[i].parent = q
            
            
            
            for i in range(len(suc)):
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        return [] 
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
                pygame.event.pump()
                suc[i].draw(screen)
                
                
                pygame.time.delay(5)
                pygame.display.update()
                pygame.display.flip()
                if(self.samePos(suc[i], open_list)):
                    continue
            
                if(self.samePos(suc[i], closed_list)):
                    continue
                else:
                    open_list.append(suc[i])



            closed_list.append(q)
        #for i in range(len(closed_list)):
            #pygame.draw.rect(screen, (0,0,255), pygame.Rect((self.decrypt((closed_list[i].pos[0], open_list[i].pos[1])), (15,15))))
    

    def dijkstra(self,diagonals, screen):
        self.grid[self.startingPos[0]][self.startingPos[1]].distance = 0
        spt = []
        endNode = self.grid[self.endPos[0]][self.endPos[1]]
        unexplored = self.copy(self.grid)
        count = 0
        #print(self.grid[self.startingPos[0]][self.startingPos[1]])
        while(len(unexplored) != 0):
            currentNode = self.minDis(unexplored)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return [] 
            try:
                unexplored.remove(currentNode)
            except(ValueError):
                print("could not find path")
                return []
            if(currentNode == endNode):
                
                path = []
                current = currentNode
                count = 0
                path.append(current)
                while (current != self.grid[self.startingPos[0]][self.startingPos[1]]):
                    path.append(current.parent)
                    current = current.parent
                    
                return path[::-1]
        
            
            neighbors = [self.grid[currentNode.pos[0]+1][currentNode.pos[1]],self.grid[currentNode.pos[0]-1][currentNode.pos[1]],self.grid[currentNode.pos[0]][currentNode.pos[1]+1],self.grid[currentNode.pos[0]][currentNode.pos[1]-1]]

            suc = []
            for i in range(len(neighbors)):
                if(currentNode != None and neighbors[i] not in spt and neighbors[i].active != 1 ):
                    suc.append(neighbors[i])
            
            for i in range(len(suc)):
                suc[i].parent = currentNode
            
            for neighbor in unexplored and suc:
                
                weight = 1
                if(currentNode.distance + weight < neighbor.distance):
                    neighbor.distance = (currentNode.distance +  weight)
                    spt.append(neighbor)
                pygame.event.pump()
                neighbor.draw(screen)
                self.draw(screen)
                pygame.display.update()
                pygame.display.flip()
            count +=1
    
    def findMin(self,list1):
        min1 = Node((0,0), None)
        min1.f = 10000
        for i in range(len(list1)):
            if(list1[i].f < min1.f):
                min1 = list1[i]
        return min1

    def minDis(self, list1):
        min1 = Node((0,0), None)
        min1.distance = sys.maxsize
        for i in range(len(list1)):
            if(list1[i].distance < min1.distance):
                
                min1 = list1[i]
        return min1
 
        return min_index
    def samePos(self, suc, list1):
        for i in range(len(list1)):
            if(list1[i].pos == suc.pos):
                if(list1[i].f < suc.f):
                    return True

        return False

    def copy(self, list1):
        return [j for sub in list1 for j in sub]