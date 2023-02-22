import random


def find_random_move(valid_moves):
    if valid_moves:
        random_move = random.choice(valid_moves)
        return random_move
    return None
