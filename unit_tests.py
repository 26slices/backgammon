import unittest
from engine import GameState, Decision, Move
from constants import (ALL_ROLLS, TEST_ONE_ON_BAR, TEST_TWO_ON_BAR,
                      TEST_LARGESE_MOVE, STARTING_BOARD, TEST_NO_LEGAL_MOVES_BAR,
                      TEST_NO_LEGAL_MOVES_BLOCKED)

        # NEED [(13, 8), (8, 5)] and [(13, 10), (10, 5)] to be the same when neither involve a hit. Can ignore for now.
        # SWAP 'w' AND 'r' for white and red
        # Get tests written out and working

class TestEngine(unittest.TestCase):
    w = GameState()

    def test_initial_state(self):
        self.assertEqual(self.w.cube, 1)
        self.assertIsNone(self.w.cube_owner)
        self.assertEqual(self.w.turn_number, 0)

        print('is whites turn: {}'.format(self.w.is_white_turn))


    def test_moves(self):

        r = GameState()
        setattr(r, 'is_white_turn', False)
        setattr(r, 'board', TEST_LARGESE_MOVE)
        setattr(r, 'dice', [5, 4])

        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_LARGESE_MOVE: {}'.format(moves))
        # # self.assertEqual(moves, [[(21, 16)]])

        setattr(r, 'board', TEST_TWO_ON_BAR)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', [5, 4])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_TWO_ON_BAR: {}'.format(moves))
        self.assertEqual(moves, [[('bar', 21)]])


        setattr(r, 'board', TEST_ONE_ON_BAR)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', [5, 4])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_ONE_ON_BAR: {}'.format(moves))
        # # self.assertEqual(moves, [[('bar', 21), (6, 1)], [('bar', 21), (21, 16)]])


        setattr(r, 'board', STARTING_BOARD)
        setattr(r, 'dice', [5, 3])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for STARTING_BOARD: {}'.format(moves))

        setattr(r, 'board', TEST_NO_LEGAL_MOVES_BAR)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', [5, 6])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_NO_LEGAL_MOVES_BAR: {}'.format(moves))

        setattr(r, 'board', TEST_NO_LEGAL_MOVES_BLOCKED)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', [1, 1])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_NO_LEGAL_MOVES_BLOCKED: {}'.format(moves))




    # def test_make_move(self):
    #     self.w.make_move(self.w_move)
    #     self.assertEqual(self.w.board[1], ['-', 0])
    #     self.assertEqual(self.w.board[2], ['w', 2])



if __name__ == '__main__':
    unittest.main(exit=False)
