import pytest
from src.ui.display import MiniBingo

def test_replay_resets_game():
    """Ensure creating a new MiniBingo resets card and draws."""
    game1 = MiniBingo()
    first_card_numbers = [n for row in game1.card.grid for n in row]

    for _ in range(5):
        game1.drawer.draw_number()

    game2 = MiniBingo()
    new_card_numbers = [n for row in game2.card.grid for n in row]

    assert game2.drawer.drawn_numbers == [], "Drawn numbers should reset"
    assert first_card_numbers != new_card_numbers, "New card should be different"
