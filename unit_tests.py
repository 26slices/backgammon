import unittest
from engine import GameState, Decision, Move
from constants import ALL_ROLLS, TEST_ONE_ON_BAR, TEST_TWO_ON_BAR, TEST_LARGESE_MOVE, STARTING_BOARD

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
    #     # print(self.w.get_all_moves())

    # def test_legal_moves(self):
    #     '''
    #     finds legal moves for all opening rolls. Eventually will loop through roll for roll in ALL_ROLLS.
    #     '''
    #     print('Dice: {}'.format(self.w.dice))
    #     print('is whites turn: {}'.format(self.w.is_white_turn))
    #     test_space = self.w.players_spaces[self.w.turn][0]

    #     print('test_space position number: {}'.format(test_space.position_number))
    #     die = self.w.dice[0]
    #     print('adding first die ({}) to test_space gives you: {}'.format(die, self.w._add_die_to_space(test_space, die)))

    #     self.w.get_all_moves()


    def test_moves(self):

        r = GameState()
        setattr(r, 'is_white_turn', True)
        setattr(r, 'board', TEST_LARGESE_MOVE)
        setattr(r, 'dice', [5, 4])

        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation: {}'.format(moves))
        # self.assertEqual(moves, [[(21, 16)]])

        setattr(r, 'board', TEST_TWO_ON_BAR)
        setattr(r, 'is_white_turn', False)
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation: {}'.format(moves))
        # self.assertEqual(moves, [[('bar', 21)]])


        setattr(r, 'board', TEST_ONE_ON_BAR)
        setattr(r, 'is_white_turn', False)
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]
        print('****************** Moves in bg notation: {}'.format(moves))
        # self.assertEqual(moves, [[('bar', 21), (6, 1)], [('bar', 21), (21, 16)]])



        setattr(r, 'board', STARTING_BOARD)
        # setattr(r, 'dice', [5, 3])
        moves = [move.move_to_backgammon_notation() for move in r.get_all_moves()]

        print('****************** Moves in bg notation: {}'.format(moves))




    # def test_make_move(self):
    #     self.w.make_move(self.w_move)
    #     self.assertEqual(self.w.board[1], ['-', 0])
    #     self.assertEqual(self.w.board[2], ['w', 2])



if __name__ == '__main__':
    unittest.main(exit=False)
