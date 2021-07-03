"""
The main file. It runs the logic behind the game
"""

# Importing other files
import math
import pygame
from pygame.constants import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame.time import Clock
from render import *
from constants import *
import sys

class CellsList:
    def __init__(self):
        self.cells = {}

    def has(self, x, y):
        return x in self.cells.get(y, [])

    def set(self, x, y, value = None):
        if value == None:
            value = not self.has(x, y)
        if value:
            row = self.cells.setdefault(y, set())
            if x not in row:
                row.add(x)
        else:
            try:
                self.cells[y].remove(x)
            except KeyError:
                pass
            else:
                if not self.cells[y]:
                    del self.cells[y]

    def __iter__(self):
        for y in self.cells:
            for x in self.cells[y]:
                yield (x, y)

def main(): 
    draw(cells, display_surface, zoom, relPos, True)

    while True:
        update()
        draw(cells, display_surface, zoom, relPos, updateAll)

def update():
    global cells
    global paused
    global zoom
    global updateAll 
    global clickPos
    global relPos
    global dx
    global dy

    changed = []

    clock.tick(12)

    updateAll = False

    if not paused:
        advance()
        pygame.display.set_caption('Game of Life')
    else:
        pygame.display.set_caption('Game of Life (paused)')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            s = 20 * zoom
            p = ((math.floor(clickPos[0]/s + relPos[0]), math.floor(clickPos[1]/s + relPos[1])),
                (math.floor(event.pos[0]/s + relPos[0]), math.floor(event.pos[1]/s + relPos[1])))

            cells.set(p[0][0], p[0][1])
            if p[0] != p[1]: cells.set(p[1][0], p[1][1])

        elif event.type == pygame.KEYDOWN:
            action = pygame.key.name(event.key).lower()
            if action == 'space':
                paused = not paused
            elif action == 'n':
                advance()
            elif action == 'z':
                oldZ = zoom
                if event.mod == pygame.KMOD_LSHIFT:
                    zoom = zoom - 0.125 if zoom > 0.25 else 0.25
                else:
                    zoom += 0.125
                print(zoom)
                updateAll = True
                for i in 0,1: relPos[i] += math.floor((VISIBLE_CELLS/oldZ - VISIBLE_CELLS/zoom)/2)
            elif action == 'c':
                cells = CellsList()
            elif action == 'q' or action == 'escape' or (action == 'w' and event.mod == pygame.KMOD_LCTRL):
                pygame.quit()
                quit()
            elif action in ARROWS:
                if action == 'up':
                    dy -= 1 
                elif action == 'down':
                    dy += 1 
                elif action == 'left':
                    dx -= 1 
                elif action == 'right': 
                    dx += 1
                else:
                    print('wh-wh-wa-hu. wuh-hu-wha? ph-bl-bwhuh?')
                # updateAll = True
            else:
                print(action, "is an invalid input")
        elif event.type == KEYUP:
                action = pygame.key.name(event.key).lower()
                if action in ARROWS:
                    dx = 0 
                    dy = 0
    relPos[0] += dx
    relPos[1] += dy
    # return changed
    
def advance():
    global cells
    """Advances the simulation to the next generation"""
    processed = CellsList()
    newlist = CellsList()
    for cell in cells.__iter__():
        x = cell[0]
        y = cell[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x + i, y + j) in processed:
                    continue
                processed.set(x + i, y + j, True)
                if advance_cell(cells, x + i, y + j):
                    newlist.set(x + i, y + j, True)
    cells = newlist

def advance_cell(cells, x, y):
    """Returns the state of the cell at x, y"""
    lcount = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if cells.has(x + i, y + j): lcount += 1
            
    return True if lcount in (SRANGE if cells.has(x, y) else BRANGE) else False

if __name__ == "__main__":
    pygame.init()

    flags = pygame.DOUBLEBUF
    display_surface = pygame.display.set_mode(AREA, flags, 16)
    display_surface.fill(GRAY)

    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    clock = Clock()
    cells = CellsList()
    # [[1 if i == 0 or j == 0 or i == 299 or j == 299 else 0 for i in range(BSIZE)] for j in range(BSIZE)]
    paused = False
    zoom = 1
    relPos = [0, 0]
    dx = 0
    dy = 0

    updateAll = False
    clickPos = (0,0)

    print('''
Press: arrows to scroll
       space to pause/resume
       n to advance by one generation
       z/shift + z to zoom in/out
       c to clear the grid
       left click to toggle the state of a cell
       Esc/q/ctrl + w to exit''')
        
    main()