from .perfect_counting import PerfectCountingAI
from ..deck import Card, Suit, Rank
from ..game import Choice


def test_simple_score():
    ai = PerfectCountingAI([Card(Suit.HEARTS, Rank.THREE)])
    score, choice = ai.score_card(Card(Suit.HEARTS, Rank.TWO), None)

    # Only card left is a 3, so 1.0 it's higher
    assert score == 1.0
    assert choice == Choice.HIGHER


def test_middle_score():
    ai = PerfectCountingAI(
        [
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.HEARTS, Rank.FIVE),
        ]
    )
    score, choice = ai.score_card(Card(Suit.HEARTS, Rank.FOUR), None)

    # 2/3 of the remaining cards are lower
    assert score == 2 / 3
    assert choice == Choice.LOWER


def test_unbound_aces_are_perfect():
    ai = PerfectCountingAI([Card(Suit.HEARTS, Rank.ACE), Card(Suit.HEARTS, Rank.SEVEN)])
    score, _ = ai.score_card(Card(Suit.HEARTS, Rank.FIVE), None)
    assert score == 1


def test_low_aces_are_low():
    ai = PerfectCountingAI(
        [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.HEARTS, Rank.SEVEN),
        ]
    )
    score, choice = ai.score_card(Card(Suit.HEARTS, Rank.FIVE), Choice.LOWER)
    assert score == 2 / 3
    assert choice == Choice.LOWER


def test_play_low_if_aces_high():
    ai = PerfectCountingAI([Card(Suit.HEARTS, Rank.TWO)])
    score, choice = ai.score_card(Card(Suit.HEARTS, Rank.ACE), Choice.HIGHER)
    assert score == 1.0
    assert choice == Choice.LOWER
