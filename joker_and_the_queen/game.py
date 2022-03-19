from enum import Enum, auto

from .deck import Card, Rank


class Choice(Enum):
    """
    Choice of direction when laying a new card
    """
    HIGHER = auto()
    LOWER = auto()
    SAME = auto()

    def flip(self) -> 'Choice':
        """
        Flip to the opposite direction
        """
        if self == Choice.HIGHER:
            return Choice.LOWER
        if self == Choice.LOWER:
            return Choice.HIGHER
        return Choice.SAME


class Game:
    """
    The state of the game board
    """
    def __init__(self, initial_cards: list[Card], initial_card_count: int = 9):
        if len(initial_cards) != initial_card_count:
            raise ValueError(f"Must start with {initial_card_count} cards")
        self._aces_choice: Choice | None = None
        self._board: list[Card | None] = list(initial_cards)

    def add_card(self, card: Card, position: int, choice: Choice):
        """
        Attempt to add a card at a certain position
        """
        assert 0 <= position <= len(self._board), "Must insert onto the board"
        current_card = self._board[position]
        if current_card is None:
            raise ValueError("Cannot insert onto a dead pile")

        # Handle the first ace
        if card.rank is Rank.ACE and self._aces_choice is None:
            if current_card.rank is Rank.ACE:
                raise ValueError("Can't play on an ace until direction is determined")
            self._aces_choice = choice
            self._board[position] = card
            return

        # Placing something on an ace after they're directed
        if current_card.rank is Rank.ACE:
            if self._aces_choice is None:
                raise ValueError("Can't play on an ace until direction is determined")
            self._board[position] = card if choice == self._aces_choice.flip() else None
            return

        # Subsequent aces
        if card.rank is Rank.ACE:
            self._board[position] = card if choice == self._aces_choice else None
            return

        correct_choice = _get_correct_choice(card, current_card)
        self._board[position] = card if correct_choice == choice else None

    @property
    def is_done(self) -> bool:
        """
        True if all of the piles are flipped
        """
        return all(c is None for c in self._board)

    @property
    def board(self) -> list[Card | None]:
        """
        The current state of all the card piles.
        None if a pile is flipped over.
        """
        return self._board

    @property
    def aces_choice(self) -> Choice | None:
        """
        The direction that's correct when laying a card on an ace
        """
        return self._aces_choice


def _get_correct_choice(card: Card, board_card: Card) -> Choice:
    if card.rank == board_card.rank:
        return Choice.SAME
    return Choice.HIGHER if card.rank.value > board_card.rank.value else Choice.LOWER
