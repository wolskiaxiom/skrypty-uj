import pygame as pg
import numpy as np
import board_helper
import constants as c
import square as s

pg.init()
color_inactive = pg.Color('lightskyblue3')
screen = pg.display.set_mode((c.height, c.width))
clock = pg.time.Clock()
font = pg.font.Font(None, 60)
bold_font = pg.font.Font(None, 60)
bold_font.set_bold(True)
new_game_text = font.render('new game', True, c.WHITE, c.PURPLE)
incorrect_state_text = pg.font.Font(None, 20).render('something is not correct', True, c.RED)
won_game_text = pg.font.Font(None, 40).render('YOU WON', True, c.PURPLE)


def main():
    complete_board, initial_numbers, definite_numbers = board_helper.init_board()
    squares = np.full((9, 9), s.Square(-1, -1))
    for x in range(9):
        for y in range(9):
            squares[x][y] = s.Square(x, y)
    active_cell_xy = (-1, -1)
    done = False
    while not done:
        screen.fill((60, 60, 60))
        new_game_button = screen.blit(new_game_text, (500, 100))
        for event in pg.event.get():
            # perform action on click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                click_xy = board_helper.get_coordinates_from_pos(pos, squares)
                if click_xy != (-1, -1) and click_xy != active_cell_xy and initial_numbers[click_xy[0]][click_xy[1]] == 0:
                    active_cell_xy = click_xy
                else:
                    active_cell_xy = (-1, -1)
                if new_game_button.collidepoint(pos):
                    complete_board, initial_numbers, definite_numbers = board_helper.init_board()
                    board_helper.clear_squares(squares)
            # perform action on number input
            if event.type == pg.KEYDOWN and active_cell_xy != (-1, -1) and 48 < event.key < 58:
                definite_numbers[active_cell_xy[0]][active_cell_xy[1]] = int(event.unicode)
                active_cell_xy = (-1, -1)
            if event.type == pg.QUIT:
                done = True

        # print board
        for x in range(9):
            for y in range(9):
                square = squares[x][y]
                if initial_numbers[x][y] != 0:
                    square.set_text(initial_numbers[x][y], bold_font, c.RED)
                elif definite_numbers[x][y] != 0:
                    square.set_text(definite_numbers[x][y], font, c.BLUE)
                if active_cell_xy == (x, y):
                    pg.draw.rect(screen, c.GREEN, square.txt_rect, 0)
                else:
                    screen.blit(square.txt_surface, square.txt_rect)
        correct = board_helper.is_correct(definite_numbers)
        won = np.array_equal(complete_board, definite_numbers)

        # print text messages
        if won:
            screen.blit(won_game_text, (170, 20))
        elif not correct:
            screen.blit(incorrect_state_text, (170, 20))

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
