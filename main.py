from backgammon import engine
# Unused import
import random

def main():

    game = engine.GameState()
    # NOTE Would be cleaner to add a property to the game class called
    # `game_is_over` or something.
    while game.score[0] < game.first_to and game.score[1] < game.first_to:
        pass
