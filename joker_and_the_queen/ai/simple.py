import random

from .base import BaseAI
from ..deck import Rank
from ..game import Game, Choice


_CENTER = (Rank.KING.value + Rank.TWO.value) / 2
_ACE_HIGH_CENTER = (Rank.KING.value + 1 + Rank.TWO.value) / 2
_ACE_LOW_CENTER = (Rank.KING.value + Rank.ACE.value) / 2


def _get_center(aces_choice: Choice | None) -> float:
    if aces_choice == Choice.LOWER:
        return _ACE_LOW_CENTER
    if aces_choice == Choice.HIGHER:
        return _ACE_HIGH_CENTER
    return _CENTER


class SimpleAI(BaseAI):
    """
    Algorithm that just knows if aces are high,
    and otherwise decides as if it couldn't counting any cards
    """

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def decide(self, game: Game) -> tuple[Choice, int]:
        center = _get_center(game.aces_choice)

        best_index = None
        best_diff = None
        for i, card in enumerate(game.board):
            if card is None:
                continue
            diff = _get_diff(center, card.rank, game.aces_choice)
            if diff is None:
                continue
            if best_diff is None or abs(diff) > abs(best_diff):
                best_diff = diff
                best_index = i
        if best_index is None or best_diff is None:
            raise ValueError("Ummm...game should be over by now")
        if best_diff > 0:
            choice = Choice.HIGHER
        elif best_diff < 0:
            choice = Choice.LOWER
        else:
            choice = random.choice([Choice.HIGHER, Choice.LOWER])
        return choice, best_index


def _get_diff(center: float, rank: Rank, aces_direction: Choice | None) -> float | None:
    if rank == Rank.ACE:
        if aces_direction is None:
            return None
        if aces_direction is Choice.HIGHER:
            return center - Rank.KING.value - 1
        return center - Rank.ACE.value
    return center - rank.value
