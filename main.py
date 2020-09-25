from backgammon import engine
import random

def main():

    game = engine.GameState()
    while game.score[0] < game.first_to and game.score[1] < game.first_to:
        pass
