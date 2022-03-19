from .simple import SimpleAI
from ..deck import Card, Rank, Suit
from ..game import Game, Choice


_SIMPLE_START = [
    Card(Suit.CLUBS, Rank.ACE),
    Card(Suit.CLUBS, Rank.TWO),
    Card(Suit.CLUBS, Rank.THREE),
    Card(Suit.CLUBS, Rank.FOUR),
    Card(Suit.CLUBS, Rank.FIVE),
    Card(Suit.CLUBS, Rank.SIX),
    Card(Suit.CLUBS, Rank.SEVEN),
    Card(Suit.CLUBS, Rank.EIGHT),
    Card(Suit.CLUBS, Rank.NINE),
]


def test_picks_the_best():
    game = Game.start(_SIMPLE_START)
    ai = SimpleAI()
    choice, position = ai.decide(game)
    assert position == 1
    assert choice == Choice.HIGHER


def test_chooses_ace_if_available():
    game = Game(_SIMPLE_START, Choice.HIGHER)
    ai = SimpleAI()

    choice, position = ai.decide(game)
    assert choice == Choice.LOWER
    assert position == 0


def test_middle_before_aces():
    # If aces are still free, choose higher than 7, lower than 8
    ai = SimpleAI()
    game = Game([Card(Suit.HEARTS, Rank.SEVEN)], None)
    choice, _ = ai.decide(game)
    assert choice == Choice.HIGHER

    game = Game([Card(Suit.HEARTS, Rank.EIGHT)], None)
    choice, _ = ai.decide(game)
    assert choice == Choice.LOWER


def test_is_aware_of_aces_high():
    # If aces are high, 8's are the center
    ai = SimpleAI(seed=18)
    game = Game([Card(Suit.HEARTS, Rank.EIGHT)], Choice.HIGHER)
    choices = [ai.decide(game)[0] for _ in range(5)]

    # It's random, so I just looked up what it'd decide with this seed
    # The interesting bit is that there's some of each
    expected = [Choice.HIGHER, Choice.HIGHER, Choice.LOWER, Choice.LOWER, Choice.HIGHER]
    assert choices == expected


def test_is_aware_of_aces_low():
    # If aces are low, 7's are the center
    ai = SimpleAI(seed=18)
    game = Game([Card(Suit.HEARTS, Rank.SEVEN)], Choice.LOWER)
    choices = [ai.decide(game)[0] for _ in range(5)]

    # It's random, so I just looked up what it'd decide with this seed
    # The interesting bit is that there's some of each
    expected = [Choice.HIGHER, Choice.HIGHER, Choice.LOWER, Choice.LOWER, Choice.HIGHER]
    assert choices == expected
