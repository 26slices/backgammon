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
        self.dice = random.sample(range(1, 7), 2)
        self.is_white_turn = self.dice[0] > self.dice[1]
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

        white_spaces = [space for space in self.board if space.occupant ==
                        'w' and space.space_type == 'outer']
        white_bar_space = self.bar['w']
        if white_bar_space.number_occupants > 0:
            white_spaces = [white_bar_space] + white_spaces

        red_spaces = [space for space in self.board if space.occupant ==
                      'r' and space.space_type == 'outer']
        red_bar_space = self.bar['r']
        if red_bar_space.number_occupants > 0:
            red_spaces = [red_bar_space] + red_spaces

        return {'w': white_spaces, 'r': red_spaces}

    @property
    def all_in_homeboard(self):
        white_spaces = self.players_spaces['w']
        red_spaces = self.players_spaces['r']

        white_all_in_homeboard = all(
            [space.position_number in self.homeboard['w'] for space in white_spaces])
        red_all_in_homeboard = all(
            [space.position_number in self.homeboard['r'] for space in red_spaces])

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

                    space.add_piece(turn_owner=self.turn)

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


        move_bank = self._get_largest_moves(move_bank)

        move_bank = self._remove_duplicates(move_bank)

        move_bank_readable = [[(start_space.position_number, end_space.position_number) for start_space, end_space in move] for move in move_bank]


        print('ALL MOVES: {}'.format(move_bank_readable))

        #convert moves to Move class
        move_bank = [Move(self.turn, move) for move in move_bank]
        return move_bank

    def _find_moves_for_dice_order(self, die0, die1):

        is_double = die0 == die1
        start_positions = self.players_spaces[self.turn]
        move_bank = []

        print('Start positions: {}'.format(
            [start_position.position_number for start_position in start_positions]))

        for space0 in start_positions:
            move_and_updated_start_positions0 = self.find_move_and_update_start_positions(
                space0, die0, start_positions)

            if move_and_updated_start_positions0:
                move0 = move_and_updated_start_positions0['move']
                updated_start_positions0 = move_and_updated_start_positions0[
                    'updated_start_positions']
                move_bank.append([move0])
                print('Adding move {}'.format([space.position_number for space in move0]))

                # loop through all spaces in updated start_positions
                for space1 in updated_start_positions0:
                    move_and_updated_start_positions1 = self.find_move_and_update_start_positions(
                        space1, die1, updated_start_positions0)
                    if move_and_updated_start_positions1:
                        move1 = move_and_updated_start_positions1['move']
                        # warning: think there was a mistake here (move_and_updated_start_positions0 instead of move_and_updated_start_positions1)
                        updated_start_positions1 = move_and_updated_start_positions1['updated_start_positions']
                        move_bank.append([move0, move1])

                        # if roll is a double we need to go two steps deeper to find four moves
                        if is_double:
                            print("***** IT'S A DOUBLE! ******" )
                            die = die1
                            for space2 in updated_start_positions1:
                                move_and_updated_start_positions2 = self.find_move_and_update_start_positions(
                                    space2, die, updated_start_positions1)
                                if move_and_updated_start_positions2:
                                    move2 = move_and_updated_start_positions2['move']
                                    updated_start_positions2 = move_and_updated_start_positions2['updated_start_positions']
                                    move_bank.append([move0, move1, move2])

                                    for space3 in updated_start_positions2:
                                        move_and_updated_start_positions3 = self.find_move_and_update_start_positions(
                                    space3, die, updated_start_positions2)
                                        if move_and_updated_start_positions3:
                                            move3 = move_and_updated_start_positions3['move']
                                            updated_start_positions3 = move_and_updated_start_positions3['updated_start_positions']
                                            move_bank.append([move0, move1, move2, move3])

                                        # if player is on the bar then that checker has to be moved, so no need to loop through other spaces
                                        if space3.space_type == 'bar':
                                            break

                                # if you're on the bar then you have to move checker off the bar so
                                # no need to look through other points
                                if space2.space_type == 'bar':
                                    break


                    # if you're on the bar then you have to move checker off the bar so
                    # no need to look through other points
                    if space1.space_type == 'bar':
                        break



            # if you're on the bar then you have to move checker off the bar so
            # no need to look through other points
            if space0.space_type == 'bar':
                print('That was a bar space, will try break')
                break


        return move_bank

    def find_move_and_update_start_positions(self, space0, die, start_positions):

        end_space = [space for space in self.board if
                     space.position_number == self._add_die_to_space(
                         space0, die)
                     and space.space_type != 'bar']
        if not end_space:
            print('Adding die {} to space {} goes out of range!'.format(die, space0))
            return None

        end_space = end_space[0]
        print('end space for space {} and die {}: {}'.format(space0.position_number,
                                                             die, end_space.position_number))
        if self._is_available_space(end_space):
            print("And it's an available space")
            move = (space0, end_space)

            # update the list of positions to look at
            # have to be careful not to update any of the actual spaces
            updated_start_positions = copy.copy(start_positions)
            end_space = copy.copy(end_space)
            end_space.add_piece(turn_owner=self.turn)
            updated_start_positions.append(end_space)

            updated_start_positions.remove(space0)
            space0 = copy.copy(space0)
            space0.remove_piece()
            # if there are still pips on that space we want to consider it
            # use insert so we can put it at the start and can consider pips on the bar
            if space0.number_occupants >= 1:
                updated_start_positions.insert(0, space0)

            return {'move': move, 'updated_start_positions': updated_start_positions}
        print("But it's not an available space")
        return None

    def _remove_duplicates(self, move_bank):
        '''
        removes duplicate moves from a list of moves
        '''

        move_bank_unique = []
        for move in move_bank:
            move_set = Counter([(start_space.position_number, end_space.position_number) for start_space, end_space in move])
            if all([move_set != Counter([(start_space.position_number, end_space.position_number) for start_space, end_space in unique_move]) for unique_move in move_bank_unique]):
                move_bank_unique.append(move)
        return move_bank_unique


    def _get_largest_moves(self, all_moves):
        """
        A player's move must be the max length possible, regardless of how many
        dice are used
        """
        # CAVEAT TO THIS WHEN YOU'RE BEARING OFF. THINK WE CAN OVERCOME THIS BY SAYING THAT THAT IF YOU BEAR OFF WITH A 6 FFOM THE 5 POINT IT HAS LENGTH 6
        max_move_length = max([sum([abs(start_pos.position_number - end_pos.position_number) for start_pos, end_pos in move]) for move in all_moves])
        moves = [move for move in all_moves if sum([abs(start_pos.position_number - end_pos.position_number) for start_pos, end_pos in move]) == max_move_length]

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

        if not self.all_in_homeboard[self.turn]:
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
            new_position = space.position_number + die
        else:
            new_position = space.position_number - die

        return new_position


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
        gives the start space and the second element gives the end space
        of a pip.
        '''
        self.id = 'generate_unique_id'
        self.player = player
        self.pip_moves = pip_moves
        self.start_positions = [
            pip_move[0].position_number for pip_move in pip_moves]
        self.end_positions = [
            pip_move[1].position_number for pip_move in pip_moves]

    @property
    def move_length(self):
        '''
        Length of a move
        '''
        move_length = sum([abs(pip_move[0].position_number - pip_move[1].position_number)
                           for pip_move in self.pip_moves])
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

            transformed_pip_moves.append((transformations[self.player][pip_move[0].position_number],
                                          transformations[self.player][pip_move[1].position_number]))

        return transformed_pip_moves
        # bg_notation = dict(Counter(transformed_pip_moves))

        # return bg_notation


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

    def remove_piece(self):
        '''
        Removes a piece from the space
        '''
        self.number_occupants -= 1
        if self.number_occupants == 0 and self.space_type == 'outer':
            self.occupant = None
        return self

    def add_piece(self, turn_owner=None):
        '''
        Adds a piece to the space
        '''

        self.number_occupants += 1
        self.occupant = turn_owner

        return self
