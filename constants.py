"""
This file contains a list of variables used by other files.
"""

#Setup
WIDTH = 625
HEIGHT = 625
AREA = (HEIGHT, WIDTH)

#Colors
# Neutral colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

#Color wheel, 3 degrees
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

#Game
# The size of the grid
BSIZE = max(WIDTH, HEIGHT)

# The number of visible cells with default zoom
VISIBLE_CELLS = BSIZE/20

# The number of neighbors needed for a cell to stay alive
LRANGE = [2,3]

# The number of neighbors needed for a dead cell to respawn
RRANGE = [3]

# A flag for debugging
dbg = 0