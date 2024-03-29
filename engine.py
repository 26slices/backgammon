'''


'''

import copy
import pandas as pd
import random
import sys
from pprint import pprint
import numpy as np
from collections import Counter
# from constants import STARTING_BOARD

WHITE = 'white'
RED = 'black'


class GameState:
    """
    This class is for storing the current state of the game. It will also
    determine all legal moves and provide a game log.
    """

    def __init__(self, match_to=7):
        """
        self.board describes how many and whose pieces are on a given point on
        the board. The first item in each tuple represents the player whose
        pieces are in that position and the second is the number of checkers in
        that position. The exception are the first and last elements
        which describe one player's bearoff_zone and the other player's bar
        """

        self.board = copy.deepcopy(STARTING_BOARD)
        self.score = {WHITE: 0, RED: 0}
        self.match_to = match_to
        self.crawford = False
        self.post_crawford = False
        self.cube_value = 1
        self.cube_owner = None
        self.dice = random.sample(range(1, 7), 2)

        self.is_white_turn = self.dice[0] > self.dice[1]
        self.is_outstanding_cube_decision = False
        self.player_passes = False
        self.turn_number = 0
        self.move_log = []

    def initialise_for_new_game(self):
        self.board = copy.deepcopy(STARTING_BOARD)
        self.cube_value = 1
        self.cube_owner = None
        self.dice = random.sample(range(1, 7), 2)
        self.is_white_turn = self.dice[0] > self.dice[1]
        self.is_outstanding_cube_decision = False
        self.player_passes = False
        self.turn_number = 0

    @property
    def print_board(self):
        board = {'position': [space.position_number for space in self.board],
                 'type': [space.space_type for space in self.board],
                 'occupant': [space.occupant for space in self.board],
                 'number_occupants': [space.number_occupants for space in self.board]
                 }
        board = pd.DataFrame(data=board)

        if not board['number_occupants'].between(0, 15).all():
            print(
                '************************ Outside range BUG!!! ************************')
            sys.exit()
        elif board[(board['occupant'].isna()) & (board['number_occupants'] > 0)].shape[0] > 0:
            sys.exit()
        elif board[(board['type'] == 'outer') & (board['occupant'].notnull()) & (board['number_occupants'] == 0)].shape[0] > 0:
            print(
                '************************ Claimed but unoccupied BUG!!! ************************')
            sys.exit()
        return board.to_string(index=False)

    @property
    def bearoff_zone(self):
        return {WHITE: self.board[-2], RED: self.board[0]}

    @property
    def bar(self):
        return {WHITE: self.board[1], RED: self.board[-1]}

    @property
    def homeboard(self):
        return {WHITE: range(19, 25), RED: range(1, 7)}

    @property
    def players_spaces(self):
        '''
        all spaces for each player.  **Note that bar space is first**
        '''

        white_spaces = [space for space in self.board if space.occupant == WHITE
                        and space.space_type == 'outer']
        white_bar_space = self.bar[WHITE]
        if white_bar_space.number_occupants > 0:
            white_spaces = [white_bar_space] + white_spaces

        red_spaces = [space for space in self.board if space.occupant ==
                      RED and space.space_type == 'outer']
        red_bar_space = self.bar[RED]
        if red_bar_space.number_occupants > 0:
            red_spaces = [red_bar_space] + red_spaces

        return {WHITE: white_spaces, RED: red_spaces}

    @property
    def number_beared_off(self):
        return {WHITE: self.bearoff_zone[WHITE].number_occupants,
                RED: self.bearoff_zone[RED].number_occupants}

    @property
    def bearoff_win(self):
        '''
        Note that a 'pass' cube decisison will also end the game
        '''
        return self.number_beared_off[WHITE] == 15 or self.number_beared_off[RED] == 15

    def update_score_for_bearoff_win(self):
        winner = [player for player,
                  score in self.number_beared_off.items() if score == 15][0]
        loser = [player for player,
                 score in self.number_beared_off.items() if score != 15][0]

        loser_spaces = self.players_spaces[loser]
        if self.any_in_opponents_homeboard(loser_spaces):
            win_type = 3  # backgammon =D
        elif self.number_beared_off[loser] == 0:
            win_type = 2  # gammon
        else:
            win_type = 1
        self.score[winner] += self.cube_value * win_type

        if self.score[winner] > self.match_to:
            self.score[winner] = self.match_to
        return self.score

    @property
    def match_over(self):
        return self.score[WHITE] >= self.match_to or self.score[RED] >= self.match_to

    def any_in_opponents_homeboard(self, all_spaces):

        any_in_opponents_homeboard = any(
            [space.position_number in self.homeboard[self.not_turn] or space.position_number ==
             self.bar[self.turn].position_number for space in all_spaces])

        return any_in_opponents_homeboard

    @property
    def turn(self):
        return WHITE if self.is_white_turn else RED

    @property
    def not_turn(self):
        return RED if self.is_white_turn else WHITE

    @property
    def player_on_bar(self):
        return self.bar[self.turn].number_occupants > 0

    @property
    def board_size(self):
        return len(self.board)

    def all_in_homeboard(self, all_spaces):
        '''
        returns true if every space from all_spaces is in the homeboard for the
        player whose turn it is
        '''
        all_in_homeboard = all(
            [space.position_number in self.homeboard[self.turn] or
             space.position_number == self.bearoff_zone[self.turn].position_number
             for space in all_spaces])

        return all_in_homeboard

    def get_dice_value(self):
        """
        generates the dice value for a go
        """
        return (random.randint(1, 6), random.randint(1, 6))

    def make_cube_decision(self, decision):
        """
        takes an instance of the Decision class and updates the gamestate
        """

        if decision.decision_type == 'no double':
            pass
        elif decision.decision_type == 'double':
            self.is_outstanding_cube_decision = True
            self.cube_value = 2 * self.cube_value
            self._update_turn_owner()
        elif decision.decision_type == 'accept':
            self.cube_owner = self.turn
            self._update_turn_owner()
            self.is_outstanding_cube_decision = False
        elif decision.decision_type == 'pass':
            self.player_passes = True
            self.score[self.not_turn] += self.cube_value / 2

    def get_all_decision_options(self):
        '''
        returns all valid decisions given the current gamestate
        '''

        # it it's an outstanding decision then you have to either double or pass
        if self.is_outstanding_cube_decision:
            take = Cube_Decision(self.cube_value, self.cube_value, True)
            Pass = Cube_Decision(self.cube_value, 1, True)
            return [take, Pass]
        else:
            no_double = Cube_Decision(self.cube_value, self.cube_value, False)
            if self.cube_owner in [self.turn, None] and self.turn_number >= 1 \
                    and self.crawford is False and (self.score[self.turn] + self.cube_value < self.match_to):
                double = Cube_Decision(
                    self.cube_value, 2 * self.cube_value, False)
                return [double, no_double]
            else:
                return [no_double]

    def make_move(self, move):
        """
        takes an instance of Move class and updates the board to reflect the move.
        It also inputs the move into the move log and updates whose turn it is.
        """

        if move is not None:
            # print('Move chosen: {}'.format(move.space_moves))

            if self.turn != move.player:
                raise Exception("It's {}'s turn!".format(self.turn))

            for space in self.board:
                for start_position, end_position in move.space_moves:
                    # update the positions of where the pips are moving from
                    if space.position_number == start_position and space.space_type in ['outer', 'bar']:
                        space.remove_pip()

                    # update the positions of where the pip is moving to
                    if space.position_number == end_position and space.space_type in ['outer', 'bearoff_zone']:
                        # remove a piece and add it to the bar
                        if space.occupant == self.not_turn:
                            space.remove_pip()
                            self.bar[self.not_turn].number_occupants += 1

                        space.add_pip(turn_owner=self.turn)
        else:
            print('No legal moves!!')
        self.turn_number += 1
        self.move_log.append(str(move))
        self._update_turn_owner()

    def _update_turn_owner(self):
        """
        update the player whose turn it is
        """
        self.is_white_turn = not self.is_white_turn

    def get_all_moves(self):
        '''
        Gets all legal moves
        '''
        move_bank = []
        die0 = self.dice[0]
        die1 = self.dice[1]

        move_bank += self._find_moves_for_dice_order(die0, die1)
        if die0 != die1:
            move_bank += self._find_moves_for_dice_order(die1, die0)

        if len(move_bank) > 0:
            move_bank = self._get_largest_moves(move_bank)

            move_bank = self._remove_duplicates_and_format(move_bank)

        # convert moves to Move class
        move_bank = [Move(self.turn, move) for move in move_bank]
        return move_bank

    def _find_moves_for_dice_order(self, die0, die1):

        is_double = die0 == die1
        start_positions = self.players_spaces[self.turn]
        move_bank = []

        for space0 in start_positions:
            move_and_updated_start_positions0 = self.find_move_and_update_start_positions(
                space0, die0, start_positions)

            if move_and_updated_start_positions0:
                move0 = move_and_updated_start_positions0['move']
                updated_start_positions0 = move_and_updated_start_positions0[
                    'updated_start_positions']
                move_bank.append([move0])
                # loop through all spaces in updated start_positions
                for space1 in updated_start_positions0:
                    move_and_updated_start_positions1 = self.find_move_and_update_start_positions(
                        space1, die1, updated_start_positions0)
                    if move_and_updated_start_positions1:
                        move1 = move_and_updated_start_positions1['move']
                        updated_start_positions1 = move_and_updated_start_positions1[
                            'updated_start_positions']
                        move_bank.append([move0, move1])

                        # if roll is a double we need to go two steps deeper to find four moves
                        if is_double:
                            die = die1
                            for space2 in updated_start_positions1:
                                move_and_updated_start_positions2 = self.find_move_and_update_start_positions(
                                    space2, die, updated_start_positions1)
                                if move_and_updated_start_positions2:
                                    move2 = move_and_updated_start_positions2['move']
                                    updated_start_positions2 = move_and_updated_start_positions2[
                                        'updated_start_positions']
                                    move_bank.append([move0, move1, move2])
                                    for space3 in updated_start_positions2:
                                        move_and_updated_start_positions3 = self.find_move_and_update_start_positions(
                                            space3, die, updated_start_positions2)
                                        if move_and_updated_start_positions3:
                                            move3 = move_and_updated_start_positions3['move']
                                            move_bank.append(
                                                [move0, move1, move2, move3])

                                        # if player is on the bar then that checker has to be moved, so no need to loop through other spaces
                                        if space3.space_type == 'bar':
                                            break
                                # if you're on the bar then you have to move checker off the bar so
                                # no need to look through other points
                                if space2.space_type == 'bar':
                                    break
                    if space1.space_type == 'bar':
                        break
            if space0.space_type == 'bar':
                break

        return move_bank

    def find_move_and_update_start_positions(self, space0, die, start_positions):

        end_space = [space for space in self.board if
                     space.position_number == self._add_die_to_space(start_positions,
                                                                     space0, die)
                     and space.space_type != 'bar']
        if not end_space:
            return None

        end_space = end_space[0]
        if self._is_available_space(start_positions, end_space):
            move = (space0, end_space)

            # update the list of positions to look at
            # have to be careful not to update any of the actual spaces
            updated_start_positions = copy.copy(start_positions)
            same_as_end_space = [
                space for space in updated_start_positions if space.position_number == end_space.position_number]
            if same_as_end_space:
                same_as_end_space = same_as_end_space[0]
                updated_start_positions.remove(
                    same_as_end_space)
                end_space = copy.copy(same_as_end_space)
                end_space.add_pip(turn_owner=self.turn)
            else:
                end_space = copy.copy(end_space)
                end_space.add_pip(turn_owner=self.turn)
                if end_space.space_type == 'outer':
                    setattr(end_space, 'number_occupants', 1)
            # if it's an outer space let's add it back into the list of spaces to consider
            if end_space.space_type == 'outer':
                updated_start_positions.append(end_space)

            updated_start_positions.remove(space0)
            space0 = copy.copy(space0)
            space0.remove_pip()
            # if there are still pips on that space we want to consider it
            # use insert so we can put it at the start so that we can still consider pips on the bar
            if space0.number_occupants >= 1:
                updated_start_positions.insert(0, space0)

            return {'move': move, 'updated_start_positions': updated_start_positions}
        return None

    def _remove_duplicates_and_format(self, move_bank):
        '''
        removes duplicate moves from a list of moves and reduces moves where one
        pip is moved to just show start position and end position
        '''

        move_bank_unique = []
        for move in move_bank:
            move_set = Counter([(start_space.position_number, end_space.position_number)
                                for start_space, end_space in move])
            if all([move_set != Counter([(start_space.position_number, end_space.position_number)
                                         for start_space, end_space in unique_move])
                    for unique_move in move_bank_unique]):
                move_bank_unique.append(move)
        return move_bank_unique

    def _get_largest_moves(self, all_moves):
        """
        A player's move must be the max length possible, regardless of how many
        dice are used
        """

        max_move_length = max([sum([abs(start_pos.position_number - end_pos.position_number)
                                    for start_pos, end_pos in move]) for move in all_moves])
        moves = [move for move in all_moves if sum(
            [abs(start_pos.position_number - end_pos.position_number) for start_pos, end_pos in move]) == max_move_length]

        return moves

    def _is_available_space(self, all_spaces, space):
        """
        Determines if a given space is available for the player whose turn it is
        """

        all_in_homeboard = self.all_in_homeboard(all_spaces)

        if (space.position_number not in range(26) or
            space.space_type == 'bar' or
            (space.position_number == self.bearoff_zone[self.not_turn].position_number
                and space.space_type == 'bearoff_zone') or
            (space.number_occupants > 1 and space.occupant == self.not_turn) or
                (all_in_homeboard is False and space.space_type == 'bearoff_zone')):
            return False
        else:
            return True

    def _add_die_to_space(self, all_spaces, space, die):
        """
        Adds die to a space, accounting for when the space is the furthest from
        bearoff and all spaces are in bearoff zone
        """

        all_in_homeboard = self.all_in_homeboard(all_spaces)

        if not all_in_homeboard:
            return self.apply_correct_fn_die_to_space(space, die)

        else:
            player_bearoff_zone = self.bearoff_zone[self.turn]

            distance_from_bearoff = abs(
                space.position_number - player_bearoff_zone.position_number)
            max_distance_from_bearoff = max(
                [abs(player_space.position_number - player_bearoff_zone.position_number) for player_space in all_spaces])
            # if the pip is the furthest pip away and adding the dice takes you past the bearoff, then make it the bearoff
            if distance_from_bearoff == max_distance_from_bearoff and self.apply_correct_fn_die_to_space(space, die) not in range(26):
                return player_bearoff_zone.position_number
            else:
                return self.apply_correct_fn_die_to_space(space, die)

    def apply_correct_fn_die_to_space(self, space, die):
        """
        Applies the correct function (add/subtract) to a pip
        """
        if self.turn == WHITE:
            new_position = space.position_number + die
        else:
            new_position = space.position_number - die

        return new_position


class Cube_Decision():
    '''
    Cube decision to either double, not double, accepts or pass
    '''

    def __init__(self, initial_cube_value, subsequent_cube_value, is_outstanding_cube_decision):
        self.initial_cube_value = initial_cube_value
        self.subsequent_cube_value = subsequent_cube_value
        self.is_outstanding_cube_decision = is_outstanding_cube_decision

    @property
    def decision_type(self):
        if not self.is_outstanding_cube_decision and self.initial_cube_value == self.subsequent_cube_value:
            return 'no double'
        elif not self.is_outstanding_cube_decision and 2 * self.initial_cube_value == self.subsequent_cube_value:
            return 'double'
        elif self.is_outstanding_cube_decision and self.initial_cube_value == self.subsequent_cube_value:
            return 'accept'
        elif self.is_outstanding_cube_decision and self.subsequent_cube_value == 1:
            return 'pass'


class Move():
    def __init__(self, player, pip_moves):
        '''
        a move is a list of tuples where the first element of each tuple
        gives the start space and the second element gives the end space
        of a pip.
        '''

        self.player = player
        self.pip_moves = pip_moves
        self.space_moves = [
            [pip_move[0].position_number, pip_move[1].position_number] for pip_move in pip_moves]

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

        transformations = {WHITE: white_transforms, RED: red_transforms}

        transformed_pip_moves = []
        for pip_move in self.pip_moves:

            transformed_pip_moves.append((transformations[self.player][pip_move[0].position_number],
                                          transformations[self.player][pip_move[1].position_number]))

        return transformed_pip_moves


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

    @property
    def print_space(self):
        space = {'position': self.position_number, 'space_type': self.space_type,
                 'occupant': self.occupant, 'number_occupants': self.number_occupants}

        return space

    def remove_pip(self):
        '''
        Removes a piece from the space
        '''
        self.number_occupants -= 1
        if self.number_occupants == 0 and self.space_type == 'outer':
            self.occupant = None
        return self

    def add_pip(self, turn_owner=None):
        '''
        Adds a piece to the space
        '''

        self.number_occupants += 1
        self.occupant = turn_owner

        return self


STARTING_BOARD = [Space(0, 'bearoff_zone', RED),
                  Space(0, 'bar', WHITE),
                  Space(1, 'outer', WHITE, 2),
                  Space(2, 'outer'),
                  Space(3, 'outer'),
                  Space(4, 'outer'),
                  Space(5, 'outer'),
                  Space(6, 'outer', RED, 5),
                  Space(7, 'outer'),
                  Space(8, 'outer', RED, 3),
                  Space(9, 'outer'),
                  Space(10, 'outer'),
                  Space(11, 'outer'),
                  Space(12, 'outer', WHITE, 5),
                  Space(13, 'outer', RED, 5),
                  Space(14, 'outer'),
                  Space(15, 'outer'),
                  Space(16, 'outer'),
                  Space(17, 'outer', WHITE, 3),
                  Space(18, 'outer'),
                  Space(19, 'outer', WHITE, 5),
                  Space(20, 'outer'),
                  Space(21, 'outer'),
                  Space(22, 'outer'),
                  Space(23, 'outer'),
                  Space(24, 'outer', RED, 2),
                  Space(25, 'bearoff_zone', WHITE),
                  Space(25, 'bar', RED)
                  ]
