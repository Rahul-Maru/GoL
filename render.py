"""
This file renders the board in its current state
"""

from constants import *
import pygame

def draw(cells, ds, z = 1, relPos = (0, 0), updateAll = False, changed = ['rickroll']): 
    # print(relPos)
    # if changed == ['rickroll']: 
    #     for i in range(BSIZE):
    #         for j in range (BSIZE):
    #             changed.append([j, i])
    rects = []
    for x in range(relPos[0], int(VISIBLE_CELLS/z) + relPos[0]):
        for y in range(relPos[1], int(VISIBLE_CELLS/z) + relPos[1]):
            try:
                c = LIVE_COLOR if cells.has(x, y) else DEAD_COLOR
            except IndexError:
                print(x, y, VISIBLE_CELLS/z)
                raise IndexError
            # if [j, i] in changed: 
            rects.append(pygame.Rect(((x - relPos[0]) * 20 * z) + 1, ((y - relPos[1]) * 20 * z) + 1, (20 * z) - 2, (20 * z) - 2))
            try:
                pygame.draw.rect(ds, c, rects[-1])
            except:
                continue
    
    if updateAll:
        ds.fill(BG_COLOR)
        pygame.display.update()
    else:
        pygame.display.update(rects)