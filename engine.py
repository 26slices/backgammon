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
        which describe one player's home board and the other player's bar
        """

        self.board = [Space(0, 'home', 'r'),
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
                      Space(25, 'home', 'w'),
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
    def home_board(self):
        return {'w': self.board[-2], 'r': self.board[0]}

    @property
    def bar(self):
        return {'w': self.board[1], 'r': self.board[-1]}

    @property
    def players_spaces(self):
        white_spaces = [space for space in self.board if space.occupant == 'w']
        red_spaces = [space for space in self.board if space.occupant == 'r']
        return {'w': white_spaces, 'r': red_spaces}

    # @property
    # def bar_position(self):
    #     return {'w': 0, 'r': 25}

    # @property
    # def home_position(self):
    #     return {'w': 25, 'r': 0}

    @property
    def turn(self):
        return 'w' if self.is_white_turn else 'r'

    @property
    def not_turn(self):
        return 'r' if self.is_white_turn else 'w'

    @property
    def player_on_bar(self):
        return self.bar[self.turn].number_occupants > 0

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

    def get_legal_moves(self, all_moves):
        """
        applies _get_longest_move and _get_largest_move to finds the legal moves of a given board.
        input: list of all legal moves ignoring the edge cases.

        EDGE CASES: - If the player has pips on the
                        bar then they must be moved first.
                    - If a player can only legally use one of his die then
                        it must be the larger of the two die he can legally use.
                    - The player must use as many of the die as he possibly can
        """
        pass

    def _get_all_moves(self):
        '''
        Returns all moves given the dice without looking at the edge cases.
        '''
        all_moves = []
        dice_to_use1 = self._get_dice_to_use()
        positions1 = self._get_all_positions()
        board_length = len(self.board)
        is_doubles = len(set(dice_to_use1)) == 1

        for die1 in dice_to_use1:
            for i1 in range(board_length):
                if positions1[i1] > 0:
                    if self._is_available_point(self._add_die_to_pip(i1, die1)):
                        all_moves.append([i1, self._add_die_to_pip(i1, die1)])
                        dice_to_use2 = dice_to_use1
                        dice_to_use2.remove(die1)
                        positions2 = positions1
                        positions2[i1] -= 1
                        positions2[self._add_die_to_pip(i1, die1)] += 1

                        for die2 in dice_to_use2:
                            for i2 in range(board_length):
                                if positions2[i2] > 0:
                                    if self._is_available_point(self._add_die_to_pip(i2, die2)):
                                        all_moves.append(
                                            [i2, self._add_die_to_pip(i2, die2)])
                                        dice_to_use3 = dice_to_use2
                                        dice_to_use3.remove(die2)
                                        positions3 = positions2
                                        positions3[i2] -= 1
                                        positions3[self._add_die_to_pip(
                                            i2, die2)] += 1

                                        if not is_doubles:
                                            # if the dice isn't doubles then the next 2 for loops don't apply
                                            continue

                                        for die3 in dice_to_use3:
                                            for i3 in range(board_length):
                                                if positions3[i3] > 0:
                                                    if self._is_available_point(self._add_die_to_pip(i3, die3)):
                                                        all_moves.append(
                                                            [i3, self._add_die_to_pip(i3, die3)])
                                                        dice_to_use4 = dice_to_use3
                                                        dice_to_use4.remove(
                                                            die3)
                                                        positions4 = positions3
                                                        positions4[i3] -= 1
                                                        positions4[self._add_die_to_pip(
                                                            i3, die3)] += 1

                                                        for die4 in dice_to_use4:
                                                            for i4 in range(board_length):
                                                                if positions4[i4] > 0:
                                                                    if self._is_available_point(self._add_die_to_pip(i4, die4)):
                                                                        all_moves.append(
                                                                            [i4, self._add_die_to_pip(i4, die4)])

        # return just the unique moves found
        return list(set(all_moves))

    def _get_all_moves_from_bar(self):
        """
        When the player has pips on the bar get all the moves that involve
        moving pips from the bar. Should use this at the top of _get_all_moves
        to improve its efficiency
        """
        pass

    def _get_largest_move(self, all_moves):
        """
        If a player can only legally use one of his die then filters the
        list of moves by removing ones not using the larger of the two die.
        """
        pass

    def _get_longest_move(self, all_moves):
        """
        Applies edge case that the player must use as many of the die as he
        possibly can.
        """
        pass

    def _get_all_positions(self):
        """
        Returns the number of pips the turnowner has on each point.
        The first entry is their bar. Doesn't include their homeboard
        """
        all_positions = [self.bar[self.turn]]
        board_size = len(self.board)
        for i in range(1, board_size):
            if self.board[i][0] == self.turn:
                all_positions.append(self.bar_position[i][1])
            else:
                all_positions.append(0)
        return all_positions

    def _get_dice_to_use(self):
        """
        Doubles self.dice if the player has rolled doubles
        """
        if self.dice[0] != self.dice[1]:
            return [die for die in self.dice]
        return [die for die in self.dice * 2]

    def _is_available_point(self, point):
        """
        Determines if a given point is available for the player whose turn it is
        """
        # when trying to evaluate a point not in the board return False
        # rather than throwing an error
        if point < 0 or point > 24:
            return False
        elif self.board[point][0] in (self.turn, '-') or self.board[point] == [self.not_turn, 1]:
            return True
        return False

    def _add_die_to_pip(self, die, pip):
        """
        Applies the correct function (add/subtract) to a pip
        """
        if self.turn == 'w':
            return pip + die
        return pip - die


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

    def move_to_backgammon_notation(self):
        '''
        Converts the computer readable backgammon moves into standard bg
        notation. Need a mapping (Disctionaty) to individual pip moves
        {}

        '''
        red_transforms = {0: 'home', 25: 'bar'}
        for i in range(1, 25):
            red_transforms[i] = i

        white_transforms = {0: 'bar', 25: 'home'}
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

    def __init__(self, position_number, space_type, occupant=None, number_occupants=0):
        self.position_number = position_number
        self.space_type = space_type
        self.occupant = occupant
        self.number_occupants = number_occupants

    @property
    def is_outer_space(self):
        return self.space_type == 'outer'

    @property
    def is_home_space(self):
        return self.space_type == 'home'

    @property
    def is_bar_space(self):
        return self.space_type == 'bar'

    def remove_piece(self):
        '''
        Removes a piece from the space
        '''
        self.number_occupants -= 1
        if self.number_occupants == 0 and self.is_outer_space:
            self.occupant = None

    def add_piece(self, move):
        '''
        Adds a piece to the space
        '''
        # if not self.is_available():
        #     raise Exception('''
        #                     {} is trying to the space with number:
        #                     {}, occupant: {}, number_occupants:
        #                     {}. This isn't possible!
        #                     '''.format(move.player, self.number, self.occupant,
        #                                self.number_occupants)
        #                     )

        self.number_occupants += 1
        self.occupant = move.player

    # def is_available(self, move):
    #     '''
    #     Determines if this position is available given the current move
    #     '''
    #     if self.occupant in [None, move.player] or self.number_occupants == 1:
    #         return True
    #     return False
