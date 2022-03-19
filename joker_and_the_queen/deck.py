import random
from enum import Enum, auto
from typing import NamedTuple


class Suit(Enum):
    """
    The suit of the card.
    This isn't actually useful unless you wanna be cute and ask, "which two"?
    """

    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()


class Rank(Enum):
    """
    The value on the card
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card(NamedTuple):
    """
    A card in the deck
    """

    suit: Suit
    rank: Rank


_DECK = []
for suit in Suit:
    _DECK += [Card(suit, rank) for rank in Rank]


def random_deck() -> list[Card]:
    """
    Draw from a deck of cards in a random order
    """
    deck_copy = _DECK.copy()
    random.shuffle(deck_copy)
    return deck_copy
