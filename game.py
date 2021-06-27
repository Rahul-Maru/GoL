"""
The main file. It runs the logic behind the game
"""

# Importing other files
import random
from pygame import fastevent 
import math

from pygame.constants import MOUSEMOTION, QUIT
from pygame.time import Clock
from render import *
from constants import *
import time
import pygame as p

p.init()
display_surface = p.display.set_mode((500,500))
display_surface.fill(GRAY)

clock = Clock()
cells = [[0 for i in range(BSIZE)] for j in range(BSIZE)]
paused = False
zoom = 1

updateAll = False
mouseDown = False

def main(): 
    init()
    draw(cells, display_surface, zoom, True)

    while True:
        update(cells)
        draw(cells, display_surface, zoom, updateAll)
        if updateAll: print(updateAll)

        
    
def init():
    one = [1, 1, 1]
    cells[10][6:9] = one
    cells[11][6:9] = one
    cells[12][6:9] = one

    cells[10][12:15] = one
    cells[11][12:15] = one
    cells[12][12:15] = one

    return cells

def update(cells):
    global paused
    global zoom
    global updateAll 
    global mouseDown

    clock.tick(30)

    updateAll = False

    if not paused:
        game_loop()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('click at ', event.pos)
            mouseDown = True

        elif event.type == pygame.MOUSEBUTTONUP:
            print('release at ', event.pos)
            mouseDown = False

        elif event.type == MOUSEMOTION:
            print('mouse moved from ', (event.pos[0] - event.rel[0], event.pos[1] - event.rel[1]), ' to ', event.pos, mouseDown)

            if mouseDown:
                s = 20 * zoom
                p = ((math.floor((event.pos[0] - event.rel[0])/s), math.floor((event.pos[1] - event.rel[1])/s)),
                    (math.floor(event.pos[0]/s), math.floor(event.pos[1]/s)))

                cells[p[0][1]][p[0][0]] = not cells[p[0][1]][p[0][0]]
                cells[p[1][1]][p[1][0]] = not cells[p[1][1]][p[1][0]]

                if paused: print('uwu')

        elif event.type == pygame.KEYDOWN:
            action = pygame.key.name(event.key).upper()
            if action == 'SPACE':
                paused = not paused

                # print(neighbors(cells, 2, 1))
            elif action == 'Z':
                # zoom = zoom
                if event.mod == pygame.KMOD_LSHIFT:
                    zoom = zoom - 0.25 if zoom > 0.25 else 0.25
                else:
                    zoom += 0.125
                print(zoom)
                updateAll = True
                print('z', updateAll, sep='')
                
            else:
                print("invalid input")

def game_loop():
    newCells = resurrect(cells)
    dedCells = kill(cells)

    for cell in newCells:
        y = cell[0]
        x = cell[1]
        cells[y][x] = 1

    for cell in dedCells:
        y = cell[0]
        x = cell[1]
        cells[y][x] = 0
    
def resurrect(cells):
    living = []
    for y in range(BSIZE):
        for x in range(BSIZE):
            if cells[y][x] == 0: 
                n = neighbors(cells, y, x)
                if n in RRANGE:
                    living.append((y, x))
    return living

def kill(cells):
    dead = []
    for y in range(BSIZE):
        for x in range(BSIZE):
            if cells[y][x] == 1: 
                l = neighbors(cells, y, x)
                if l not in LRANGE:
                    dead.append((y, x))
    return dead

def neighbors(cells, y, x):
    """Returns how many of the cell at x, y's neighbors are alive."""
    lcount = 0

    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if not ((i < 0 or i >= BSIZE) or (j < 0 or j >= BSIZE)):
                # print('try')
                if not (i == y and j == x):
                    # print('if1')
                    if cells[i][j] == 1:
                        # print('if2')
                        lcount += 1
            # print(i,j,lcount,cells[i][j])
            
    return lcount

if __name__ == "__main__":
    
    main()