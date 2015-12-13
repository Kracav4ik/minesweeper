from __future__ import division


class Cell:
    def __init__(self, is_open, is_bomb):
        self.is_open = is_open
        self.is_bomb = is_bomb


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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



