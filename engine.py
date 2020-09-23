"""
This class is for stroing the current state of the game. It will also determine
all legal moves and provide a game log.
"""
import random
import numpy as np
from collections import Counter


class GameState():
    def __init__(self, first_to, is_white_turn=None):
        ''' self.board describes how many and whose pieces are on a given point on
         the board. The first item in each tuple represents the player whose
         pieces are in that position and the second is the number of checkers in
          that position. The exception is the bar which has 0 pieces initially
          but can hold pips from both players simultaneously. '''

        self.board = [['r', 0],  # red home board
                      ['w', 2], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['r', 5],
                      ['-', 0], ['r', 3], ['-', 0], ['-', 0], ['-', 0], ['w', 5],
                      ['r', 5], ['-', 0], ['-', 0], ['-', 0], ['w', 3], ['-', 0],
                      ['w', 5], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['r', 2],
                      ['w', 0],  # white home board
                      ['r', 0],  # red bar
                      ['w', 0],  # white bar
                      ]

        self.score = (0, 0)

        self.first_to = first_to

        self.crawford = False

        self.post_crawford = False

        self.cube = 1

        self.cube_owner = None

        self.dice = None

        self.is_white_turn = is_white_turn

        self.cube_decision = False

        self.move_log = []

        self.turn_number = 0

    @property
    def num_home(self):
        return (self.board[-1], self.board[-2])

    @property
    def bar(self):
        return (self.board[-3], self.board[-4])

    @property
    def white_on_bar(self):
        return self.bar[0][1] > 0

    @property
    def red_on_bar(self):
        return self.bar[1][1] > 0

    @property
    def turn(self):
        if self.is_white_turn:
            return 'w'
        return 'r'

    def show_state(self):
        '''Prints all attributes of the current state of the game.'''

        state = """ Board: {};
                      Score: {};
                      first to: {};
                      Crawford: {};
                      Post Crawford: {};
                      Cube value: {};
                      Cube owner: {};
                      Turn owner: {},
                      Dice: {}""".format(self.board, self.score, self.first_to,
                                         self.crawford, self.post_crawford,
                                         self.cube, self.cube_owner, self.turn,
                                         self.dice)
        return state

    def get_initial_roll(self):
        '''
        gets the first roll and sets the player whose turn it is to begin the game
        '''
        dice = (0, 0)
        while dice[0] == dice[1]:
            dice = (random.randint(1, 6), random.randint(1, 6))
        self.dice = dice
        self.is_white_turn = dice[0] > dice[1]

    def make_decision(self, decision):
        '''
        takes an instance of the Decision class and determines whether a person
        has doubled/accepted/passed
        '''
        self.cube_decision = decision.initial_cube_value != decision.final_cube_value
        self.cube = decision.final_cube_value

    def generate_dice_value(self):
        '''
        generates the dice value for a go
        '''
        self.dice = (random.randint(1, 6), random.randint(1, 6))

    def move_to_backgammon_notation(self, move):
        '''
        converts the computer readable backgammon moves into standard bg notation
        '''
        if move.player == 'r':
            bg_notation = Counter(move.pip_moves)
        else:
            transformed_pip_moves = [
                tuple(np.abs(np.subtract(pip_move, (25, 25)))) for pip_move in move.pip_moves]
            bg_notation = Counter(transformed_pip_moves)
        return bg_notation

    def make_move(self, move):
        '''
        takes an instance of Move class and updates the board to reflect the move,
        inputs the move into the move log and updates whose turn it is.
        '''
        if self.turn != move.player:
            raise ("It's {}'s turn!".format(self.turn))

        if self.is_white_turn:
            self.turn_number += 1
        # update the positions of where the pips are moving from
        for start_position in move.start_positions:
            self.board[start_position][1] -= 1
            if self.board[start_position][1] == 0:
                self.board[start_position][0] = '-'

        # update the positions of where the pips are moving to
        for end_position in move.end_positions:
            if self.board[end_position][0] in (self.turn, '-'):
                self.board[end_position][1] += 1
            self.board[end_position][0] = self.turn

        # update the move log
        self.move_log.append(self.move_to_backgammon_notation(move))

        # update whose turn it is
        self.is_white_turn = not self.is_white_turn


class Decision():
    def __init__(self, initial_cube_owner, final_cube_owner,
                 initial_cube_value, final_cube_value):
        self.id = 'generate_unique_id'
        self.initial_cube_owner = initial_cube_owner
        self.final_cube_owner = final_cube_owner
        self.initial_cube_value = initial_cube_value
        self.final_cube_value = final_cube_value


class Move():
    def __init__(self, player, pip_moves):
        self.id = 'generate_unique_id'
        self.player = player
        self.pip_moves = pip_moves
        self.start_positions = [pip_move[0] for pip_move in pip_moves]
        self.end_positions = [pip_move[1] for pip_move in pip_moves]
