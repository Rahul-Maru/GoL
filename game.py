"""
The main file. It runs the logic behind the game and executes it all
"""

# Importing files
import pygame
import math
import colorama
from pygame.constants import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame.time import Clock
from typing import OrderedDict
from render import *
from constants import *

class CellsList:
    """Class for proccessing the cells"""
    def __init__(self):
        """Basic initialization function for the Cells class"""
        self.cells = {}

    def has(self, x, y):
        """Returns whether the cell at the given coords is in the cells list"""
        return x in self.cells.get(y, [])

    def set(self, x, y, value = None):
        """Changes the value of the cell at the given coords"""
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
        """Basic function to iterate through the cells list"""
        for y in self.cells:
            for x in self.cells[y]:
                yield (x, y)

def main(): 
    """The skeleton of the program."""
    draw(cells, display_surface, zoom, relPos, True)

    while True:
        update()
        draw(cells, display_surface, zoom, relPos, updateAll)

def update():
    """Runs the logic of the code and handles live events"""

    # These lines ensure that when these variables are called, they link to the global ones
    global cells
    global oldCells
    global paused
    global zoom
    global updateAll 
    global titleString
    global clickPos
    global relPos
    global dx
    global dy
    global SRange
    global BRange

    # Keeps the game running under the given fps
    clock.tick(12)

    updateAll = False

    if not paused:
        # The main logic happens here
        advance()

    for event in pygame.event.get():
        # Event handling

        if event.type == QUIT:
            # Quits
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Stores the position where the click occurred for future use
            clickPos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            # Logic for toggling cells on release
            s = 20 * zoom
            p = ((math.floor(clickPos[0]/s + relPos[0]), math.floor(clickPos[1]/s + relPos[1])),
                (math.floor(event.pos[0]/s + relPos[0]), math.floor(event.pos[1]/s + relPos[1])))

            cells.set(p[0][0], p[0][1])
            # Makes sure that we don't double count
            if p[0] != p[1]: cells.set(p[1][0], p[1][1])

            # Updating the saved cells list
            oldCells = cells

        elif event.type == pygame.KEYDOWN:
            # Handles key clicks

            action = pygame.key.name(event.key).lower()
            if action == 'space':
                # Pauses/resumes the game
                paused = not paused
                
                # Changes the caption accordingly
                if paused:
                    pygame.display.set_caption(F"{titleString}, paused)")
                else:
                    pygame.display.set_caption(F"{titleString})")

            elif action == 'r':
                # Prompts the user to change the B/S parameters
                valid = False
                pygame.display.set_caption('Awaiting input')

                # Goes on until a valid input is recieved
                while not valid:
                    BRange = input('How many neighbors should a dead cell have to be born (n1, n2...): ')
                    SRange = input('How many neighbors should a living cell have to survive (n1, n2, ...): ')

                    # Splits, sorts, and removes duplicates from the inputs
                    BRange = list(OrderedDict.fromkeys(BRange.split(', ')))
                    BRange.sort()

                    SRange = list(OrderedDict.fromkeys(SRange.split(', ')))
                    SRange.sort()

                    # Weeding out errors
                    try:
                        for i in range(len(BRange)):
                            if BRange[i] !='': 
                                n = BRange[i] = int(BRange[i])
                                if n > 8 or n <= 0:
                                    raise ValueError
                        for i in range(len(SRange)):
                            if SRange[i] !='': 
                                n = SRange[i] = int(SRange[i])
                                if n > 8 or n < 0:
                                    raise ValueError
    
                    except ValueError:
                        # Red error message!
                        print(colorama.Fore.RED + 'Invalid input')
                        print(colorama.Style.RESET_ALL)
                    else:
                        # If there is no error
                        valid = paused = True

                        titleString = F"Game of Life (B{''.join(map(str, BRange))}/S{''.join(map(str, SRange))}"
                        pygame.display.set_caption(F"{titleString}, paused)")
                        
            elif action == 'n':
                # Advances the simulation by only one generation when paused
                if paused: advance()
            elif action == 'z':
                # Zooms in/out
                oldZ = zoom
                updateAll = True

                if event.mod == pygame.KMOD_LSHIFT:
                    if zoom > 0.375: 
                        zoom -= 0.125  
                    else: updateAll = False
                else:
                    zoom += 0.125

                # Centers the screen on where it was previouly centered, as opposed to zooming in on the top-left
                for i in 0,1: relPos[i] += math.floor((VISIBLE_CELLS/oldZ - VISIBLE_CELLS/zoom)/2)

            elif action == 'c':
                # Kills all the cells
                cells = CellsList()
            
            elif action == 's':
                # Saves the current version of the grid
                oldCells = cells

            elif action == 'b':
                # Resets the grid to the last version
                cells = oldCells

            elif action == 'q' or action == 'escape' or (action == 'w' and event.mod == pygame.KMOD_LCTRL):
                # More quit events
                pygame.quit()
                quit()

            elif action in ARROWS:
                # Handles scrolling
                if action == 'up':
                    dy = -1 
                elif action == 'down':
                    dy = 1 
                elif action == 'left':
                    dx = -1 
                elif action == 'right': 
                    dx = 1
        elif event.type == KEYUP:
            # Only stops scrolling when arrow keys are released
            action = pygame.key.name(event.key).lower()
            if action in ARROWS:
                dx = 0 
                dy = 0
    # Adds the scroll to the relative position
    relPos[0] += dx
    relPos[1] += dy
    
def advance():
    """Advances the simulation to the next generation"""
    global cells
    processed = CellsList()
    newlist = CellsList()

    for cell in cells.__iter__():
        x = cell[0]
        y = cell[1]
        # Goes through all the cells around the living
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Checks if we have looked at this cell before
                if (x + i, y + j) in processed:
                    continue
                processed.set(x + i, y + j, True)

                # If not, we advance it
                if advance_cell(cells, x + i, y + j):
                    newlist.set(x + i, y + j, True)
    # Update our list
    cells = newlist

def advance_cell(cells, x, y):
    """Returns the state of the cell at x, y"""
    lcount = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if cells.has(x + i, y + j): lcount += 1

    # Returns true if the cell is in the right range depending on its current status    
    return True if lcount in (SRange if cells.has(x, y) else BRange) else False

if __name__ == "__main__":
    """Starts the code"""
    # Colorama fixes the color-code issues on windows
    colorama.init()

    # Sets up the display
    pygame.init()
    flags = pygame.DOUBLEBUF
    display_surface = pygame.display.set_mode(AREA, flags, 16)
    display_surface.fill(GRAY)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # Vataible declerations
    clock = Clock()
    cells = CellsList()
    oldCells = CellsList()

    BRange = [3]
    SRange = [2, 3]
    titleString = F"Game of Life (B{''.join(map(str, BRange))}/S{''.join(map(str, SRange))}"
    pygame.display.set_caption(F"{titleString}, paused, check terminal for instructions)")

    updateAll = False
    paused = True
    zoom = 1
    relPos = [0, 0]
    clickPos = (0,0)
    dx = 0
    dy = 0
 
    # Tutorial
    print("\nThe Game of Life, also known simply as Life or \033[1;37;40mGoL, is a cellular automaton devised by the British mathematician John Horton Conway in1970.", end=' ')
    print("It is a zero-player game played on a 2d grid. A zero-player game is one whose evolution is determined by its initial state,")
    print("requiring no further input. One interacts with the Game of Life by creating an initial configuration of 'cells' (squares on the grid")
    print("which can either be alive or dead) and observing how it evolves. There are 2 rules. The birth rule, which states that dead cells with 3 out of", end=' ')
    print("8 neighbors come to life (written as B3), and the Surival rule, which states that any living cell with 2 or 3 live neighbors stays alive (written as S23).")
    print(F"""
        Change the state of a cellby left-clicking on it
        Pause/resume by pressing space
        Zoom in by pressing 'Z'
        Zoom out by pressing 'Shift' + 'Z'
        Scroll by pressing arrow keys
        Load the last saved or changed version of the board by pressing 'B'
        Save the current state of the board by pressing 'S'
        Change the birth and survival rules by pressing 'R'
        Clear the board by pressing 'C'
        Advance the simulation by one generation by pressing 'N'
        Quit the app by clicking the red x, pressing 'Q', 'Escape', or 'Ctrl' + 'W'
        """)
        
    main()