import unittest
from engine import GameState, Decision, Move
import move_finder as mf
import constants as c

# NEED [(13, 8), (8, 5)] and [(13, 10), (10, 5)] to be the same when neither involve a hit. Can ignore for now.


class TestEngine(unittest.TestCase):
    w = GameState()

    def test_initial_state(self):
        self.assertEqual(self.w.cube, 1)
        self.assertIsNone(self.w.cube_owner)
        self.assertEqual(self.w.turn_number, 0)

        print('is whites turn: {}'.format(self.w.is_white_turn))

    def test_find_moves(self):

        r = GameState()
        print(r.print_board)
        setattr(r, 'is_white_turn', False)

        # ideally [(13, 8), (8, 5)] and  [(13, 10), (10, 5)] would both read: [(13, 5)], but for now it's a nice to have
        setattr(r, 'board', c.STARTING_BOARD)
        setattr(r, 'dice', [5, 3])
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for STARTING_BOARD: {}'.format(moves))

        # here red can only move the pip on the 21 space. because the 12 space is blocked red must play the larger of the two dice, 5: 21 - 16
        setattr(r, 'board', c.TEST_LARGESE_MOVE)
        setattr(r, 'dice', c.TEST_LARGESE_MOVE_DICE_5_4)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_LARGESE_MOVE: {}'.format(moves))
        self.assertEqual(moves, [[(21, 16)]])

        # here red has one pip on the bar which he has to move with the 4. He then has 2 options to play the 5, 21-16 and 6-1.
        setattr(r, 'board', c.TEST_ONE_ON_BAR)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', c.TEST_ONE_ON_BAR_DICE_5_4)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for TEST_ONE_ON_BAR: {}'.format(moves))
        self.assertEqual(
            moves, [[('bar', 21), (6, 1)], [('bar', 21), (21, 16)]])

        # here red has 2 pips on the bar and can only bring one in. therefore his only legal move is the move whihc brings that one in: bar-21
        setattr(r, 'board', c.TEST_TWO_ON_BAR)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', c.TEST_TWO_ON_BAR_DICE_5_4)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for TEST_TWO_ON_BAR: {}'.format(moves))
        self.assertEqual(moves, [[('bar', 21)]])

        # here red has all his pips in the bearoff zone including pips on the 2,3 and 4.
        setattr(r, 'board', c.TEST_BEAROFF_1)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', c.TEST_BEAROFF_1_DICE_3_2)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for TEST_BEAROFF_1: {}'.format(moves))
        self.assertEqual(
            moves, [[(3, 'bearoff_zone'), (3, 1)], [
                (3, 'bearoff_zone'), (2, 'bearoff_zone')],
                [(3, 'bearoff_zone'), (4, 2)], [(4, 1), (2, 'bearoff_zone')], [(4, 1), (3, 1)]])

        # here red has all his pips in the bearoff zone spaces 1 and 2. He can use the 3 and 5 to bearoff pips in the 2.
        setattr(r, 'board', c.TEST_BEAROFF_2)
        setattr(r, 'dice', c.TEST_BEAROFF_2_DICE_3_5)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for TEST_BEAROFF_1: {}'.format(moves))
        self.assertEqual(
            moves, [[(2, 'bearoff_zone'), (2, 'bearoff_zone')]])

        # here red has all his pips in the bearoff zone spaces 1 and 2. He can use the 5 and 5 to bearoff pips 4 in the 2.
        setattr(r, 'board', c.TEST_DOUBLES_BEAROFF)
        setattr(r, 'dice', c.TEST_DOUBLES_BEAROFF_DICE_5_5)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print(
            '****************** Moves in bg notation for TEST_DOUBLES_BEAROFF: {}'.format(moves))
        self.assertEqual(
            moves, [[(2, 'bearoff_zone'), (2, 'bearoff_zone'), (2, 'bearoff_zone'), (2, 'bearoff_zone')]])

        setattr(r, 'board', c.TEST_DOUBLES_BEAROFF_STARTING_OUTSIDE_HOMEBOARD)
        setattr(r, 'dice', [6, 6])
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_DOUBLES_BEAROFF_STARTING_OUTSIDE_HOMEBOARD: {}'.format(moves))
        self.assertEqual(
            moves, [[(20, 14), (14, 8), (8, 2), (3, 'bearoff_zone')]])

        setattr(r, 'board', c.TEST_BEAROFF_BUG)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', c.TEST_BEAROFF_BUG_4_1)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print([move.space_moves for move in r.get_all_moves()])
        print(
            '****************** Moves in bg notation for TEST_BEAROFF_BUG: {}'.format(moves))

        setattr(r, 'board', c.TEST_NEGATIVE_OUTER_SPACE_BUG)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', c.TEST_NEGATIVE_OUTER_SPACE_BUG_DICE_6_6)
        print(r.print_board)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print([move.space_moves for move in r.get_all_moves()])
        print('****************** Moves in bg notation for TEST_NEGATIVE_OUTER_SPACE_BUG: {}'.format(moves))

        # white is on the bar and rolls a 5,6 , but red is blocking those spaces.
        setattr(r, 'board', c.TEST_NO_LEGAL_MOVES_BAR)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', c.TEST_NO_LEGAL_MOVES_BAR_DICE_5_6)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_NO_LEGAL_MOVES_BAR: {}'.format(moves))
        self.assertEqual(
            moves, [])

# all white's pips are on the 1 space and all reds are on the 2 space. white rolls 1,1 and so is blocked.
        setattr(r, 'board', c.TEST_NO_LEGAL_MOVES_BLOCKED)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', c.TEST_NO_LEGAL_MOVES_BLOCKED_DICE_1_1)
        moves = [move.move_to_backgammon_notation()
                 for move in r.get_all_moves()]
        print('****************** Moves in bg notation for TEST_NO_LEGAL_MOVES_BLOCKED: {}'.format(moves))
        self.assertEqual(
            moves, [])

    def test_make_moves(self):
        # testing make random move
        r = GameState()

        setattr(r, 'board', c.STARTING_BOARD)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', [5, 3])
        moves = r.get_all_moves()
        print(r.print_board)
        random_move = mf.find_random_move(moves)
        print('The random move was: {}'.format(
            random_move.move_to_backgammon_notation()))
        r.make_move(random_move)
        print(r.print_board)
        self.assertEqual(1, 1)

        setattr(r, 'board', c.TEST_BEAROFF_1)
        setattr(r, 'is_white_turn', False)
        setattr(r, 'dice', c.TEST_BEAROFF_1_DICE_3_2)
        moves = r.get_all_moves()
        print(r.print_board)
        random_move = mf.find_random_move(moves)
        print('The random move was: {}'.format(
            random_move.move_to_backgammon_notation()))
        r.make_move(random_move)
        print(r.print_board)

        # want to test three things.
        # One: hit and run: 24, 21(hit); 21,20
        # Two: hit and dodge: 24,23; 23,20
        # three: hit and stay: 24,21(hit); 24,23
        setattr(r, 'board', c.TEST_HIT_PIECE)
        setattr(r, 'is_white_turn', True)
        setattr(r, 'dice', c.TEST_HIT_PIECE_3_1)
        moves = r.get_all_moves()
        print(r.print_board)
        random_move = mf.find_random_move(moves)
        print('The random move was: {}'.format(
            random_move.move_to_backgammon_notation()))
        r.make_move(random_move)
        print(r.print_board)


if __name__ == '__main__':
    unittest.main(exit=False)
