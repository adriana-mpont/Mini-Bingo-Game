from src.ui.display import MiniBingo

#Defining a test function to verify that a drawn number that exists on the card gets marked. 
def test_draw_marks_card():
    """Ensure a number on the card is marked."""
    #Creating a new mini bingo game instance.
    game = MiniBingo()
    #Picking the first number on the card as the target number to mark.
    number_to_mark = game.card.grid[0][0]
    #Calling the mark_number() method to mark the target number. 
    game.card.mark_number(number_to_mark)
    #Failing the test if the target number has not been marked (True).
    assert game.card.marked[0][0], f"Number {number_to_mark} should be marked"

#Defining a test function to ensure that invalid numbers do not mark anything.
def test_mark_number_not_on_card():
    """Ensure a number not on the card is not marked."""
    #Creating a new mini bingo game instance.
    game = MiniBingo()
    #Picking a number outside of the valid range.
    invalid_number = 999
    #Calling the mark_number() method to attempt to mark the invalid number.
    game.card.mark_number(invalid_number)
    #Failing the test if any number has been marked (as the picked number was not valid).
    assert not any(any(row) for row in game.card.marked), \
        "No marks should occur for a number not on the card"
