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

def test_card_starts_unmarked():
    """All cells should start unmarked"""
    card = BingoCard()
    for row in card.marked:
        assert all(not cell for cell in row), "Card starts with marked cells"

def test_mark_number_marks_correct_cell():
    """mark_number() should only mark the cell that matched the number"""
    card = BingoCard()
    target = card.grid[0][0]
    card.mark_number(target)
    assert card.marked[0][0], "Target number not marked"
    
    #All other cells remain False
    for i in range(card.size):
        for j in range(card.size):
            if (i,j) != (0,0):
                assert not card.marked[[i][j]], "Other cells should remain unmarked"

def test_mark_number_ignores_missing_number():
    """mark_number() should not change anything if number not on card."""
    card = BingoCard()
    before = [row.copy() for row in card.marked]
    card.mark_number(200)  #Out of range / Not in card
    assert card.marked == before, "Card changed even though number not found"

def test_is_marked_returns_correct_value():
    """is_marked() should report True only for marked numbers."""
    card = BingoCard()
    num = card.grid[0][0]
    card.mark_number(num)
    assert card.is_marked(num), "is_marked() failed for a marked number"
    # Some random number not in the card should be False
    not_in_card = 200
    assert not card.is_marked(not_in_card), "is_marked() returned True for number not on card"

def test_display_card_shows_marked_numbers(capsys):
    """display_card() should visually mark numbers when they are marked."""
    card = BingoCard()
    target = card.grid[0][0]
    card.mark_number(target)
    card.display_card()
    captured = capsys.readouterr()
    # The marked number should appear surrounded by brackets [NN]
    assert "[" in captured.out and "]" in captured.out, "Marked numbers not displayed properly"
