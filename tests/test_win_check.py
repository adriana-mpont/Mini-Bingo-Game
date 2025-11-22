import pytest
from src.game.card import BingoCard

#Defining a test function to verify horizontal line detection.
def test_check_line_horizontal():
    """Test that a horizontal line is correctly detected."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking the entire first row (True) to simulate completing a line.
    card.marked[0] = [True, True, True, True]
    #Failing the test if check_line() does not detect the completed line.
    assert card.check_line() == True

#Defining a test function to verify vertical line detection.
def test_check_line_vertical():
    """Test that a vertical line is correctly detected."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking the entire second column (True) to simulate completing a line.
    #Creating a loop over all 4 rows. 
    for i in range(4):
        #Marking the second column (index 1) to form a vertical line
        card.marked[i][1] = True
    #Failing the test if check_line() does not detect the completed line.
    assert card.check_line() == True

#Defining a test function to verify that if a line is not complete, no valid line is detected. 
def test_check_line_none():
    """Test that no line returns False."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Marking the numbers diagonally, so no full row or columns is created (marked).
    card.marked[0][0] = True
    card.marked[1][1] = True
    card.marked[2][2] = True
    card.marked[3][3] = True
    #Failing the test if line is incorrectly detected (since no line is complete on the card).
    assert card.check_line() == False

#Defining a test function to check full card bingo detection.
def test_check_bingo_full():
    """Test that Bingo is detected when all numbers are marked."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking every cell in the 4x4 grid.
    card.marked = [[True]*4 for _ in range(4)]
    #Failing the test if bingo is not detected as expected. 
    assert card.check_bingo() == True

#Defining a test function to ensure that if the card is only partially marked, it doesn't cound as full bingo detection.
def test_check_bingo_partial():
    """Test that Bingo is not detected when only part of the card is marked."""
     #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking some cells on the card. 
    card.marked[0][0] = True
    card.marked[1][1] = True
    card.marked[2][2] = True
    card.marked[3][3] = True
    #Failing the test if this partial marking is detected as bingo.
    assert card.check_bingo() == False

#Defining a test function to cover both line and bingo conditions together.
def test_line_and_bingo_combined():
    """Test that a line is detected before full Bingo."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking the entire first row (True) to simulate completing a line.
    card.marked[0] = [True, True, True, True]
    #Manually marking some other cells on the card, but not enough to complete the card. 
    card.marked[1][0] = True
    card.marked[2][1] = True
    card.marked[3][2] = True

    #Failing the test if line is not detected (as a complete line exists on the card). 
    assert card.check_line() == True
    #Failing the test if bingo is detected (as the card is not complete).
    assert card.check_bingo() == False

#Defining a test function to verify that if there is an incomplete row on the card, no valid line is detected.
def test_check_line_almost_full_row():
    """A row with only 3 marked cells should not count as a line."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking the first row with only 3 of 4 cells completed. 
    card.marked[0] = [True, True, True, False]
    #Failing the test if line is incorrectly detected (since no line is complete on the card).
    assert card.check_line() == False

#Defining a test function to verify that diagonal marking of cells is not considered a line.
def test_check_line_diagonal_not_valid():
    """Diagonal marks should not count as a line."""
    #Creating a new bingo card instance.
    card = BingoCard()
    Creating a loop across the grid indices.
    for i in range(4):
        #Manually marking a diagonal from top left to bottom right.
        card.marked[i][i] = True
    #Failing if the diagonal numbers marder are recognized as winning lines. 
    assert card.check_line() == False
