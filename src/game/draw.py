import random

class NumberDrawer:
    """Handles random number drawing from 1–99 without repetition."""

    def __init__(self, max_number: int = 99):
        self.max_number = max_number
        self.available_numbers = set(range(1, max_number + 1))
        self.drawn_numbers = []

    def draw_number(self):
        """Draws a random number and removes it from the available pool."""
        if not self.available_numbers:
            print("⚠️ All numbers have been drawn!")
            return None

        number = random.choice(list(self.available_numbers))
        self.available_numbers.remove(number)
        self.drawn_numbers.append(number)
        return number

    def display_drawn_numbers(self):
        """Displays all drawn numbers in sorted order."""
        print("\n🔢 Numbers Drawn So Far:")
        if self.drawn_numbers:
            print(", ".join(map(str, sorted(self.drawn_numbers))))
        else:
            print("No numbers drawn yet.")
