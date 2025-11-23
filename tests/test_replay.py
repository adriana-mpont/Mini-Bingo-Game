import pytest
from src.ui.display import MiniBingo

#Defining a test function to check that restarting the game resets all states (card and draws).
def test_replay_resets_game():
    """Ensure creating a new MiniBingo resets card and draws."""
    #Creating a first mini bingo game instance.
    game1 = MiniBingo()
    #Collecting all the numbers on the card from the first game into a flat list.
    first_card_numbers = [n for row in game1.card.grid for n in row]

    #Creating a loop to simulate 5 draws in the first game.
    for _ in range(5):
        #Drawing a number and recording it in the game. 
        game1.drawer.draw_number()

    #Creating a second mini bingo game instance.
    game2 = MiniBingo()
    #Collecting all the numbers on the card from the second game into a flat list.
    new_card_numbers = [n for row in game2.card.grid for n in row]

    #Failing the test if there are numbers drawn from the second game (state of drawn numbers should reset after first game).
    assert game2.drawer.drawn_numbers == [], "Drawn numbers should reset"
    #Failing the test if the card from the second game is identical to the card from the first game. 
    assert first_card_numbers != new_card_numbers, "New card should be different"
