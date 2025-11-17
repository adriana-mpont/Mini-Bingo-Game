from src.ui.display import MiniBingo

def test_draw_marks_card():
    """Ensure a number on the card is marked."""

    game = MiniBingo()

    number_to_mark = game.card.grid[0][0]

    game.card.mark_number(number_to_mark)

    assert game.card.marked[0][0], f"Number {number_to_mark} should be marked"

def test_mark_number_not_on_card():
    """Ensure a number not on the card is not marked."""
    game = MiniBingo()
    invalid_number = 999

    game.card.mark_number(invalid_number)

    assert not any(any(row) for row in game.card.marked), \
        "No marks should occur for a number not on the card"


