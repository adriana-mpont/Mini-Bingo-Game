import random

class BingoCard:
    """Represents a 4x4 Bingo card with unique random numbers."""

    def __init__(self, size: int = 4, number_range: int = 99):
        self.size = size
        self.number_range = number_range
        self.grid = self._generate_card()
        self.marked = [[False for _ in range(self.size)] for _ in range(self.size)]

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

    def mark_number(self, number: int) -> bool:
        """Marks the number of the card if found. 
        Returns True if the number was present and marked, False otherwise. """
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == number:
                    self.marked[i][j] = True
                    return True
        return False
        
     def display_card(self):
        """Displays the Bingo card in a grid format.""" 
        print("\n Your Bingo card")
        print("-" * (self.size * 6))
        
        for i in range(self.size):
            row_display = []
            for j in range(self.size):
                num = self.grid[i][j]
                if self.marked[i][j]:
                    row_display.append(f"[{num:02}]") #If number is marked
                else:
                    row_display.append(f" {num:02} ") #If number is not marked
            print(" ".join(row_display))
        print("-" * (self.size * 6))
