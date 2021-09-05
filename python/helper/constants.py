"""
This file contains a list of variables used by other files.
"""
#Setup
WIDTH = 720
HEIGHT = WIDTH
AREA = (HEIGHT, WIDTH)

#Keys
ARROWS = ['up', 'down', 'left', 'right']

#Colors
# Neutral colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

#Color wheel, 2 degrees
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
GOLD = (255, 180, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
MAGENTA = (255, 0, 255)

BG_COLOR = BLACK
DEAD_COLOR = DARK_BLUE
LIVE_COLOR = GOLD

#Game
# The number of visible cells with default zoom
VISIBLE_CELLS = int(max(WIDTH,HEIGHT)/20 + 2)
