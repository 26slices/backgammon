import unittest
from engine import GameState, Decision, Move


class TestEngine(unittest.TestCase):
    w = GameState(7, is_white_turn=True)
    w_move = Move('w', [(1, 2), (1, 2)])

    r = GameState(7, is_white_turn=False)
    r_move = Move('r', [(6, 2), (8, 2)])

    setattr(r, 'board', [['r', 0],  # red home board
                         ['w', 1], ['w', 1], [
                             '-', 0], ['-', 0], ['-', 0], ['r', 5],
                         ['-', 0], ['r', 3], ['-', 0], ['-', 0], ['-', 0], ['w', 4],
                         ['r', 5], ['-', 0], ['-', 0], ['-', 0], ['w', 4], ['-', 0],
                         ['w', 5], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['r', 2],
                         ['w', 0]  # white home board
                         ]
            )

    def test_initial_state(self):
        self.assertEqual(self.w.cube, 1)
        self.assertIsNone(self.w.cube_owner)
        self.assertEqual(self.w.turn_number, 0)

    def test_make_move(self):
        self.w.make_move(self.w_move)
        self.assertEqual(self.w.board[1], ['-', 0])
        self.assertEqual(self.w.board[2], ['w', 2])

        self.r.make_move(self.r_move)
        self.assertEqual(self.r.board[2], ['r', 2])
        self.assertEqual(self.r.bar, {'w': 1, 'r': 0})


if __name__ == '__main__':
    unittest.main(exit=False)
