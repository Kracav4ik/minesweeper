from __future__ import division

import pygame
import sys

from grid import Grid

pygame.init()

WINDOW_SIZE = (1280, 720)
WINDOW_BG_COLOR = (128, 255, 255)

screen = pygame.display.set_mode(WINDOW_SIZE)
grid = Grid(20, 10, WINDOW_SIZE)


def handle_input():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                grid.cell_click(event.pos)
            else:
                grid.mark_cell(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            grid.cell_hover(event.pos)


def process_game():
    pass


def render():
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    grid.render(screen)

    pygame.display.flip()


# main game cycle
while True:
    handle_input()
    process_game()
    render()
