import constants as c
import pygame as pg
import sudoku_algorithms
import copy


def clear_squares(squares):
    for x in range(9):
        for y in range(9):
            squares[x, y].txt_surface = pg.Surface((c.cell_size, c.cell_size))


def get_coordinates_from_pos(pos, squares):
    for x in range(9):
        for y in range(9):
            if squares[x][y].txt_rect.collidepoint(pos):
                return x, y
    return -1, -1


def init_board():
    complete = sudoku_algorithms.generate_board()
    initial = sudoku_algorithms.remove_n_numbers_from_board(2, copy.deepcopy(complete))
    definite = initial.copy()
    return complete, initial, definite


def is_correct(board):
    return sudoku_algorithms.is_board_correct(board)
