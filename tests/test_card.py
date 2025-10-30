import pytest
from src.game.card import BingoCard


def test_card_has_16_numbers():
    """Each card should have 16 numbers."""
    card = BingoCard()
    flat_list = [num for row in card.grid for num in row]
    assert len(flat_list) == 16, "Card does not have 16 numbers"


def test_numbers_unique():
    """All numbers in the card should be unique."""
    card = BingoCard()
    flat_list = [num for row in card.grid for num in row]
    assert len(flat_list) == len(set(flat_list)), "Card numbers are not unique"


def test_numbers_in_range():
    """All numbers must be between 1 and 99."""
    card = BingoCard()
    flat_list = [num for row in card.grid for num in row]
    assert all(1 <= num <= 99 for num in flat_list), "Numbers out of range"


def test_multiple_cards_are_different():
    """Probability of generating two identical cards should be very low."""
    card1 = BingoCard()
    card2 = BingoCard()
    flat1 = [num for row in card1.grid for num in row]
    flat2 = [num for row in card2.grid for num in row]
    # In practice, 2 cards may rarely match by chance, so allow test to pass if different
    assert flat1 != flat2, "Two generated cards are identical (very unlikely)"
