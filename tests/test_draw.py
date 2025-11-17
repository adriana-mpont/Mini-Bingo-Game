import pytest
from src.game.draw import NumberDrawer


def test_draw_returns_number_in_range():
    drawer = NumberDrawer()
    num = drawer.draw_number()
    assert 1 <= num <= 99, "Drawn number out of range"


def test_draw_no_repetition():
    drawer = NumberDrawer()
    drawn_numbers = set()
    for _ in range(99):
        num = drawer.draw_number()
        assert num not in drawn_numbers, "Number repeated"
        drawn_numbers.add(num)
    # Next draw should return None because all numbers drawn
    assert drawer.draw_number() is None, "Draw should be None when all numbers are used"


def test_display_drawn_numbers(capsys):
    drawer = NumberDrawer()
    drawer.draw_number()
    drawer.draw_number()
    drawer.display_drawn_numbers()
    captured = capsys.readouterr()
    assert "Numbers Drawn So Far:" in captured.out

def test_draw_after_exhaustion_returns_none():
    drawer = NumberDrawer()
    for _ in range(99):
        drawer.draw_number()
    assert drawer.draw_number() is None, "After all draws, should return None"

