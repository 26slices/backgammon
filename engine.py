'''


'''

import copy
import random
from pprint import pprint
import numpy as np
from collections import Counter


class GameState:
    """
    This class is for storing the current state of the game. It will also
    determine all legal moves and provide a game log.
    """

    def __init__(self, first_to=7):
        """
        self.board describes how many and whose pieces are on a given point on
        the board. The first item in each tuple represents the player whose
        pieces are in that position and the second is the number of checkers in
        that position. The exception are the first and last elements
        which describe one player's bearoff_zone and the other player's bar
        """

        self.board = [Space(0, 'bearoff_zone', 'r'),
                      Space(0, 'bar', 'w'),
                      Space(1, 'outer', 'w', 2),
                      Space(2, 'outer'),
                      Space(3, 'outer'),
                      Space(4, 'outer'),
                      Space(5, 'outer'),
                      Space(6, 'outer', 'r', 5),
                      Space(7, 'outer'),
                      Space(8, 'outer', 'r', 3),
                      Space(9, 'outer'),
                      Space(10, 'outer'),
                      Space(11, 'outer'),
                      Space(12, 'outer', 'w', 5),
                      Space(13, 'outer', 'r', 5),
                      Space(14, 'outer'),
                      Space(15, 'outer'),
                      Space(16, 'outer'),
                      Space(17, 'outer', 'w', 3),
                      Space(18, 'outer'),
                      Space(19, 'outer', 'w', 5),
                      Space(20, 'outer'),
                      Space(21, 'outer'),
                      Space(22, 'outer'),
                      Space(23, 'outer'),
                      Space(24, 'outer', 'r', 2),
                      Space(25, 'bearoff_zone', 'w'),
                      Space(25, 'bar', 'r')
                      ]

        self.score = (0, 0)
        self.first_to = first_to
        self.crawford = False
        self.post_crawford = False
        self.cube = 1
        self.cube_owner = None
        self.dice = None
        self.is_white_turn = None
        self.cube_decision = False
        self.turn_number = 0
        self.move_log = []

    @property
    def bearoff_zone(self):
        return {'w': self.board[-2], 'r': self.board[0]}

    @property
    def bar(self):
        return {'w': self.board[1], 'r': self.board[-1]}

    @property
    def homeboard(self):
        return {'w': range(19, 25), 'r': range(1, 7)}

    @property
    def players_spaces(self):
        '''
        all spaces for each player. Note that bar space is first
        '''
        white_bar_space = [self.bar['w']]
        white_spaces = [space for space in self.board if space.occupant ==
                        'w' and space.space_type == 'outer']
        white_spaces = white_bar_space + white_spaces

        red_bar_space = [self.bar['r']]
        red_spaces = [space for space in self.board if space.occupant ==
                      'r' and space.space_type == 'outer']
        red_spaces = red_bar_space + red_spaces

        return {'w': white_spaces, 'r': red_spaces}

    @property
    def all_in_homeboard(self):
        white_spaces = self.players_spaces()['w']
        red_spaces = self.players_spaces()['r']

        white_all_in_homeboard = all(
            [space.position_number in self.homeboard()['w'] for space in white_spaces])
        red_all_in_homeboard = all(
            [space.position_number in self.homeboard()['r'] for space in red_spaces])

        return {'w': white_all_in_homeboard, 'r': red_all_in_homeboard}

    @property
    def turn(self):
        return 'w' if self.is_white_turn else 'r'

    @property
    def not_turn(self):
        return 'r' if self.is_white_turn else 'w'

    @property
    def player_on_bar(self):
        return self.bar[self.turn].number_occupants > 0

    @property
    def dice_to_use(self):
        """
        Doubles self.dice if the player has rolled doubles
        """
        if self.dice[0] != self.dice[1]:
            return [die for die in self.dice]
        return [die[0] * 4]

    @property
    def board_size(self):
        return len(self.board)

    def show_state(self):
        pprint(self.__dict__)

    def get_initial_roll(self):
        """
        Gets the first roll and sets the player whose turn it is to begin the
        game.
        """
        self.dice = random.sample(range(1, 7), 2)
        self.is_white_turn = self.dice[0] > self.dice[1]

    def generate_dice_value(self):
        """
        generates the dice value for a go
        """
        self.dice = (random.randint(1, 6), random.randint(1, 6))

    def make_decision(self, decision):
        """
        takes an instance of the Decision class and determines whether a person
        has doubled/accepted/passed
        """
        self.cube_decision = decision.initial_cube_value != decision.final_cube_value
        self.cube = decision.final_cube_value

    def make_move(self, move):
        """
        takes an instance of Move class and updates the board to reflect the move.
        It also inputs the move into the move log and updates whose turn it is.
        """
        if self.turn != move.player:
            raise Exception("It's {}'s turn!".format(self.turn))

        if self.is_white_turn:
            self.turn_number += 1

        # update the positions of where the pips are moving from
        for space in self.players_spaces[self.turn]:
            for start_position in move.start_positions:
                if space.position_number == start_position:
                    space.remove_piece()

        # update the positions of where the pips are moving to
        for end_position in move.end_positions:
            for space in self.board:
                if space.position_number == end_position:
                    # remove a piece and add it to the bar
                    # this assumes that the move is a legal move
                    if space.occupant == self.not_turn:
                        space.remove_piece()
                        self.board[self.bar[self.not_turn]
                                   ].number_occupants += 1

                    space.add_piece()

        # update the move log
        self.move_log.append(str(move))

        # update whose turn it is
        self._update_turn_owner()

    def _update_turn_owner(self):
        """
        update the player whose turn it is
        """
        self.is_white_turn = not self.is_white_turn

    def get_all_moves(self):
        '''
        Gets all legal moves for the case that there are no doubles
        '''
        move_bank = []
        die0 = self.dice[0]
        die1 = self.dice[1]

        move_bank += self._find_moves_for_dice_order(die0, die1)
        move_bank += self._find_moves_for_dice_order(die1, die0)

        return move_bank

    def _find_moves_for_dice_order(self, die0, die1):
        all_start_positions = self.players_spaces()[self.turn]
        move_bank = []

        for space0 in all_start_positions:
            move_and_updated_start_positions0 = self.find_move_and_update_start_positions(
                space0, die0, all_start_positions)
            move0 = move_and_updated_start_positions0['move']
            updated_start_positions0 = move_and_updated_start_positions0['updated_start_positions']
            if move0:
                move_bank.append([move0])
                for space1 in updated_start_positions0:
                    move_and_updated_start_positions1 = self.find_move_and_update_start_positions(
                        space1, die1, updated_start_positions0)
                    move1 = move_and_updated_start_positions1['move']
                    updated_start_positions1 = move_and_updated_start_positions1[
                        'updated_start_positions']
                    if move1:
                        move_bank.append([move0, move1])
                    # if you're on the bar then you have to move checker off the bar so
                    # no need to look through other points
                    if space1.space_type == 'bar' or updated_start_positions1[0]:
                        break
            # if you're on the bar then you have to move checker off the bar so
            # no need to look through other points
            if space0.space_type == 'bar':
                break

        # if you can use both die, you must use both die
        both_die_used = max([len(move) for move in move_bank]) == 2
        if both_die_used:
            move_bank = [move for move in move_bank if len(move) == 2]

        move_bank = self._get_largest_move(move_bank)

        return move_bank

    def find_move_and_update_start_positions(self, space0, die, start_positions):
        end_space = [space for space in self.board if
                     space.position_number == self._add_die_to_space(
                         space0, die)
                     and space.space_type != 'bar'][0]
        if self._is_available_space(end_space):
            move = (space0, end_space)

            # update the list of positions to look at
            # have to be careful not to update any of the actual spaces
            updated_start_positions = copy.copy(start_positions)
            end_space = copy.copy(end_space)
            end_space.add_piece()
            updated_start_positions.append(end_space)

            updated_start_positions.remove(space0)
            space0 = copy.copy(space0)
            space0.remove_piece()
            # if there are still pips on that space we want to consider it
            # use insert so we can put it at the start and can consider pips on the bar
            if space0.number_occupants >= 1:
                updated_start_positions.insert(0, space0)

            return {'move': move, 'updated_start_positions': updated_start_positions}

        return {'move': None, 'updated_start_positions': None}

    def _get_largest_move(self, all_moves):
        """
        If a player can only legally use one of his die then filters the
        list of moves by removing ones not using the larger of the two die.
        """
        max_move_length = max([move.move_length for move in all_moves])
        moves = [move for move in all_moves if move.move_length == max_move_length]

        return moves

    def _is_available_space(self, space):
        """
        Determines if a given space is available for the player whose turn it is
        """

        if (space.position_number not in range(26) or
            space.space_type == 'bar' or
            (space.position_number == self.bearoff_zone[self.not_turn].position_number
                and space.space_type == 'bearoff_zone') or
            (space.number_occupants > 1 and space.occupant == self.not_turn) or
                (self.all_in_homeboard[self.turn] is False and space.space_type == 'bearoff_zone')):
            return False
        else:
            return True

    def _add_die_to_space(self, space, die):
        """
        Adds die to a space, accounting for when the space is the furthest from
        bearoff and all spaces are in bearoff zone
        """

        if not self.all_in_homeboard()[self.turn]:
            return self.apply_correct_fn_die_to_space(space, die)

        else:
            players_spaces = self.players_spaces[self.turn]
            player_bearoff_zone = self.bearoff_zone[self.turn]

            distance_from_bar = abs(
                space.position_number - player_bearoff_zone.position_number)
            max_distance_from_bar = max(
                [abs(player_space.position_number - player_bearoff_zone.position_number) for player_space in players_spaces])
            if distance_from_bar == max_distance_from_bar and self.apply_correct_fn_die_to_space(space, die) not in range(26):
                return player_bearoff_zone.position_number
            else:
                return self.apply_correct_fn_die_to_space(space, die)

    def apply_correct_fn_die_to_space(self, space, die):
        """
        Applies the correct function (add/subtract) to a pip
        """
        if self.turn == 'w':
            space.position_number += die
        else:
            space.position_number -= die

        return space.position_number


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
        '''
        a move is a list of tuples where the first element of each tuple
        gives the start position and the second element gives the end position
        of a pip. White's start moves must be in the range [0, 24] and end moves in range [1, 25].
        Black's start moves must be in the range [1, 25] and end moves in range [0, 24].
        '''
        self.id = 'generate_unique_id'
        self.player = player
        self.pip_moves = pip_moves
        self.start_positions = [pip_move[0] for pip_move in pip_moves]
        self.end_positions = [pip_move[1] for pip_move in pip_moves]

    @property
    def move_length(self):
        '''
        Length of a move
        '''
        move_length = sum([abs(pip_move[0] - pip_move[1])
                           for pip_move in self.pip_moves()])
        return move_length

    def move_to_backgammon_notation(self):
        '''
        Converts the computer readable backgammon moves into standard bg
        notation. Need a mapping (Disctionaty) to individual pip moves
        {}

        '''
        red_transforms = {0: 'bearoff_zone', 25: 'bar'}
        for i in range(1, 25):
            red_transforms[i] = i

        white_transforms = {0: 'bar', 25: 'bearoff_zone'}
        for i in range(1, 25):
            white_transforms[i] = np.abs(i - 25)

        transformations = {'w': white_transforms, 'r': red_transforms}

        transformed_pip_moves = []
        for pip_move in self.pip_moves:
            transformed_pip_moves.append((transformations[self.player][pip_move[0]],
                                          transformations[self.player][pip_move[1]]))
        bg_notation = dict(Counter(transformed_pip_moves))

        return bg_notation


class Space:
    '''
    Each position on the board will be an instance of a space class
    '''

    def __init__(self, position_number, space_type, occupant=None,
                 number_occupants=0, red_homeboard=False, white_homeboard=False):
        self.position_number = position_number
        self.space_type = space_type
        self.occupant = occupant
        self.number_occupants = number_occupants

    @ property
    def remove_piece(self):
        '''
        Removes a piece from the space
        '''
        self.number_occupants -= 1
        if self.number_occupants == 0 and self.space_type == 'outer':
            self.occupant = None

    def add_piece(self, move):
        '''
        Adds a piece to the space
        '''

        self.number_occupants += 1
        self.occupant = move.player
