import constants as c
import pygame as pg
import sudoku_algorithms
import copy


def clear_squares(squares):
    for x in range(9):
        for y in range(9):
            squares[x, y].txt_surface = pg.Surface((c.cell_size - 15, c.cell_size - 5))


def get_coordinates_from_pos(pos, squares):
    for x in range(9):
        for y in range(9):
            if squares[x][y].txt_rect.collidepoint(pos):
                return x, y
    return -1, -1


def init_board(empty_cells_num):
    complete = sudoku_algorithms.generate_board()
    initial = sudoku_algorithms.remove_n_numbers_from_board(empty_cells_num, copy.deepcopy(complete))
    definite = initial.copy()
    return complete, initial, definite


def is_correct(board):
    return sudoku_algorithms.is_board_correct(board)


def draw_lines(screen):
    for x in range(8):
        x_cord = c.border_space + 15 + (c.cell_size + c.cell_space) * (x + 1)
        if x % 3 == 2:
            pg.draw.line(screen, c.LIGHT_GREY, (x_cord, c.border_space + 20),
                             (x_cord, c.border_space + 9 * (c.cell_space + c.cell_size) + 20), 3)
    for y in range(8):
        y_cord = c.border_space + 20 + (c.cell_size + c.cell_space) * (y + 1)
        if y % 3 == 2:
            pg.draw.line(screen, c.LIGHT_GREY, (c.border_space + 20, y_cord),
                         (c.border_space + 10  + 9 * (c.cell_space + c.cell_size), y_cord), 3)