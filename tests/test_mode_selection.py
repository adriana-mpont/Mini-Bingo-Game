import pytest
from unittest.mock import patch
from src.ui.display import MiniBingo

#Defining a test function to verify the behavior of mode selection.
def test_mode_selection():
    #Creating a dictionary mapping the different mode names to their expected number of rounds.
    modes = {"Competitive": 30, "Normal": 45, "Easy": 99}
    #Creating another dictionary mapping the different mode names to their user input (number through which the user choses the mode).
    mode_inputs = {"Competitive": "1", "Normal": "2", "Easy": "3"}

    #Creating a loop through each game mode, to test them all.
    for mode_name, expected_rounds in modes.items():
        #Creating a new mini bingo game instance
        game = MiniBingo()
        #Simulating input(), so that the game receives the correct selection without the user typing.
        with patch("builtins.input", return_value=mode_inputs[mode_name]):
            #Starting the game, which should automatically select the decided mode.
            game.start()

        #Failing the test if the number of rounds (drawn numbers) is not as expected for that mode.
        assert len(game.drawer.drawn_numbers) == expected_rounds
        #Failing the test if the numbers drawn are not all unique (there are duplicates). 
        assert len(set(game.drawer.drawn_numbers)) == expected_rounds
