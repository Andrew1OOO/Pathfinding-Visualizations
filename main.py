from node import Node
from grid import Grid
import pygame, random
import numpy as np
from pygame.constants import K_d


pygame.init()

HEIGHT = 600
WIDTH = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((255,255,255))
game_over=False
clock = pygame.time.Clock()
pygame.display.set_caption('Searching Visualization')

pygame.draw.line(screen, (0,0,255), (HEIGHT,0), (HEIGHT,HEIGHT))

for i in range(int(HEIGHT/15)):
    pygame.draw.line(screen, (0,0,0), (i*15,0), (i*15,HEIGHT))

for i in range(int(HEIGHT/15)):
    pygame.draw.line(screen, (0,0,0), (0,i*15), (HEIGHT,i*15))





#grid = np.zeros((40,40))

grid = [ ([0] * 40) for row in range(40) ]

for i in range(len(grid)):
    for j in range(len(grid[0])):
        
        grid[i][j] = Node((i,j), None)



grid_2 = Grid(grid)



draw = False
i=0
while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                draw = True
            if event.button == 2:
                pos = pygame.mouse.get_pos()
                grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 2
            if event.button == 3:
                pos = pygame.mouse.get_pos()
                grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 3
                
        if event.type == pygame.MOUSEBUTTONUP:
            draw = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_d:
                grid_2.astar(False,screen)

    if draw:
        pos = pygame.mouse.get_pos()
        try:
            grid_2.grid[grid_2.encrypt(pos)[0]][grid_2.encrypt(pos)[1]].active = 1
        except(TypeError):
            pass
        

    grid_2.draw(screen)

    pygame.display.update()
    pygame.display.flip()


    clock.tick(120)
pygame.quit()
quit()