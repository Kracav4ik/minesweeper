from __future__ import division

import pygame
import sys

from grid import Grid

pygame.init()

window_size = (1280, 720)
window_bg = (128, 255, 255)

screen = pygame.display.set_mode(window_size)
grid = Grid(20, 10)


def handle_input():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()


def process_game():
    pass


def render():
    main_screen = pygame.display.get_surface()
    main_screen.fill(window_bg)

    grid.render(screen)

    pygame.display.flip()


# main game cycle
while True:
    handle_input()
    process_game()
    render()
