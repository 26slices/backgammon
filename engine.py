import random
import numpy as np
from collections import Counter


# NOTE make a separate module for each class.


class GameState():
    # NOTE Good to keep docstring lines <= 79 chars
    """
    This class is for storing the current state of the game. It will also determine
    all legal moves and provide a game log.
    """

    def __init__(self, first_to=7):
        # NOTE why inconsistent use docstring style here? Docstring used above
        # is better :)
        ''' self.board describes how many and whose pieces are on a given point on
         the board. The first item in each tuple represents the player whose
         pieces are in that position and the second is the number of checkers in
          that position. The exception are the first and last elements
          which describe one player's home board and the other player's bar '''

        # NOTE I would suggest adding a `Space` class or something like that.
        # It should track the `occupant`, e.g. `w`, `r`, or `None`, and the
        # value. An aside, use constants for string which you use repeatedly.
        # You should have a constant for `'w'` and `'r'` and I reckon you
        # should just use None when there is no occupant.

        # NOTE after refactoring this I wonder if you could make the board set
        # up more programmatic? Maybe more hassle than it's worth.
        self.board = [[0, 0],  # red home board/white bar
                      ['w', 2], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['r', 5],
                      ['-', 0], ['r', 3], ['-', 0], ['-', 0], ['-', 0], ['w', 5],
                      ['r', 5], ['-', 0], ['-', 0], ['-', 0], ['w', 3], ['-', 0],
                      ['w', 5], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['r', 2],
                      [0, 0]  # white home board/red bar
                      ]

        self.score = (0, 0)
        self.first_to = first_to
        self.crawford = False
        self.post_crawford = False
        self.cube = 1
        self.cube_owner = None
        self.dice = None
        self.is_white_turn = None  # NOTE should this not be `False`?
        self.cube_decision = False
        self.turn_number = 0
        self.move_log = []

    @property
    def home_board(self):
        return {'w': self.board[-1][0], 'r': self.board[0][0]}

    @property
    def bar(self):
        return {'w': self.board[0][1], 'r': self.board[-1][1]}

    @property
    def bar_position(self):
        return {'w': 0, 'r': 25}

    @property
    def home_position(self):
        return {'w': 25, 'r': 0}

    @property
    def turn(self):
        return 'w' if self.is_white_turn else 'r'

    @property
    def not_turn(self):
        return 'r' if self.is_white_turn else 'w'

    @property
    def player_on_bar(self):
        return self.bar[self.turn] > 0

    def show_state(self):
        # NOTE use consistent docstring style.
        '''Prints all attributes of the current state of the game.'''

        # Is this for debugging purposes?
        # NOTE This is not a very programmatic way of handling this. Firstly,
        # as you add more attributes you'll need to maintain this function.
        # Also it's just a bunch of unnecessary code.

        # The easiest way to do improve this would be to import `pprint` which
        # is a library which prints dictionaries nicely. Then just replace the
        # contents of this function with `pprint(self.__dict__)`. I think that
        # should work though I haven't tested it.
        state = """ Board: {};
                    Bar: {};
                      Score: {};
                      first to: {};
                      Crawford: {};
                      Post Crawford: {};
                      Cube value: {};
                      Cube owner: {};
                      Turn owner: {},
                      Dice: {}""".format(self.board, self.bar, self.score, self.first_to,
                                         self.crawford, self.post_crawford,
                                         self.cube, self.cube_owner, self.turn,
                                         self.dice)
        return state

    def get_initial_roll(self):
        # NOTE caps at the start of docstring for consistency.
        '''
        gets the first roll and sets the player whose turn it is to begin the game
        '''
        dice = (0, 0)
        # NOTE are we basically saying get two random numbers between 1 and 6
        # that aren't the same? If so, I don't really like this approach. This
        # is a fairly academic point but theoretically this could iterate many
        # times before getting to a valid combination. Just feels like a smelly
        # approach to me.

        # A better approach would be to use this:
        # https://docs.python.org/2/library/random.html#random.sample
        # Maybe your code could be `roll = random.sample(range(1, 6), 2)`
        # Also possibly a good idea to make that into a method so that it is
        # self documenting, e.g. `get_unique_dice_roll` or something.
        while dice[0] == dice[1]:
            dice = (random.randint(1, 6), random.randint(1, 6))
        self.dice = dice
        self.is_white_turn = dice[0] > dice[1]

    def generate_dice_value(self):
        '''
        generates the dice value for a go
        '''
        self.dice = (random.randint(1, 6), random.randint(1, 6))

    def make_decision(self, decision):
        '''
        takes an instance of the Decision class and determines whether a person
        has doubled/accepted/passed
        '''
        # NOTE this is quite confusing. The naming here must be wrong because
        # on first glance I can't really tell what's going on?
        self.cube_decision = decision.initial_cube_value != decision.final_cube_value
        self.cube = decision.final_cube_value

    def make_move(self, move):
        '''
        takes an instance of Move class and updates the board to reflect the move.
        It also inputs the move into the move log and updates whose turn it is.
        '''
        if self.turn != move.player:
            raise Exception("It's {}'s turn!".format(self.turn))

        if self.is_white_turn:
            self.turn_number += 1
        # update the positions of where the pips are moving from
        for start_position in move.start_positions:

            # NOTE I mentioned above that each space on the board should be
            # represented by a `Space` class. That way we could add methods
            # like `remove_piece` which would handle this logic.

            # note that this does work for the bar moves
            self.board[start_position][1] -= 1
            if self.board[start_position][1] == 0 and self.board[start_position][0] not in (0, 25):
                self.board[start_position][0] = '-'

        # update the positions of where the pips are moving to
        # NOTE again refactor this into a method on the `Space` class.
        for end_position in move.end_positions:
            if self.board[end_position] == self.home_position[self.turn]:
                # NOTE you sure the index is right here? Should it not be:
                # `self.board[end_position][1] += 1`
                self.board[end_position][0] += 1

            elif self.board[end_position][0] != self.not_turn:
                self.board[end_position][1] += 1
                self.board[end_position][0] = self.turn
            else:
                # NOTE this will throw an error. Should be 
                # `self.board[self.bar_position[self.not_turn]][1]`
                self.board[self.bar_position(self.not_turn)][1] += 1
                self.board[end_position][0] = self.turn

        # update the move log
        # NOTE replace `move_to_backgammon_notation` method with `__str__`
        # method. Then -> `self.move_log.append(str(move))`
        self.move_log.append(move.move_to_backgammon_notation())

        # update whose turn it is
        # NOTE refactor into method
        self.is_white_turn = not self.is_white_turn

    def get_legal_moves(self, all_moves):
        '''
        applies _get_longest_move and _get_largest_move to finds the legal moves of a given board.
        input: list of all legal moves ignoring the edge cases.

        EDGE CASES: - If the player has pips on the
                        bar then they must be moved first.
                    - If a player can only legally use one of his die then
                        it must be the larger of the two die he can legally use.
                    - The player must use as many of the die as he possibly can
        '''
        pass

    def _get_all_moves(self):
        '''returns all moves given the dice without looking at the edge cases '''
        # NOTE holy moley
        # Definitely shouldn't have methods this deeply nested. Needs to be
        # refactored into bite size chunks.

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
        '''
        when the player has pips on the bar get all the moves that involve moving pips from the bar.
        Should use this at the top of _get_all_moves to improve its efficiency
        '''
        pass

    def _get_largest_move(self, all_moves):
        '''
        - If a player can only legally use one of his die then
            filters the list of moves by removing ones not using the larger of the two die.
        '''
        pass

    def _get_longest_move(self, all_moves):
        '''
        Applies edge case that the player must use as many of the die as he possibly can

        '''
        # NOTE add pass!

    def _get_all_positions(self):
        '''
        Returns the number of pips the turnowner has on each point.
        The first entry is their bar. Doesn't include their homeboard
        '''
        # NOTE these two lines can be one line:
        # all_positions = [self.bar[self.turn]]

        # Also will throw error because you're using curly brackets instead of
        # square brackets.
        all_positions = []
        all_positions.append(self.bar(self.turn))
        board_size = len(self.board)
        # NOTE this can be rewritten like this:
        # `for space in self.board:`
        # Then replace any `self.board[i]` with `space`.
        for i in range(1, board_size):
            if self.board[i][0] == self.turn:
                all_positions.append(self.bar_position[i][1])
            else:
                all_positions.append(0)
        return all_positions

    def _get_dice_to_use(self):
        '''
        Doubles self.dice if the player has rolled doubles
        '''
        # NOTE Doesn't need to be this complicated.
        # ```
        # if self.dice[0] == self.dice[1]:
        #     return [d * 2 for d in self.dice]
        # return self.dice
        # ```
        return [die for die in self.dice] if self.dice[0] != self.dice[1] else [
            die for die in self.dice * 2]

    def _is_available_point(self, point):
        '''
        determines if a given point is available for the player whose turn it is
         '''
        # NOTE what is the rationale behind not throwing an error? Sounds like
        # an error to me. Shouldn't be allowed to pass in incorrect values.

        # when trying to evaluate a point not in the board return False rather than throwing an error
        if point < 0 or point > 24:
            return False
        # NOTE this can just be `if` not `elif`
        # NOTE Should be more self documenting. It's a bit confusing
        # NOTE `if` isn't necessary at all here. Can just return the
        # conditional.
        elif self.board[point][0] in (self.turn, '-') or self.board[point] == [self.not_turn, 1]:
            return True
        return False

    def _add_die_to_pip(self, die, pip):
        '''
        applies the correct function (add/subtract) to a pip
        '''
        if self.turn == 'w':
            return pip + die
        return pip - die


# NOTE Not really sure what this class is all about. Am assuming it's a bit of
# a work in progress.
class Decision():
    def __init__(self, initial_cube_owner, final_cube_owner,
                 initial_cube_value, final_cube_value):
        self.id = 'generate_unique_id'  # ;)
        self.initial_cube_owner = initial_cube_owner
        self.final_cube_owner = final_cube_owner
        self.initial_cube_value = initial_cube_value
        self.final_cube_value = final_cube_value


class Move():
    def __init__(self, player, pip_moves):
        # only need the player to throw the exception.. do we really need it?
        self.id = 'generate_unique_id'
        self.player = player
        self.pip_moves = pip_moves
        self.start_positions = [pip_move[0] for pip_move in pip_moves]
        self.end_positions = [pip_move[1] for pip_move in pip_moves]

    # NOTE I think this should be the `__str__` method for the class
    def move_to_backgammon_notation(self):
        '''
        converts the computer readable backgammon moves into standard bg notation
        I could TYPO remoove player from the init method and have this in the Gamestate class?
        '''
        # NOTE the if and else blocks here share a lot in common. Try putting
        # your mind to simplifying this function. I think using a `dict` could
        # help here.
        if self.player == 'r':
            transformed_pip_moves = []
            for pip_move in self.pip_moves:
                if pip_move[0] == 25:
                    transformed_pip_moves.append(('bar', pip_move[1]))
                elif pip_move[1] == 0:
                    transformed_pip_moves.append((pip_move[0], 'off'))
                else:
                    transformed_pip_moves.append(pip_move)
            bg_notation = Counter(transformed_pip_moves)
        else:
            transformed_pip_moves = []
            for pip_move in self.pip_moves:
                if pip_move[0] == 0:
                    transformed_pip_moves.append((
                        'bar', np.abs(pip_move[1] - 25)))
                elif pip_move[1] == 25:
                    transformed_pip_moves.append(
                        (np.abs(pip_move[0] - 25), 'off'))
                else:
                    transformed_pip_moves.append(
                        tuple(np.abs(np.subtract(pip_move, (25, 25)))))
            bg_notation = Counter(transformed_pip_moves)

        return bg_notation
