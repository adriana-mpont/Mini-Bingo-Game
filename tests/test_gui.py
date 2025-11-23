import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch

from src.ui.gui import MiniBingoGUI

@pytest.fixture
def app(monkeypatch):
    """
    Fixture that instantiates the MiniBingoGUI while preventing GUI side effects.
    - Replaces time.sleep to avoid animation delays.
    - Suppresses intro popups to keep tests non-interactive.
    - Ensures the window is destroyed after each test.
    """
    #Avoid real sleep during animation
    monkeypatch.setattr("time.sleep", lambda x: None)
    #Prevent auto-popups (rules, etc.)
    monkeypatch.setattr(MiniBingoGUI, "show_intro", lambda self: None)

    app = MiniBingoGUI()
    yield app
    app.destroy()

def test_initial_state(app):
    """Verifies that the GUI initializes with the expected default attributes."""
    #Logic: no game should exist at startup
    assert app.card is None
    assert app.drawer is None
    assert app.rounds == 0
    assert app.current_round == 0
    #style: draw button must be disabled before game starts
    assert app.draw_btn["state"] == tk.DISABLED

def test_start_game_creates_card_and_drawer(app):
    """start_game must reset the game state and create card & drawer."""
    app.rounds = 10
    app.start_game()
    #Game components must be instantiated
    assert app.card is not None
    assert app.drawer is not None
    assert app.current_round == 0
    #All tracking variables must be reset
    assert len(app.marked) == 0
    assert len(app.completed_lines) == 0
    #Card grid must be fully created
    assert len(app.card_labels) == app.card.size

def test_display_card_creates_grid(app):
    """Ensures display_card creates a square matrix of Label widgets."""
    app.rounds = 10
    app.start_game()

    size = app.card.size
    #Row count must match card size
    assert len(app.card_labels) == size
    #Iterate grid to validate consistency
    for row in app.card_labels:
        assert len(row) == size #square structure
        for cell in row:
            assert isinstance(cell, tk.Label)

def test_update_drawn_history_adds_label(app):
    """A drawn number must be appended to the drawn-number history panel."""
    app.rounds = 10
    app.start_game()
    #Append one number
    app.update_drawn_history(42)

    assert len(app.drawn_history_labels) == 1
    assert app.drawn_history_labels[0]["text"] == "42"

def test_draw_number_marks_card(app, monkeypatch):
    """
    When a drawn number matches a cell:
    - It must be added to the marked set.
    - Its corresponding label must update its background color.
    """
    #Skip roulette animation to speed up test
    monkeypatch.setattr(app, "roulette_animation", lambda: None)
    app.rounds = 5
    app.start_game()
    #Deterministic draw result
    known_number = app.card.grid[0][0]
    app.drawer.draw_number = MagicMock(return_value=known_number)

    app.draw_number()
    #Verify correct marking
    assert known_number in app.marked
    assert app.card_labels[0][0]["bg"] == "#81c784"

def test_check_line_detects_rows(app):
    """check_line must detect and record a fully marked row."""
    app.rounds = 5
    app.start_game()
    #Simulate a full row marking
    row_nums = app.card.grid[0]
    app.marked = set(row_nums)

    assert app.check_line() is True
    assert 0 in app.completed_lines #Row index is stored

def test_check_line_detects_columns(app):
    """check_line must detect and record a fully marked column."""
    app.rounds = 5
    app.start_game()
    #Mark entire first column
    col_nums = [app.card.grid[r][0] for r in range(app.card.size)]
    app.marked = set(col_nums)
    #Column indices follow rows, so first column index = size
    assert app.check_line() is True
    assert app.card.size in app.completed_lines

def test_check_bingo_true(app):
    """check_bingo must return True when all card numbers are marked."""
    app.rounds = 5
    app.start_game()
    #Mark entire card
    all_nums = app.card.get_card_numbers()
    app.marked = set(all_nums)

    assert app.check_bingo() is True

def test_check_bingo_false(app):
    """check_bingo must return False when the card is not fully marked."""
    app.rounds = 5
    app.start_game()

    app.marked = set() #No marks
    assert not app.check_bingo()

def test_show_rules_creates_popup(app):
    """show_rules must create a new Toplevel window."""
    #Patch to avoid real popup creation
    with patch("tkinter.Toplevel") as mock_top:
        app.show_rules()
        assert mock_top.called

def test_show_effect_creates_popup(app):
    """show_effect must create a new Toplevel window."""
    #Ensure GUI side effects are isolated
    with patch("tkinter.Toplevel") as mock_top:
        app.show_effect("LINE")
        assert mock_top.called

def test_end_round_disables_button(app):
    """
    end_round must disable the draw button and finalize the round.
    Popup creation is patched to prevent GUI interference.
    """
    app.rounds = 5
    app.start_game()
    #Avoid real popup during test
    with patch("tkinter.Toplevel"):
        app.end_round()
    #Draw button must be disabled after round finishes
    assert app.draw_btn["state"] == tk.DISABLED
