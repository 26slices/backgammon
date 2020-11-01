import unittest
from engine import GameState, Decision, Move


class TestEngine(unittest.TestCase):
    w = GameState()
    setattr(w, 'is_white_turn', True)
    w_move = Move('w', [(1, 2), (1, 2)])

    def test_initial_state(self):
        self.assertEqual(self.w.cube, 1)
        self.assertIsNone(self.w.cube_owner)
        self.assertEqual(self.w.turn_number, 0)

    def test_make_move(self):
        self.w.make_move(self.w_move)
        self.assertEqual(self.w.board[1], ['-', 0])
        self.assertEqual(self.w.board[2], ['w', 2])

    def move_to_backgammon_notation(self):
        pass


if __name__ == '__main__':
    unittest.main(exit=False)
