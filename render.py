"""
This file renders the board in its current state
"""

from constants import *
import pygame

def draw(cells, ds, z = 1, updateAll = False): 
    rects = []
    for i in range(int(VISIBLE_CELLS/z)):
        for j in range(int(VISIBLE_CELLS/z)):
            c = BLUE if cells[j][i] == 0 else YELLOW
            rects.append(pygame.Rect((i * 20 * z) + 1, (j * 20 * z) + 1, (20 * z) - 2, (20 * z) - 2))
            pygame.draw.rect(ds, c, rects[-1])
    
    if updateAll:
        ds.fill(GRAY)
        pygame.display.update()
    else:
        pygame.display.update(rects)