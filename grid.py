from __future__ import division
import random
import pygame

bomb_color = (192, 0, 0)
empty_color = (0, 192, 0)
unknown_color = (130, 60, 130)
hover_color = (255, 255, 255)
bomb_count = 30


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
        self.active_cell = (0, 0)
        coords = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Cell(False, False))
                coords.append([x, y])
            self.cells.append(col)
        for x, y in random.sample(coords, bomb_count):
            cell = self.cells[x][y]
            cell.is_bomb = True
        self.font = pygame.font.SysFont('Arial', 70)

    def good_coords(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x, y):
        result = []
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                if xn == x and yn == y:
                    continue
                if self.good_coords(xn, yn):
                    result.append([xn, yn])
        return result

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
                if cell.is_open and not cell.is_bomb:
                    bombs_count = 0
                    for xn, yn in self.neighbors(x, y):
                        celln = self.cells[xn][yn]
                        if celln.is_bomb:
                            bombs_count += 1
                    if bombs_count > 0:
                        text_surface = self.font.render(str(bombs_count), False, (0, 0, 0))
                        text_x = pix_x - 1 + self.pix_w // 2 - text_surface.get_width() // 2
                        text_y = pix_y - 1 + self.pix_h // 2 - text_surface.get_height() // 2
                        screen.blit(text_surface, (text_x, text_y))

        x, y = self.active_cell
        pix_x = x * self.pix_w
        pix_y = y * self.pix_h
        pygame.draw.rect(screen, hover_color, (pix_x, pix_y, self.pix_w, self.pix_h), 3)

    def cell_click(self, pos):
        pix_x, pix_y = pos
        x = pix_x // self.pix_w
        y = pix_y // self.pix_h
        cell = self.cells[x][y]
        cell.is_open = True

    def cell_hover(self, pos):
        pix_x, pix_y = pos
        x = pix_x // self.pix_w
        y = pix_y // self.pix_h
        self.active_cell = (x, y)
