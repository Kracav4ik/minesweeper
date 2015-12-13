from __future__ import division
import pygame


class Cell:
    def __init__(self, is_open, is_bomb):
        self.is_open = is_open
        self.is_bomb = is_bomb


class Grid:
    def __init__(self, width, height, window_size):
        self.width = width
        self.height = height
        window_w, window_h = window_size
        self.pix_w = window_w / width
        self.pix_h = window_h / height
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
                left = x * self.pix_w + 1
                top = y * self.pix_h + 1
                pygame.draw.rect(screen, (192, 0, 0), (left, top, self.pix_w - 2, self.pix_h - 2))
