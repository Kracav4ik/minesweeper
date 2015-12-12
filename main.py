from __future__ import division

import pygame
import sys


pygame.init()

window_size = (1280, 720)
window_bg = (128, 255, 255)

screen = pygame.display.set_mode(window_size)


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
    pygame.display.flip()


# main game cycle
while True:
    handle_input()
    process_game()
    render()
