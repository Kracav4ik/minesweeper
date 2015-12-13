from __future__ import division
import random
import pygame

BOMB_COLOR = (192, 0, 0)
EMPTY_COLOR = (0, 192, 0)
UNKNOWN_COLOR = (130, 60, 130)
HOVER_COLOR = (255, 255, 255)
BOMB_COUNT = 30


class Cell:
    is_open = False
    is_bomb = False
    is_marked = False


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
                col.append(Cell())
                coords.append([x, y])
            self.cells.append(col)
        for x, y in random.sample(coords, BOMB_COUNT):
            cell = self.cells[x][y]
            cell.is_bomb = True
        self.font = pygame.font.SysFont('Arial', 70)
        self.flag_font = pygame.font.SysFont('Arial', 30)

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

    def bombs_count(self, x, y):
        count = 0
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if celln.is_bomb:
                count += 1
        return count

    def flags_count(self, x, y):
        count = 0
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if celln.is_marked:
                count += 1
        return count

    def pixels2grid(self, pos):
        pix_x, pix_y = pos
        x = pix_x // self.pix_w
        y = pix_y // self.pix_h
        return [x, y]

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                pix_x = x * self.pix_w + 1
                pix_y = y * self.pix_h + 1
                if not cell.is_open:
                    color = UNKNOWN_COLOR
                elif cell.is_bomb:
                    color = BOMB_COLOR
                else:
                    color = EMPTY_COLOR
                pygame.draw.rect(screen, color, (pix_x, pix_y, self.pix_w - 2, self.pix_h - 2))
                if cell.is_open and not cell.is_bomb:
                    bombs_count = self.bombs_count(x, y)
                    if bombs_count > 0:
                        text_surface = self.font.render(str(bombs_count), False, (0, 0, 0))
                        text_x = pix_x - 1 + self.pix_w // 2 - text_surface.get_width() // 2
                        text_y = pix_y - 1 + self.pix_h // 2 - text_surface.get_height() // 2
                        screen.blit(text_surface, (text_x, text_y))
                if cell.is_marked:
                    text_surface = self.flag_font.render('|>', False, (0, 0, 0))
                    text_x = pix_x - 1 + self.pix_w // 2 - text_surface.get_width() // 2
                    text_y = pix_y - 1 + self.pix_h // 2 - text_surface.get_height() // 2
                    screen.blit(text_surface, (text_x, text_y))

        x, y = self.active_cell
        pix_x = x * self.pix_w
        pix_y = y * self.pix_h
        pygame.draw.rect(screen, HOVER_COLOR, (pix_x, pix_y, self.pix_w, self.pix_h), 3)

    def cell_click(self, pos):
        x, y = self.pixels2grid(pos)
        self.open_cell(x, y)

    def open_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_marked:
            return
        cell.is_open = True
        if not cell.is_bomb and self.bombs_count(x, y) == 0:
            self.open_neighbors(x, y)

    def open_neighbors(self, x, y):
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if not celln.is_open:
                self.open_cell(xn, yn)

    def cell_hover(self, pos):
        x, y = self.pixels2grid(pos)
        self.active_cell = (x, y)

    def mark_cell(self, pos):
        x, y = self.pixels2grid(pos)
        cell = self.cells[x][y]
        if cell.is_open:
            if not cell.is_bomb and self.bombs_count(x, y) == self.flags_count(x, y):
                self.open_neighbors(x, y)
        else:
            cell.is_marked = not cell.is_marked
