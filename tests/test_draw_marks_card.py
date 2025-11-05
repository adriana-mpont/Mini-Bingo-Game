import pytest
from unittest.mock import patch
from src.ui.display import MiniBingo

def test_draw_marks_card(monkeypatch):
    """When a drawn number is on the card, it should be marked."""
    game = MiniBingo()

    # Manually set a known number on the card
    target = game.card.grid[0][0]

    # Patch draw_number to always draw that number first
    def fake_draw():
        return target

    monkeypatch.setattr(game.drawer, "draw_number", fake_draw)

    with patch("builtins.input", return_value=""):
        game.start()

    assert game.card.marked[0][0], "Number drawn was not marked on the card"
