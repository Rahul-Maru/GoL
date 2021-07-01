"""
The main file. It runs the logic behind the game
"""

# Importing other files
import math
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT
from pygame.time import Clock
from render import *
from constants import *
import time
import pygame as p

def main(): 
    init()
    draw(cells, display_surface, zoom, relPos, True)

    while True:
        t = time.time()
        changed = update()
        # print('updt:', time.time() - t)

        t = time.time()
        draw(cells, display_surface, zoom, relPos, updateAll, changed)
        # print('draw:', time.time() - t, '\n ----------')

        
    
def init():
    one = [1, 1, 1]
    # cells[100][60:63] = one
    # cells[101][60:63] = one
    # cells[102][60:63] = one

    # cells[10][12:15] = one
    # cells[11][12:15] = one
    # cells[12][12:15] = one

    return cells

def update():
    global cells
    global paused
    global zoom
    global updateAll 
    global clickPos
    global relPos

    changed = []

    clock.tick(30)

    updateAll = False

    if not paused:
        changed = game_loop()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('click at ', event.pos)
            clickPos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            print('release at ', event.pos)
            s = 20 * zoom
            p = ((math.floor(clickPos[0]/s + relPos[0]), math.floor(clickPos[1]/s + relPos[1])),
                (math.floor(event.pos[0]/s + relPos[0]), math.floor(event.pos[1]/s + relPos[1])))
            print(event.pos, clickPos, (event.pos[0]/s, event.pos[1]/s), (clickPos[0]/s, clickPos[1]/s), relPos, p[1], p[0])

            cells[p[0][1]][p[0][0]] = not cells[p[0][1]][p[0][0]]
            if p[0] != p[1]: cells[p[1][1]][p[1][0]] = not cells[p[1][1]][p[1][0]]


        # elif event.type == MOUSEMOTION:
            # print('mouse moved from ', (event.pos[0] - event.rel[0], event.pos[1] - event.rel[1]), ' to ', event.pos)

        elif event.type == pygame.KEYDOWN:
            action = pygame.key.name(event.key).lower()
            if action == 'space':
                paused = not paused

                # print(neighbors(cells, 2, 1))
            elif action == 'z':
                # zoom = zoom
                if event.mod == pygame.KMOD_LSHIFT:
                    zoom = zoom - 0.125 if zoom > 0.25 else 0.25
                else:
                    zoom += 0.125
                print(zoom)
                updateAll = True
                # print('z', updateAll, sep='')
            elif action == 'c':
                # if event.mod == pygame.KMOD_CTRL:
                cells = [[0 for i in range(BSIZE)] for j in range(BSIZE)]
            elif action in ARROWS:
                if action == 'up':
                    if relPos[1] > 0: relPos[1] -= 1 
                elif action == 'down':
                    if relPos[1] < BSIZE - VISIBLE_CELLS/zoom: relPos[1] += 1 
                elif action == 'left':
                    if relPos[0] > 0: relPos[0] -= 1 
                else: 
                    if relPos[0] < BSIZE - VISIBLE_CELLS/zoom: relPos[0] += 1
                print(relPos) 
                # updateAll = True
            else:
                print(action, "is an invalid input")
    return changed

def game_loop():
    t = time.time()
    # print(cells[100][233])
    newCells = resurrect(cells)
    dedCells = kill(cells)
    # print('calc:', time.time() - t)

    for cell in newCells:
        y = cell[0]
        x = cell[1]
        cells[y][x] = 1

    for cell in dedCells:
        y = cell[0]
        x = cell[1]
        cells[y][x] = 0
    
    return newCells + dedCells
    
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
                    if cells[i][j] == 1:
                        # print('if2')
                        lcount += 1
            # print(i,j,lcount,cells[i][j])
            
    return lcount

if __name__ == "__main__":
    p.init()

    flags = pygame.DOUBLEBUF
    display_surface = p.display.set_mode(AREA, flags, 16)
    display_surface.fill(GRAY)

    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    clock = Clock()
    cells = [[1 if i == 0 or j == 0 or i == 299 or j == 299 else 0 for i in range(BSIZE)] for j in range(BSIZE)]
    paused = True
    zoom = 1
    relPos = [230, 0]

    updateAll = False
    clickPos = (0,0)
        
    main()