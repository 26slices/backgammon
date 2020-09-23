from engine import GameState, Move

x = Move('w', [(1, 2), (1, 2)])
print(x.player, x.start_positions, x.end_positions)
y = GameState(7, is_white_turn=True)
print(y.show_state())
print(y.turn)
print(x.start_positions)
print((y.board[1][1]) > 1)
y.make_move(x)
print(y.move_to_backgammon_notation(x))
print(y.show_state())
print(y.move_log)
