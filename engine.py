"""
This class is for stroing the current state of the game. It will also determine
all legal moves and provide a game log.
"""


class GameState():
    def __init__(self):
        # self.board describes how many of each side are on a given point on the
        # board the first integer in each tuple represents the number of white
        # checkers in that position, the second integer in each tuple represents
        # the number of red checkers in that position
        #
        self.board() = [(0, 0),  # red home board
                        (2, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 5),
                        (0, 0), (0, 3), (0, 0), (0, 0), (0, 0), (5, 0),
                        (0, 0),  # the bar
                        (0, 5), (0, 0), (0, 0), (0, 0), (3, 0), (0, 0),
                        (5, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 2),
                        (0, 0)]  # white home board

        self.score() = (0, 0)

        self.first_to() = first_to

        self.crawford() = False

        self.cube() = 0

        self.cube_owner() = None
