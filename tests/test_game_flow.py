from src.game.card import BingoCard

#Defining a test function to verify that line detection occurs before bingo detection.
def test_line_detected_before_bingo():
    """Ensure line detection happens before full bingo."""
    #Creating a new bingo card instance.
    card = BingoCard()
    #Manually marking the entire first row (True) to simulate completing a line. 
    card.marked[0] = [True, True, True, True]
    #Failing the test if check_line() does not detect the completed line.
    assert card.check_line(), "Line should be detected"
    #Failing the test if check_bingo() reports a full bingo (since only one row is complete). 
    assert not card.check_bingo(), "Bingo should not trigger yet"
