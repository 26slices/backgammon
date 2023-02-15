import engine
import random
import pygame as p
from constants import TEST_LARGESE_MOVE, TEST_ONE_ON_BAR


p.init()

BOARD_WIDTH = 1200
SCORE_BORDER = 80
BAR = 50
HOME_BOARD = 80
WIDTH = SCORE_BORDER + BOARD_WIDTH + BAR + HOME_BOARD
HEIGHT = 750
WHITE_HOMEBOARD_START = (10, 10)
BLACK_HOMEBOARD_START = (10, HEIGHT - 10)
ROWS = 2
COLUMNS = 12
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['black', 'white']
    for piece in pieces:

        IMAGES[piece] = p.transform.scale(p.image.load(
            'images/{}_stone.png'.format(piece)), (WIDTH / 20, WIDTH / 15))


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('dodgerblue'))
    gs = engine.GameState()
    setattr(gs, 'board', TEST_LARGESE_MOVE)
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_GameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_GameState(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    '''
    draw the triangles on the board
    '''
    colors = [p.Color('blue3'), p.Color('gray69')]

    for r in range(ROWS):
        for c in range(COLUMNS):
            add_middle_border = BAR * int(c > 5)
            color = colors[(r + c) % 2]
            triangle_point_coord = [SCORE_BORDER +
                                    ((2 * c + 1) * 100) / 2 + add_middle_border, 200 * r - 100 + HEIGHT / 2]
            triangle_left_coord = [SCORE_BORDER +
                                   add_middle_border + c * 100, r * HEIGHT]
            triangle_right_coord = [
                SCORE_BORDER + add_middle_border + (c + 1) * 100, r * HEIGHT]
            coords = [triangle_point_coord,
                      triangle_left_coord, triangle_right_coord]
            p.draw.polygon(screen, color, coords)

    border_colour = 'darkblue'
    p.draw.rect(screen, border_colour, p.Rect(0, 0, SCORE_BORDER, HEIGHT))
    p.draw.rect(screen, border_colour, p.Rect(
        SCORE_BORDER + BOARD_WIDTH / 2, 0, BAR, HEIGHT))
    p.draw.rect(screen, border_colour, p.Rect(
        SCORE_BORDER + BAR + BOARD_WIDTH, 0, HOME_BOARD, HEIGHT))


def draw_pieces(screen, board):

    draw_outfield_pips(screen, board)
    draw_homeboard_pips(screen, board)
    draw_bar_pips(screen, board)


def draw_outfield_pips(screen, board):
    for r in range(ROWS):
        for c in range(1, COLUMNS + 1):

            position = r * 12 + c
            space = [
                space for space in board if space.position_number == position][0]
            if space.number_occupants > 0:
                add_middle_border = BAR * int(position in range(6, 19))
                space_position = space.position_number
                board_position = - 1 + int(
                    space_position <= 12) * space_position + (int(space_position > 12)) * (-1 * space_position + 25)
                player = space.occupant
                number_occupants = space.number_occupants
                for pip in range(min(number_occupants, 5)):
                    x_coord = HOME_BOARD + \
                        add_middle_border + (board_position) * 100 + 10
                    y_coord = (HEIGHT - 60) * r + \
                        (60 * pip) * (-2 * r + 1) - 15
                    screen.blit(IMAGES[player], p.Rect(x_coord, y_coord, 0, 0))
                if number_occupants > 5:
                    draw_text_for_pips(
                        screen, number_occupants, x_coord, y_coord)


def draw_homeboard_pips(screen, board):

    homeboard_spaces = [
        space for space in board if space.space_type == 'bearoff_zone']
    for space in homeboard_spaces:
        if space.number_occupants > 0:
            player = space.occupant
            number_occupants = space.number_occupants
            for pip in range(min(number_occupants, 5)):
                x_coord = 0
                is_white_player = int(player == 'white')
                y_coord = (HEIGHT - 60) * is_white_player + \
                    (60 * pip) * (-2 * is_white_player + 1) - 15
                screen.blit(IMAGES[player], p.Rect(x_coord, y_coord, 0, 0))
            if number_occupants > 5:
                draw_text_for_pips(
                    screen, number_occupants, x_coord, y_coord)


def draw_bar_pips(screen, board):
    bar_spaces = [
        space for space in board if space.space_type == 'bar']
    for space in bar_spaces:
        if space.number_occupants > 0:
            player = space.occupant
            number_occupants = space.number_occupants
            for pip in range(min(number_occupants, 3)):
                x_coord = SCORE_BORDER + BOARD_WIDTH / 2 - 10
                is_white_player = int(player == 'white')
                y_coord = HEIGHT / 2 - 50 + \
                    (60 * pip + 100) * (-2 * is_white_player + 1)
                screen.blit(IMAGES[player], p.Rect(x_coord, y_coord, 0, 0))
            if number_occupants > 3:
                draw_text_for_pips(
                    screen, number_occupants, x_coord + 5, y_coord)


def draw_text_for_pips(screen, number_occupants, x_coord, y_coord):
    font = p.font.SysFont('arial', 50)
    text = font.render(
        str(number_occupants), True, 'green')
    screen.blit(text,
                (x_coord, y_coord + 10))


if __name__ == '__main__':
    main()
