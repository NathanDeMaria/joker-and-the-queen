from .deck import Card, Rank, Suit
from .game import Game, Choice

_SIMPLE_START = [
    Card(Suit.CLUBS, Rank.TWO),
    Card(Suit.CLUBS, Rank.THREE),
    Card(Suit.CLUBS, Rank.FOUR),
    Card(Suit.CLUBS, Rank.FIVE),
    Card(Suit.CLUBS, Rank.SIX),
    Card(Suit.CLUBS, Rank.SEVEN),
    Card(Suit.CLUBS, Rank.EIGHT),
    Card(Suit.CLUBS, Rank.NINE),
    Card(Suit.CLUBS, Rank.TEN),
]


def test_wrong_choice_closes_slot():
    game = Game(_SIMPLE_START)
    game.add_card(Card(Suit.HEARTS, Rank.TEN), 0, Choice.LOWER)
    assert game.board[0] is None


def test_correct_choice_sets_card():
    game = Game(_SIMPLE_START)
    set_rank = Rank.TEN
    game.add_card(Card(Suit.HEARTS, set_rank), 0, Choice.HIGHER)
    assert game.board[0].rank == set_rank


def test_place_on_a_decided_ace():
    game = Game(_SIMPLE_START)
    position = 0
    # An ace is laid when saying "higher", so aces are high
    game.add_card(Card(Suit.HEARTS, Rank.ACE), position, Choice.HIGHER)
    # Lay a two on the ace as a "lower", which is correct
    game.add_card(Card(Suit.HEARTS, Rank.TWO), position, Choice.LOWER)
    assert game.board[position] is not None


def test_second_ace_appears():
    game = Game(_SIMPLE_START)
    # An ace is laid when saying "higher", so aces are high
    game.add_card(Card(Suit.HEARTS, Rank.ACE), 0, Choice.HIGHER)
    # Second ace shows up when looking for a higher card is good
    game.add_card(Card(Suit.CLUBS, Rank.ACE), 1, Choice.HIGHER)
    assert game.board[1] is not None
    # Third ace shows up when looking for a lower card, bad
    game.add_card(Card(Suit.SPADES, Rank.ACE), 2, Choice.LOWER)
    assert game.board[2] is None
