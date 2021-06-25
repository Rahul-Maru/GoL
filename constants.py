"""
This file contains a list of variables used by other files.
"""

#Setup
WIDTH = 500
HEIGHT = 500
AREA = (HEIGHT, WIDTH)

#Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Game
# The size of the grid
BSIZE = 25

# The number of neighbors needed for a cell to stay alive
LRANGE = [2,3]

# The number of neighbors needed for a dead cell to respawn
RRANGE = [3]

# A flag for debugging
dbg = 0