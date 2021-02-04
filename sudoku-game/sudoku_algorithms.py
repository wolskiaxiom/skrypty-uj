import random
import numpy as np


def is_number_box_safe(x, y, board, value):
    x_rel = int(x / 3) * 3
    y_rel = int(y / 3) * 3
    return not value in board[x_rel:x_rel + 3, y_rel: y_rel + 3]


def is_number_yline_safe(y, board, value):
    if value in board[:, y]:
        return False
    return True


def is_number_xline_safe(x, board, value):
    if value in board[x, :]:
        return False
    return True


# x,y - 1..3 - describe number of box on board
def is_box_correct(x, y, board):
    for num in range(1, 10):
        if np.count_nonzero(board[x * 3:x * 3 + 3, y * 3: y * 3 + 3] == num) > 1:
            return False
    return True


def is_xline_correct(x, board):
    for num in range(1, 10):
        if np.count_nonzero(board[x, :] == num) > 1:
            return False
    return True


def is_yline_correct(y, board):
    for num in range(1, 10):
        if np.count_nonzero(board[:, y] == num) > 1:
            return False
    return True


def fill_box(x, y, board):
    for box_x in range(3):
        for box_y in range(3):
            rand = random.randint(1, 9)
            while not is_number_box_safe(x + box_x, y + box_y, board, rand):
                rand = random.randint(1, 9)
            board[x + box_x][y + box_y] = rand
    pass


def is_board_correct(board):
    for x in range(8):
        if not is_xline_correct(x, board):
            return False
    for y in range(8):
        if not is_yline_correct(y, board):
            return False
    for box_x in range(3):
        for box_y in range(3):
            if not is_box_correct(box_x, box_y, board):
                return False
    return True


def fill_remaining_boxes(board, x, y, depth=0):
    if y > 8 and x < 8:
        x += 1
        y = 0
    if x > 8 and y > 8:
        return True
    if x < 3:
        if (y < 3):
            y = 3
    elif x < 6:  # x in 3,4,5
        if y == int(x / 3) * 3:
            y = y + 3
    else:  # x in 6,7,8
        if y == 6:
            x += 1
            y = 0
            if x > 8:
                return True

    for val in range(1, 10):
        if is_number_yline_safe(y, board, val) and is_number_xline_safe(x, board, val) and is_number_box_safe(x, y,
                                                                                                              board,
                                                                                                              val):
            board[x, y] = val
            if fill_remaining_boxes(board, x, y + 1, depth + 1):
                return True
            board[x, y] = 0
    return False


def fill_diagonal_boxes(board):
    fill_box(0, 0, board)
    fill_box(3, 3, board)
    fill_box(6, 6, board)


def generate_board():
    board = np.zeros((9, 9), dtype=int)
    fill_diagonal_boxes(board)
    fill_remaining_boxes(board, 0, 3)
    if not is_board_correct(board):
        raise Exception("Houston, we have a problem")
    return board


def remove_n_numbers_from_board(n, board):
    counter = 0
    while counter < n:
        counter += 1
        is_deleted = False
        while not is_deleted:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if board[x, y] != 0:
                is_deleted = True
                board[x, y] = 0
    return board
