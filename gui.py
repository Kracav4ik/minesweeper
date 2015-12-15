# encoding: utf-8

from __future__ import division
import pygame


class Button:
    def __init__(self, x, y, width, height, click_function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.click = click_function

    def render(self, surface):
        pygame.draw.rect(surface, [0, 0, 255], [self.x, self.y, self.width, self.height])

    def is_inside(self, pos):
        """Возвращает True, если точка pos находится внутри
        """
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
