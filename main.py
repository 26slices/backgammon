from backgammon import engine
import random

def main():

    game = engine.Game()

    while game.score[0] < game.first_to and game.score[1] < game.first_to:
        pass
        # game getsupdated

        game.advance_state()
