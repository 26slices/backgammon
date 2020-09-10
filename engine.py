"""
This class is for stroing the current state of the game. It will also determine
all legal moves and provide a game log.
"""


class GameState():
    def __init__(self, first_to):
    ''' self.board describes how many and whose pieces are on a given point on
     the board. The first item in each tuple represents the player whose
     pieces are in that position and the second is the number of checkers in
      that position. The exception is the bar which has 0 pieces initially
      but can hold pips from both players simultaneously. '''

        self.board = [('r', 0),  # red player's home board
                    ('w', 2), ('-', 0), ('-', 0), ('-', 0), ('-', 0), ('r', 5),
                    ('-', 0), ('r', 3), ('-', 0), ('-', 0), ('-', 0), ('w', 5),
                    (0, 0),  # the bar
                    ('r', 5), ('-', 0), ('-', 0), ('-', 0), ('w', 3), ('-', 0),
                    ('w', 5), ('-', 0), ('-', 0), ('-', 0), ('-', 0), ('r', 2),
                    ('w', 0)]  # white player's home board

      self.home = (0, 0)

      self.bar = (0, 0)

      self.score = (0, 0)

      self.first_to = first_to

      self.crawford = False

      self.post_crawford = False

      self.cube = 0

      self.cube_owner = None

      self.white_turn = None

      self.dice = None

      self.cube_decision = False

      self.move_log = []

  @property
  def white_on_bar(self):
    return self.bar[0] > 0

  @property
  def red_on_bar(self):
    return self.bar[1] > 0

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
                                       self.crawford, self.post_crawford, self.cube,
                                       self.cube_owner, self.turn, self.dice)
    return state

  def make_move(self, move):
    if move.double_offered:
      self.cube_decision = True



   # self.board[move.start_pos] -= 1



class Move():
  def __init__(self, player, turn_number):
    self.id
    self.turn_number
    self.player
    self.double_offered = False
    self.double_accepted = False
    self.movements = []
    self.dice = None

  def generate_dice_value():
    pass

  def add_movement():
    '''accepts a single instance of a Movement and passes to the movements attribute'''
    pass

  @property
  def remaining_movements(self):
    '''
calculates the number of individual dice moves remaining to use
    '''
    return self._foo
