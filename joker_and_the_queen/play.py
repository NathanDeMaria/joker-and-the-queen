from typing import Callable

from .ai import BaseAI
from .deck import random_deck
from .game import Game


def play_game(decision_algorithm: Callable[[], BaseAI], n_cards: int = 9) -> int:
    """
    Play one iteration of the game
    """
    algorithm = decision_algorithm()
    deck = random_deck()
    first_board = [deck.pop() for _ in range(n_cards)]
    for card in first_board:
        algorithm.observe(card)
    game = Game.start(first_board)
    while deck:
        choice, position = algorithm.decide(game)
        card = deck.pop()
        game.add_card(card, position, choice)
        algorithm.observe(card)
        if game.is_done:
            return len(deck)
    # 🎉 we made it through the whole deck
    return 0
