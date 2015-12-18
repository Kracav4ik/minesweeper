# encoding: utf-8

from __future__ import division

import pygame
import sys
import os.path

from grid import Grid
from gui import Button
from screen import Screen

# инициализация
SAVE_FILE = 'save_data'
pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (128, 255, 255)  # цвет окна

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)


def create_grid():
    global grid
    grid = Grid(20, 10, 40, 90, 1200, 600)

create_grid()


def save_grid():
    global grid
    f = open(SAVE_FILE, 'w')
    grid.save(f)
    f.close()


def load_grid():
    global grid
    if os.path.exists(SAVE_FILE):
        f = open(SAVE_FILE, 'r')
        grid.load(f)
        f.close()


save_game_button = Button(640, 5, 200, 50, 'Save game', save_grid)
load_game_button = Button(430, 5, 200, 50, 'Load game', load_grid)
new_game_button = Button(10, 5, 200, 50, 'New game', create_grid)
exit_button = Button(220, 5, 200, 50, 'Exit!', sys.exit)

buttons = [new_game_button, exit_button, load_game_button, save_game_button]


def get_button(pos):
    for button in buttons:
        if button.is_inside(pos):
            return button


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button = get_button(event.pos)
            if button is not None:
                button.click()
            else:
                pos = grid.convert_to_local(event.pos)
                if event.button == 1:  # left mouse button
                    grid.cell_click(pos)
                else:
                    grid.mark_cell(pos)
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.on_mouse_move(event.pos)
            pos = grid.convert_to_local(event.pos)
            grid.cell_hover(pos)


def process_game():
    pass


def render():
    """ Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    grid.render(screen)
    for button in buttons:
        button.render(screen)

    pygame.display.flip()


# игровой цикл
while True:
    handle_input()
    process_game()
    render()
