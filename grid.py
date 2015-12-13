from __future__ import division
import pygame

bomb_color = (192, 0, 0)
empty_color = (0, 192, 0)
unknown_color = (130, 60, 130)


class Cell:
    def __init__(self, is_open, is_bomb):
        self.is_open = is_open
        self.is_bomb = is_bomb


class Grid:
    def __init__(self, width, height, window_size):
        self.width = width
        self.height = height
        window_w, window_h = window_size
        self.pix_w = window_w // width
        self.pix_h = window_h // height
        self.cells = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Cell(False, False))
            self.cells.append(col)

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                pix_x = x * self.pix_w + 1
                pix_y = y * self.pix_h + 1
                if not cell.is_open:
                    color = unknown_color
                elif cell.is_bomb:
                    color = bomb_color
                else:
                    color = empty_color
                pygame.draw.rect(screen, color, (pix_x, pix_y, self.pix_w - 2, self.pix_h - 2))

    def cell_click(self, pos):
        pix_x, pix_y = pos
        x = pix_x // self.pix_w
        y = pix_y // self.pix_h
        cell = self.cells[x][y]
        cell.is_open = True
