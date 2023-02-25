import pygame as p
from time import sleep
import engine
import move_finder
import random

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
DELAY = 0.1
WHITE = engine.WHITE
RED = engine.RED


def load_images():
    pieces = ['black', 'white']
    for piece in pieces:

        IMAGES[piece] = p.transform.scale(p.image.load(
            'images/{}_stone.png'.format(piece)), (WIDTH / 20, WIDTH / 15))


screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()


def main():

    screen.fill(p.Color('dodgerblue'))
    gs = engine.GameState(match_to=11)
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_GameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        play_out_match(gs)
        running = False


def play_out_match(gs):
    play_out_game(gs)
    while not gs.match_over:
        gs.initialise_for_new_game()
        play_out_game(gs)


def play_out_game(gs):
    '''
    Plays out a single game in a match until someone has brought all their
    pieces home or someone has passed on a double
    '''
    print('{} is going to start'.format(gs.turn))
    play_out_dice_move(gs)

    while not gs.bearoff_win:

        play_out_decision(gs)
        if gs.player_passes:
            break

        setattr(gs, 'dice', gs.get_dice_value())
        play_out_dice_move(gs)

    print(gs.turn_number)

    if gs.bearoff_win:
        gs.update_score_for_bearoff_win()
    if not gs.match_over and gs.post_crawford is False and 1 in [gs.match_to - gs.score[WHITE], gs.match_to - gs.score[RED]]:
        gs.crawford = True
    elif not gs.match_over and gs.crawford is True:
        gs.crawford = False
        gs.post_crawford = True
    print(gs.score)
    sleep(5)


def play_out_dice_move(gs):

    print('Dice: {}'.format(gs.dice))
    moves = gs.get_all_moves()
    move = move_finder.find_random_move(moves)
    draw_dice(screen, gs.dice, gs.is_white_turn)
    sleep(DELAY)
    clock.tick(MAX_FPS)
    p.display.flip()
    gs.make_move(move)
    # print(gs.print_board)
    screen.fill(p.Color('dodgerblue'))
    draw_GameState(screen, gs)


def play_out_decision(gs):
    decisions = gs.get_all_decision_options()
    decisions_readable = [decision.decision_type for decision in decisions]
    print('Available decisions for {} are: {}'.format(
        gs.turn, decisions_readable))
    decision = move_finder.find_random_decision(decisions)
    print('Decision chosen: {}'.format(decision.decision_type))
    gs.make_cube_decision(decision)
    if decision.decision_type == 'double':
        decisions = gs.get_all_decision_options()
        decisions_readable = [
            decision.decision_type for decision in decisions]
        print('Available decisions for {} are: {}'.format(
            gs.turn, decisions_readable))
        decision = move_finder.find_random_decision(decisions)
        print('Decision chosen: {}'.format(decision.decision_type))
        gs.make_cube_decision(decision)


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
    draw_hash_brown(screen)


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
                add_middle_border = BAR * int(position in range(7, 19))
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


def draw_hash_brown(screen):
    font = p.font.SysFont('snellroundhand', 60)
    hash_brown = font.render(
        'Hash Brown', True, 'gold')
    x_coord_1, y_coord_1 = (WIDTH / 5, HEIGHT / 2 - 50)
    x_coord_2, y_coord_1 = (6 * WIDTH / 10 + BAR, HEIGHT / 2 - 50)
    screen.blit(hash_brown,
                (x_coord_1, y_coord_1))
    screen.blit(hash_brown,
                (x_coord_2, y_coord_1))

    enterprises = font.render(
        'Enterprises', True, 'gold')
    x_coord_1, y_coord_2 = (WIDTH / 5 + 10, HEIGHT / 2)
    x_coord_2, y_coord_2 = (6 * WIDTH / 10 + 10 + BAR, HEIGHT / 2)
    screen.blit(enterprises,
                (x_coord_1, y_coord_2))
    screen.blit(enterprises,
                (x_coord_2, y_coord_2))


def draw_dice(screen, dice, is_white_turn):
    dice_0 = dice[0]
    dice_1 = dice[1]

    draw_one_dice(screen, dice_0, is_white_turn, first_dice=True)
    draw_one_dice(screen, dice_1, is_white_turn, first_dice=False)


def draw_one_dice(screen, dice, is_white_turn, first_dice=True):
    if is_white_turn:
        colour = 'white'
        font_colour = 'black'
        right = 1
    else:
        colour = 'black'
        font_colour = 'white'
        right = 0

    dice_x_pos = WIDTH / 2 + (50 + int(first_dice) *
                              100 + BAR) * (2 * right - 1)
    dice_y_pos = HEIGHT / 2
    p.draw.rect(screen, colour, p.Rect(dice_x_pos, dice_y_pos, 50, 50))

    font = p.font.SysFont('arial', 20)
    dice = font.render(str(dice), True, font_colour)
    screen.blit(dice, (dice_x_pos, dice_y_pos))


if __name__ == '__main__':
    main()
