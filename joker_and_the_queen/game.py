from enum import Enum, auto

from .deck import Card, Rank


class Choice(Enum):
    """
    Choice of direction when laying a new card
    """

    HIGHER = auto()
    LOWER = auto()
    SAME = auto()

    def flip(self) -> "Choice":
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

    def __init__(self, initial_cards: list[Card | None], aces_choice: Choice | None):
        self._board: list[Card | None] = initial_cards
        self._aces_choice: Choice | None = aces_choice

    @classmethod
    def start(cls, initial_cards: list[Card]) -> "Game":
        """
        Initialize a game
        """
        return cls(list(initial_cards), None)

    def add_card(self, card: Card, position: int, choice: Choice):
        """
        Attempt to add a card at a certain position
        """
        current_card = self._get_current_card(position)
        is_valid = self._check_valid_placement(current_card, card, choice)
        self._board[position] = card if is_valid else None

    def _check_valid_placement(
        self, current_card: Card, card: Card, choice: Choice
    ) -> bool:
        # The card getting flipped is an ace
        if card.rank is Rank.ACE:
            return self._handle_flipped_ace(current_card, choice)

        # Placing something on an ace after they're directed
        # This is basically always correct in practice
        # ...unless you went rogue and said "same"
        # or forget the ace direction
        if current_card.rank is Rank.ACE:
            return self._handle_play_on_an_ace(choice)

        return _get_correct_choice(card, current_card) == choice

    def _handle_play_on_an_ace(self, choice: Choice) -> bool:
        if self._aces_choice is None:
            raise ValueError("Can't play on an ace until direction is determined")
        return choice == self._aces_choice.flip()

    def _handle_flipped_ace(self, current_card: Card, choice: Choice) -> bool:
        if self._aces_choice is None:
            if current_card.rank is Rank.ACE:
                raise ValueError("Can't play on an ace until direction is determined")
            self._aces_choice = choice
            return True
        # It's not the first ace
        return choice == self._aces_choice

    def _get_current_card(self, position: int) -> Card:
        assert 0 <= position <= len(self._board), "Must insert onto the board"
        current_card = self._board[position]
        if current_card is None:
            raise ValueError("Cannot insert onto a dead pile")
        return current_card

    @property
    def is_done(self) -> bool:
        """
        True if all of the piles are flipped
        """
        if all(c is None for c in self._board):
            # All are flipped
            return True
        # If it's only aces left, and aces haven't been directed yet, it's over?
        if self._aces_choice is not None:
            return False
        return all(c is None or c.rank is Rank.ACE for c in self._board)

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
    """
    Get the correct choice when neither card was an ace
    """
    if card.rank == board_card.rank:
        return Choice.SAME
    return Choice.HIGHER if card.rank.value > board_card.rank.value else Choice.LOWER
