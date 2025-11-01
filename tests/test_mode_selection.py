import pytest
from unittest.mock import patch
from src.ui.display import MiniBingo


def test_mode_selection():
    modes = {"Competitive": 30, "Normal": 45, "Easy": 99}
    mode_inputs = {"Competitive": "1", "Normal": "2", "Easy": "3"}

    for mode_name, expected_rounds in modes.items():
        game = MiniBingo()
        with patch("builtins.input", return_value=mode_inputs[mode_name]):
            game.start()

        # Check that the correct number of numbers were drawn
        assert len(game.drawer.drawn_numbers) == expected_rounds
        # Check that all drawn numbers are unique
        assert len(set(game.drawer.drawn_numbers)) == expected_rounds
