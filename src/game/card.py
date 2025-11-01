import random

class BingoCard:
    """Represents a 4x4 Bingo card with unique random numbers."""

    def __init__(self, size: int = 4, number_range: int = 99):
        self.size = size
        self.number_range = number_range
        self.grid = self._generate_card()

    def _generate_card(self):
        """Generates a grid of unique random numbers between 1–99."""
        numbers = random.sample(range(1, self.number_range + 1), self.size ** 2)
        return [numbers[i:i + self.size] for i in range(0, len(numbers), self.size)]

    def validate_card(self) -> bool:
        """Validates that the card contains 16 unique numbers within range."""
        flat_numbers = self.get_card_numbers()
        return len(flat_numbers) == len(set(flat_numbers)) and all(
            1 <= n <= self.number_range for n in flat_numbers
        )

    def get_card_numbers(self):
        """Returns all numbers in a flat list."""
        return [num for row in self.grid for num in row]

    def display_card(self):
        """Displays the Bingo card in a grid format."""
        print("\n Your Bingo card")
        print("-" * (self.size * 6))
        for row in self.grid:
            print(" ".join(f"{num:>4}" for num in row))
        print("-" * (self.size * 6))
