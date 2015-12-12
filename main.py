from __future__ import division

import pygame
import sys


pygame.init()

window_size = (1280, 720)

screen = pygame.display.set_mode(window_size)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
