from src.game.card import BingoCard

def test_line_detected_before_bingo():
    """Ensure line detection happens before full bingo."""

    card = BingoCard()

    card.marked[0] = [True, True, True, True]
    assert card.check_line(), "Line should be detected"
    assert not card.check_bingo(), "Bingo should not trigger yet"
