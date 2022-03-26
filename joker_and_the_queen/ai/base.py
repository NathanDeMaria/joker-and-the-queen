from abc import ABC, abstractmethod

from ..deck import Card
from ..game import Choice, Game


class BaseAI(ABC):
    """
    Something responsible for choosing a direction/position combination
    """

    @abstractmethod
    def decide(self, game: Game) -> tuple[Choice, int]:
        """
        Pick a location/direction given the game state.
        """
        return NotImplemented

    def observe(self, _: Card):
        """
        Notice that this card has been played (to potentially remember it)
        """
