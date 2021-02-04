import pygame as pg
import constants as c


class Square:
    x = -1
    y = -1

    @staticmethod
    def calculate_center(x, y):
        center_x = c.border_space + c.cell_space + 20 + (c.cell_space + c.cell_size) * x
        center_y = c.border_space + c.cell_space + 20 + (c.cell_space + c.cell_size) * y
        return center_x, center_y

    def __init__(self, x, y):
        self.x = x
        self.y = y
        center_coordinates = self.calculate_center(x, y)
        self.txt_surface = pg.Surface((c.cell_size - 15, c.cell_size - 5))
        self.txt_rect = pg.Rect(center_coordinates[1], center_coordinates[0], c.cell_size - 15, c.cell_size - 5)

    def set_text(self, text, font, color, background=None):
        self.txt_surface = font.render(str(text), True, color)

