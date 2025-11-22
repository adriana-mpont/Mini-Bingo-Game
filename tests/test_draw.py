import pytest
from src.game.draw import NumberDrawer

#Defining a test function to ensure that the drawn numbers are withing the valid limits. 
def test_draw_returns_number_in_range():
    #Creating a new number drawer instance.
    drawer = NumberDrawer()
    #Drawing one random number.
    num = drawer.draw_number()
    #Failing the test if the number falls outside of the rande 1 to 99.
    assert 1 <= num <= 99, "Drawn number out of range"

#Defining a test function to ensure that no number is drawn more than once in a game. 
def test_draw_no_repetition():
    #Creating a new number drawer instance.
    drawer = NumberDrawer()
    #Crating a set to track the numbers already drawn. 
    drawn_numbers = set()
    #Crating a loop through 99 draws (which is the maximum possible). 
    for _ in range(99):
        #Drawing one random number.
        num = drawer.draw_number()
        #Failing the test if the number has been drawn before.
        assert num not in drawn_numbers, "Number repeated"
        #Adding the number drawn last to the tracking set.
        drawn_numbers.add(num)
    #Failing the test if the next draw doesn't return None (all numbers have already been drawn).
    assert drawer.draw_number() is None, "Draw should be None when all numbers are used"

#Defining a test function to verify the printed output of display_drawn_numbers().
def test_display_drawn_numbers(capsys):
    #Creating a new number drawer instance.
    drawer = NumberDrawer()
    #Drawing a first random number.
    drawer.draw_number()
    #Drawing a second random number.
    drawer.draw_number()
    #Printing the list of drawn numbers.
    drawer.display_drawn_numbers()
    #Capturing printed output from display_drawn_numbers() to the console.
    captured = capsys.readouterr()
    #Failing the test is the output does not apper as expected (with the title at the top).
    assert "Numbers Drawn So Far:" in captured.out

#Defining a test function to check behavior after all numbers are drawn. 
def test_draw_after_exhaustion_returns_none():
    #Creating a new number drawer instance.
    drawer = NumberDrawer()
    #Crating a loop through 99 draws (which is the maximum possible). 
    for _ in range(99):
        #Drawing one random number.
        drawer.draw_number()
    #Failing the test if it doesn't return None (should confirm that there are no numbers remaining).
    assert drawer.draw_number() is None, "After all draws, should return None"

