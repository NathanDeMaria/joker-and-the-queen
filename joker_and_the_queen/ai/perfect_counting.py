from collections import Counter
from typing import Counter as CounterType, Iterator

from .base import BaseAI
from ..deck import Card, Rank, random_deck
from ..game import Game, Choice


_ScoredChoice = tuple[float, Choice]


class PerfectCountingAI(BaseAI):
    """
    Perfectly count all cards to actually make the best choice every time
    """

    def __init__(self, possible_cards: list[Card] = None) -> None:
        self._possible_cards = possible_cards or random_deck()

    def decide(self, game: Game) -> tuple[Choice, int]:
        scored_choices = [
            self.score_card(card, game.aces_choice) + (position,)
            for position, card in enumerate(game.board)
            if card is not None
        ]
        winner = max(scored_choices, key=lambda scp: scp[0], default=None)
        if winner is None:
            raise ValueError("Game should've already ended")
        return winner[1:]

    def observe(self, card: Card):
        self._possible_cards.remove(card)

    def score_card(self, card: Card, aces_choice: Choice | None) -> _ScoredChoice:
        """
        Get the best choice for this card,
        and the probability of being correct with that choice.
        """
        if card.rank is Rank.ACE:
            return _score_ace(aces_choice)
        correct_choices: CounterType[Choice] = Counter()
        for possible_card in self._possible_cards:
            choices = _get_correct_choices(possible_card, card, aces_choice)
            for correct_choice in choices:
                correct_choices[correct_choice] += 1
        return _score_counts(correct_choices, len(self._possible_cards))


def _score_ace(aces_choice: Choice | None) -> _ScoredChoice:
    return (-1, Choice.HIGHER) if aces_choice is None else (1, aces_choice.flip())


def _get_correct_choices(
    possible_card: Card, card: Card, aces_choice: Choice | None
) -> Iterator[Choice]:
    if possible_card.rank is Rank.ACE:
        if aces_choice is None:
            yield from Choice
        else:
            yield aces_choice
    elif possible_card.rank.value > card.rank.value:
        yield Choice.HIGHER
    elif possible_card.rank.value < card.rank.value:
        yield Choice.LOWER
    else:
        yield Choice.SAME


def _score_counts(correct_choices: dict[Choice, int], total: int) -> _ScoredChoice:
    scores = [(count / total, choice) for choice, count in correct_choices.items()]
    return max(scores, key=lambda sc: sc[0])
