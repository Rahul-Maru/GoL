import pygame
from pygame import event
from pygame.constants import QUIT
from constants import *
from random import randint
from render import draw

pygame.init()

display_surface = pygame.display.set_mode(AREA)
# img = pygame.image.load(r'C:\\Users\\rahul\Downloads\\tens.png')
cells = [[randint(0, 1) for i in range(BSIZE)] for j in range(BSIZE)]

