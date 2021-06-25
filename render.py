"""
This file renders the board in its current state
"""

from constants import *
import pygame

def draw(cells, ds, z = 1): 
    rects = []
    for i in range(BSIZE):
        for j in range(BSIZE):
            c = BLACK if cells[j][i] == 0 else WHITE
            rects.append(pygame.Rect((i * 20 * z) + 1, (j * 20 * z) + 1, (20 * z) - 2, (20 * z) - 2))
            pygame.draw.rect(ds, c, rects[-1])
    pygame.display.update(rects)
            