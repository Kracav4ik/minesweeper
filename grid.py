# encoding: utf-8

from __future__ import division
import os.path
import random
import pygame


HOVER_COLOR = (255, 255, 255)  # Цвет рамки
BOMB_COUNT = 30  # Кол-во бомб
SEPARATOR = ' x '


# noinspection PyClassHasNoInit
class Cell:
    """Клетка игрового поля,
    is_open -  Открыта ли клетка,
    is_bomb - Есть ли в клетке бомба,
    is_marked - Помечена ли клетка флажком.
    """
    is_open = False
    is_bomb = False
    is_marked = False


class Grid:
    """Игровое поле,
    width - Кол-во ячеек по горизантали
    height - Кол-во ячеек по вертикали
    pix_w - Кол-во пикселей одной ячейки по горизантали
    pix_h - Кол-во пикселей одной ячейки по вертикали
    screen_x, screen_y - Координаты левого верхнего угла игрового поля на экране в пикселах
    screen_width - Ширина игрового поля в пикселах
    screen_height - Высота игрового поля в пикселах
    cells - 2-мерная матрица с ячейками; ячейка с координатоми x, y получается как self.cells[x][y]
    active_cell - Коор-ты активной ячейки т.е. коор-ты ячейки где находится курсор мыши
    font - Шрифт цифр внутри клетки
    flag_texture - Текстура с флагом
    """
    def __init__(self, width, height, screen_x, screen_y, screen_width, screen_height):
        self.width = width
        self.height = height
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pix_w = screen_width // width
        self.pix_h = screen_height // height
        self.cells = []
        self.active_cell = (0, 0)
        self.game_over = False

        # Рисовалка
        self.font = pygame.font.SysFont('Arial', 70)
        self.flag_texture = pygame.image.load(os.path.join('data', 'flag.png'))
        self.bomb_cell_texture = pygame.image.load(os.path.join('data', 'bomb_cell.png'))
        self.empty_cell_texture = pygame.image.load(os.path.join('data', 'empty_cell.png'))
        self.unknown_cell_texture = pygame.image.load(os.path.join('data', 'unknown_cell.png'))

    def free_cells_count(self):
        free_cells = 0
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                if cell.is_open:
                    free_cells += 1
        return free_cells

    def load(self, f):
        lines = f.readlines()
        header = lines[0]
        index = header.find(SEPARATOR)
        w = header[:index]
        h = header[index + len(SEPARATOR):-1]
        self.width = int(w)
        self.height = int(h)

        self.cells = []
        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(Cell())
            self.cells.append(col)

        lines = lines[2:]
        self.game_over = False
        for y in range(self.height):
            row = lines[y]
            elements = row.split(', ')
            for x in range(self.width):
                element = elements[x]
                cell = self.cells[x][y]
                cell.is_bomb = 'b' in element
                cell.is_open = 'o' in element
                cell.is_marked = 'm' in element
                if cell.is_open and cell.is_bomb:
                    self.game_over = True
        self.check_win()

    def check_win(self):
        if self.free_cells_count() == self.height * self.width - BOMB_COUNT:
            self.game_over = True

    def save(self, f):
        f.write('%s%s%s\n\n' % (self.width, SEPARATOR, self.height))
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[x][y]
                f.write('b' if cell.is_bomb else ' ')
                f.write('o' if cell.is_open else ' ')
                f.write('m' if cell.is_marked else ' ')
                if x < self.width - 1:
                    f.write(', ')
            f.write('\n')

    def fill_cells(self, x0, y0):
        """Генератор случайных бомб в пустых клеточках
        Изначально все клеточки без бомб, в список coords записываем все коор-ты всех клеточек
        """

        coords = []
        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(Cell())
                if x0 == x and y0 == y:
                    continue
                coords.append([x, y])
            self.cells.append(col)
        # Случайно выбираем BOMB_COUNT коор-т и ставим в них бомбу
        for x, y in random.sample(coords, BOMB_COUNT):
            cell = self.cells[x][y]
            cell.is_bomb = True

    def good_coords(self, x, y):
        """Возвращает True, если коор-ты х, у которые пренадлежат ячейкам
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x, y):
        """Возврощает список коор-т соседних клеточек
        """
        result = []
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                if xn == x and yn == y:
                    continue
                if self.good_coords(xn, yn):
                    result.append([xn, yn])
        return result

    def bombs_count(self, x, y):
        """Возвращает нужную цифру, в звисимости сколько рядом бомб
        """
        count = 0
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if celln.is_bomb:
                count += 1
        return count

    def flags_count(self, x, y):
        """Возвращает нужную цифру, в звисимости сколько рядом флажков
        """
        count = 0
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if celln.is_marked:
                count += 1
        return count

    def pixels_to_grid(self, pos):
        """Возвращает коор-ты в клетках из переданных коор-т в пикселах
        """
        pix_x, pix_y = pos
        x = pix_x // self.pix_w
        y = pix_y // self.pix_h
        return [x, y]

    def render(self, screen):
        """ Отрисовка игрового поля
        """
        # Рисуем ячейки
        for x in range(self.width):
            for y in range(self.height):
                if self.cells:
                    cell = self.cells[x][y]
                    is_open = cell.is_open
                    is_bomb = cell.is_bomb
                    is_marked = cell.is_marked
                else:
                    is_open = False
                    is_bomb = False
                    is_marked = False

                pix_x = x * self.pix_w + 1
                pix_y = y * self.pix_h + 1
                
                # Переход из локальных коор-т в коор-ты экрана
                pix_x, pix_y = self.convert_to_global(pix_x, pix_y)

                if not is_open:
                    texture = self.unknown_cell_texture
                elif is_bomb:
                    texture = self.bomb_cell_texture
                else:
                    texture = self.empty_cell_texture

                # Рисуем клетку нужной текстурой
                screen.draw_texture(texture, pix_x, pix_y, self.pix_w, self.pix_h)

                # Смотрим кол-во бомб и рисуем цифру кол-во бомб поверх клетки
                if is_open and not is_bomb:
                    bombs_count = self.bombs_count(x, y)
                    if bombs_count > 0:
                        screen.draw_text(str(bombs_count), self.font, (0, 0, 0), pix_x, pix_y, self.pix_w - 2, self.pix_h - 2)

                # Рисуем флажок поверх помеченой клетке
                if is_marked:
                    screen.draw_texture(self.flag_texture, pix_x, pix_y, self.pix_w - 2, self.pix_h - 2)

        # Рисуем рамку поверх активной ячейки
        x, y = self.active_cell
        pix_x = x * self.pix_w
        pix_y = y * self.pix_h
        # Переход из локальных коор-т в коор-ты экрана
        pix_x, pix_y = self.convert_to_global(pix_x, pix_y)
        screen.draw_frame(HOVER_COLOR, pix_x, pix_y, self.pix_w, self.pix_h, 3)

    def convert_to_local(self, pos):
        """Получаем на вход пиксельные коор-ты относительно окна,
        возвращаем пиксельные коор-ты относительно игрового поля
        pos - координаты, список из двух чисел
        """
        x, y = pos
        return [x - self.screen_x, y - self.screen_y]

    def convert_to_global(self, pix_x, pix_y):
        """Получаем на вход пиксельные коор-ты относительно игрового поля,
        возвращаем пиксельные коор-ты относительно окна
        pix_x, pix_y - координаты
        """
        return [(self.screen_x + pix_x), (self.screen_y + pix_y)]

    def cell_click(self, pos):
        """Открывает клетку по которой нажали левой кнопкой мыши
        """
        if self.game_over:
            return
        x, y = self.pixels_to_grid(pos)
        if not self.cells:
            self.fill_cells(x, y)
        if not self.good_coords(x, y):
            return
        self.open_cell(x, y)

    def open_cell(self, x, y):
        """ Открывает клетку в заданных коор-х, если клетка без флажка,
        если рядом с клеткой нет бомб открывает все соседние клетки
        """
        cell = self.cells[x][y]
        if cell.is_marked:
            return
        cell.is_open = True
        if cell.is_bomb:
            # Открыть все ячейки с бомбами
            self.open_bombs()
            self.game_over = True
        if not cell.is_bomb and self.bombs_count(x, y) == 0:
            self.open_neighbors(x, y)
        self.check_win()

    def open_bombs(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[x][y]
                if cell.is_bomb:
                    cell.is_open = True

    def open_neighbors(self, x, y):
        """ Открыть все соседние клетки
        """
        for xn, yn in self.neighbors(x, y):
            celln = self.cells[xn][yn]
            if not celln.is_open:
                self.open_cell(xn, yn)

    def cell_hover(self, pos):
        """Активирует клетку, на которую наведён курсор мыши
        """
        x, y = self.pixels_to_grid(pos)
        if not self.good_coords(x, y):
            return
        self.active_cell = (x, y)

    def mark_cell(self, pos):
        """Ставит / снимает флажок на закрытые клетки,
        для открытых клеток открывает соседние если кол-во флажков соот-ет кол-ву бомб рядом с клеткой
        """
        if self.game_over:
            return
        x, y = self.pixels_to_grid(pos)
        if not self.good_coords(x, y):
            return
        if not self.cells:
            self.fill_cells(x, y)
        cell = self.cells[x][y]
        if cell.is_open:
            if not cell.is_bomb and self.bombs_count(x, y) == self.flags_count(x, y):
                self.open_neighbors(x, y)
        else:
            cell.is_marked = not cell.is_marked
