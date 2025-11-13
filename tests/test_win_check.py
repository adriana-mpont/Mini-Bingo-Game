import pytest
from src.game.card import BingoCard

def test_check_line_horizontal():
    """Test that a horizontal line is correctly detected."""
    card = BingoCard()
    # Mark a full horizontal line (first row)
    card.marked[0] = [True, True, True, True]
    assert card.check_line() == True

def test_check_line_vertical():
    """Test that a vertical line is correctly detected."""
    card = BingoCard()
    # Mark a full vertical line (second column)
    for i in range(4):
        card.marked[i][1] = True
    assert card.check_line() == True

def test_check_line_none():
    """Test that no line returns False."""
    card = BingoCard()
    # No line is fully marked
    card.marked[0][0] = True
    card.marked[1][1] = True
    card.marked[2][2] = True
    card.marked[3][3] = True
    assert card.check_line() == False

def test_check_bingo_full():
    """Test that Bingo is detected when all numbers are marked."""
    card = BingoCard()
    card.marked = [[True]*4 for _ in range(4)]
    assert card.check_bingo() == True

def test_check_bingo_partial():
    """Test that Bingo is not detected when only part of the card is marked."""
    card = BingoCard()
    card.marked[0][0] = True
    card.marked[1][1] = True
    card.marked[2][2] = True
    card.marked[3][3] = True
    assert card.check_bingo() == False

def test_line_and_bingo_combined():
    """Test that a line is detected before full Bingo."""
    card = BingoCard()
    # Mark a full first row
    card.marked[0] = [True, True, True, True]
    # Mark some other cells (not full card)
    card.marked[1][0] = True
    card.marked[2][1] = True
    card.marked[3][2] = True

    assert card.check_line() == True
    assert card.check_bingo() == False

def test_check_line_almost_full_row():
    """A row with only 3 marked cells should not count as a line."""
    card = BingoCard()
    card.marked[0] = [True, True, True, False]
    assert card.check_line() == False

def test_check_line_diagonal_not_valid():
    """Diagonal marks should not count as a line."""
    card = BingoCard()
    for i in range(4):
        card.marked[i][i] = True
    assert card.check_line() == False
