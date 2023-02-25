import random


def find_random_move(valid_moves):
    if valid_moves:
        random_move = random.choice(valid_moves)
        return random_move
    return None


def no_doubles(valid_decisions):
    no_double = [
        decision for decision in valid_decisions if decision.decision_type == 'no double'][0]
    return no_double


def find_random_decision(valid_decisions):
    if valid_decisions:
        random_decision = random.choice(valid_decisions)
        return random_decision
    return None
