# encoding: utf-8

from __future__ import division

import pygame
import sys

from grid import Grid
from screen import Screen

# инициализация
pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (128, 255, 255)  # цвет окна

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)
grid = Grid(20, 10, screen.get_size())


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = screen.convert_to_local(event.pos)
            if event.button == 1:  # left mouse button
                grid.cell_click(pos)
            else:
                grid.mark_cell(pos)
        elif event.type == pygame.MOUSEMOTION:
            pos = screen.convert_to_local(event.pos)
            grid.cell_hover(pos)


def process_game():
    pass


def render():
    """ Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    grid.render(screen)

    pygame.display.flip()


# игровой цикл
while True:
    handle_input()
    process_game()
    render()
