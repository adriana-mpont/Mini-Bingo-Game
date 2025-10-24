import pytest
from src.game.card import BingoCard

def test_card_structure():
    """Ensure the generated card is a 4x4 grid."""
    card = BingoCard("Player 1")

    assert isinstance(card.card, list), "Card should be a list."
    assert all(isinstance(row, list) for row in card.card), "Each row must be a list."
    assert len(card.card) == 4, "Card must have 4 rows."
    assert all(len(row) == 4 for row in card.card), "Each row must contain 4 numbers."

def test_card_validation():
    """Ensure generated cards are valid according to the internal validation logic."""
    card = BingoCard("Player 2")
    assert card._validate_card(), "Generated card should pass validation."

def test_numbers_within_range():
    """Check that all numbers in the card are within 1–99."""
    card = BingoCard("Player 3")
    flat_numbers = card.get_card_numbers()
    assert all(1 <= num <= 99 for num in flat_numbers), "All numbers must be within 1–99."

def test_unique_numbers_in_card():
    """Ensure all numbers inside a single card are unique."""
    card = BingoCard("Player 4")
    flat_numbers = card.get_card_numbers()
    assert len(flat_numbers) == len(set(flat_numbers)), "Numbers in a single card must be unique."

def test_low_duplicate_probability(num_tests=500):
    """
    Generate multiple BingoCard instances and ensure
    that the probability of identical cards is very low.
    """
    generated_cards = set()

    for i in range(num_tests):
        card = BingoCard(f"Player_{i}")
        card_tuple = tuple(card.get_card_numbers())
        generated_cards.add(card_tuple)

    duplicate_probability = 1 - (len(generated_cards) / num_tests)
    assert duplicate_probability < 0.001, "Duplicate card probability too high."

