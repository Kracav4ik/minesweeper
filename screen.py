from __future__ import division
import pygame


class Screen:
    def __init__(self, surface):
        self.surface = surface
        self.offset_y = 60

    def get_size(self,):
        width, height = self.surface.get_size()
        return width, height - self.offset_y

    def draw_rect(self, color, pix_x, pix_y, pix_w, pix_h):
        pygame.draw.rect(self.surface, color, (pix_x, pix_y + self.offset_y, pix_w, pix_h))

    def draw_text(self, text, font, color, pix_x, pix_y, pix_w, pix_h):
        text_surface = font.render(text, False, color)
        text_x = pix_x + pix_w // 2 - text_surface.get_width() // 2
        text_y = pix_y + pix_h // 2 - text_surface.get_height() // 2
        self.surface.blit(text_surface, (text_x, text_y + self.offset_y))

    def draw_frame(self, color, pix_x, pix_y, pix_w, pix_h, thickness):
        pygame.draw.rect(self.surface, color, (pix_x, pix_y + self.offset_y, pix_w, pix_h), thickness)

    def convert_to_local(self, pos):
        x, y = pos
        return x, y - self.offset_y
