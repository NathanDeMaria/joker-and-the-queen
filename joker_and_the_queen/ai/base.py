from abc import ABC, abstractmethod

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
