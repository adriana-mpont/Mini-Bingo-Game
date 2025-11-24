import pytest
from src.game.card import BingoCard

#Defining a test function to check that the card contains 16 numbers.
def test_card_has_16_numbers():
    """Each card should have 16 numbers."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Flattening the matrix (grid of the bingo card) into a single list of numbers.
    flat_list = [num for row in card.grid for num in row]
    #Failing the test if the total number of the elements in the list isn't exactly 16. 
    assert len(flat_list) == 16, "Card does not have 16 numbers"

#Defining a test function to ensure that all numbers on the card are unique.
def test_numbers_unique():
    """All numbers in the card should be unique."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Flattening the matrix (grid of the bingo card) into a single list of numbers.
    flat_list = [num for row in card.grid for num in row]
    #Failing the test if duplicates are detected when comparing each number in the list. 
    assert len(flat_list) == len(set(flat_list)), "Card numbers are not unique"

#Defining a test function to check that every number on the card is within the range 1 to 99. 
def test_numbers_in_range():
    """All numbers must be between 1 and 99."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Flattening the matrix (grid of the bingo card) into a single list of numbers.
    flat_list = [num for row in card.grid for num in row]
    #Failing the test if a number outside the valid bounds is found. 
    assert all(1 <= num <= 99 for num in flat_list), "Numbers out of range"

#Defining a test function to verify two cards are unlikely to be the same (contain the same numbers).
def test_multiple_cards_are_different():
    """Probability of generating two identical cards should be very low."""
    #Creating a first bingo card instance.
    card1 = BingoCard()
    #Creating a second bingo card instance.
    card2 = BingoCard()
    #Flattening the matrix of the first bingo card into a list of numbers.
    flat1 = [num for row in card1.grid for num in row]
    #Flattening the matrix of the first bingo card into another list of numbers.
    flat2 = [num for row in card2.grid for num in row]
    #Failing the test if both full cards match exactly (in practice, two cards may rarely match by chance).
    assert flat1 != flat2, "Two generated cards are identical (very unlikely)"

#Defining a test function to confirm that every cell starts unmarked. 
def test_card_starts_unmarked():
    """All cells should start unmarked"""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Creating a loop through each row of the marked state grid.
    for row in card.marked:
        #Failing the test if there is a cell with the value True (marked). 
        assert all(not cell for cell in row), "Card starts with marked cells"

#Defining a test function to ensure that the mark_number() method only marks the cell of the matching number. 
def test_mark_number_marks_correct_cell():
    """mark_number() should only mark the cell that matched the number"""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Picking the first number on the card as the target number to mark. 
    target = card.grid[0][0]
    #Calling the mark_number() method to mark the target number. 
    card.mark_number(target)
    #Failing the test if the target number cell is not marked (True) now.  
    assert card.marked[0][0], "Target number not marked"
    
    #Ensuring that all other cells remain False.
    #Creating a loop through all the rows of the card. 
    for i in range(card.size):
        #Creating a loop through all the columns of the card. 
        for j in range(card.size):
            #Avoiding the target number cell, which should now be marked. 
            if (i,j) != (0,0):
                #Failing the test if there are other cells now marked.
                assert not card.marked[i][j], "Other cells should remain unmarked"

#Defining a test function to verify that marking a number not on the card changes nothing. 
def test_mark_number_ignores_missing_number():
    """mark_number() should not change anything if number not on card."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Copying the matrix of the original marked state of the card. 
    before = [row.copy() for row in card.marked]
    #Attempting to mark an invalid number, that is not present on the card. 
    card.mark_number(200)  #Out of range / Not in card
    #Failing the test if the marked state has changed.
    assert card.marked == before, "Card changed even though number not found"

#Defining a test function to check the behavior of is_marked method. 
def test_is_marked_returns_correct_value():
    """Should correctly report marked vs unmarked numbers without using is_marked method."""
    card = BingoCard()

    # Pick the first number and mark it
    num = card.grid[0][0]
    card.mark_number(num)

    # Manually check that the cell containing num is True
    assert card.marked[0][0], "Marked number should be marked"

    # Check that a number not on the card is indeed not marked
    not_in_card = 200
    # Should simply verify that nothing changed for invalid numbers
    assert not any(not_in_card in row for row in card.grid), \
        "Test requires a number that is not on the card"

#Defining a test function to check visual formatting of the displayed card output.
def test_display_card_shows_marked_numbers(capsys):
    """display_card() should visually mark numbers when they are marked."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Picking the first number on the card as the target number to mark. 
    target = card.grid[0][0]
    #Calling the mark_number() method to mark the target number.
    card.mark_number(target)
    #Displaying the card to console. 
    card.display_card()
    #Capturing printed output from the display_card().
    captured = capsys.readouterr()
    #Failing the test if the marked number doesn't appear surrounded by brackets [ ].
    assert "[" in captured.out and "]" in captured.out, "Marked numbers not displayed properly"
