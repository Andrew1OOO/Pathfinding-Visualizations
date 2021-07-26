import sys
from node import Node
from grid import Grid
import pygame, random
import numpy as np
from pygame.constants import K_a, K_d
import pygame.freetype

pygame.init()

HEIGHT = 600
WIDTH = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((255,255,255))
game_over=False
clock = pygame.time.Clock()
pygame.display.set_caption('Searching Visualization')

pygame.draw.line(screen, (0,0,0), (HEIGHT,0), (HEIGHT,HEIGHT))

for i in range(int(HEIGHT/15)):
    pygame.draw.line(screen, (0,0,0), (i*15,0), (i*15,HEIGHT))

for i in range(int(HEIGHT/15)):
    pygame.draw.line(screen, (0,0,0), (0,i*15), (HEIGHT,i*15))





#grid = np.zeros((40,40))

grid = [ ([0] * 40) for row in range(40) ]

for i in range(len(grid)):
    for j in range(len(grid[0])):
        
        grid[i][j] = Node(None, (i,j))



grid_2 = Grid(grid)

for i in range(len(grid_2.grid)):
    for j in range(len(grid_2.grid)):
        if(i == 0 or j == 0 or i == len(grid_2.grid)-1 or j == len(grid_2.grid)-1):
            grid_2.grid[i][j].active = 1
            grid_2.grid[i][j].distance = sys.maxsize

draw = False
i = 0

def clear():
    for i in range(len(grid_2.grid)):
        for j in range(len(grid_2.grid[0])):
            if(grid_2.grid[i][j].active != 1 and grid_2.grid[i][j] != 2 and grid_2.grid[i][j] != 3):
                grid_2.grid[i][j] = Node(None, (i,j))
    grid_2.repaint(screen, 600)
astar = pygame.Rect(650, 300, 100, 40)
dijkstra = pygame.Rect(650, 360, 100, 40)

Font = pygame.freetype.SysFont('Sans', 16)

aDraw = False
dDraw = False
while not game_over:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if(astar.collidepoint(pos)):
                    aDraw = True
                elif(dijkstra.collidepoint(pos)):
                    dDraw = True
                else:
                    draw = True

            if event.button == 2:
                pos = pygame.mouse.get_pos()
                grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 2
            if event.button == 3:
                pos = pygame.mouse.get_pos()
                if(grid_2.encrypt(pos)[0] < 38 and grid_2.encrypt(pos)[0] > 1 and grid_2.encrypt(pos)[1] < 38 and grid_2.encrypt(pos)[1] > 1):
                    grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 3
                else:
                    print("end cannot be on edges")
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            draw = False
            if(astar.collidepoint(pos)):
                apath = grid_2.astar(False,screen)
                for i in range(len(apath)):
                    pygame.draw.rect(screen, (0,0,255), pygame.Rect((grid_2.decrypt(apath[i].pos), (15,15))))
                aDraw = False
            elif(dijkstra.collidepoint(pos)):
                dpath = grid_2.dijkstra(False,screen)
                for i in range(len(dpath)):
                    pygame.draw.rect(screen, (0,0,255), pygame.Rect((grid_2.decrypt(dpath[i].pos), (15,15))))
                dDraw = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_d:
                clear()
                
    if draw:
        pos = pygame.mouse.get_pos()
        try:
            grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 1
        except(TypeError):
            pass

    if(aDraw):
        pygame.draw.rect(screen,(149, 48, 217),astar)
    else:
        pygame.draw.rect(screen,(128, 38, 189),astar)
    if(dDraw):
        pygame.draw.rect(screen,(149, 48, 217),dijkstra)
    else:
        pygame.draw.rect(screen,(128, 38, 189),dijkstra)


    astar_rect = Font.get_rect("A* Search")
    awidth = astar_rect.width
    aheight = astar_rect.height
    astar_rect.center = ((650+(100-awidth)/2),(300+(40-aheight)/2))
    Font.render_to(screen, astar_rect.center, "A* Search", (255,255,255))

    

    drect = Font.get_rect("Dijkstra")
    dwidth = drect.width
    dheight = drect.height
    drect.center = ((650+(100-dwidth)/2),(360+(40-dheight)/2))
    Font.render_to(screen, drect.center, "Dijkstra", (255,255,255))

    grid_2.draw(screen)

    pygame.display.update()
    pygame.display.flip()


    clock.tick(120)
pygame.quit()
quit()