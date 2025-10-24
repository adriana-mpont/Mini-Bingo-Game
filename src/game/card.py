import random

class BingoCard:
    """
    Represents a single Bingo card.
    Each card contains a 4x4 grid of unique numbers between 1 and 99.
    """

    def __init__(self, player_name: str):
        """
        Initialize a BingoCard and assign it to a player.
        The card is generated and validated automatically.
        """
        self.player_name = player_name
        self.card = self._generate_card()

        if not self._validate_card():
            raise ValueError("Invalid Bingo card generated. Please retry.")

    def _generate_card(self):
        """
        Generates a 4x4 bingo card with unique random numbers (1–99).
        Returns:
            list[list[int]]: 4x4 grid representing the Bingo card.
        """
        numbers = random.sample(range(1, 100), 16)
        return [numbers[i:i + 4] for i in range(0, 16, 4)]

    def _validate_card(self):
        """
        Validates the Bingo card ensuring:
        - 16 total numbers
        - All numbers are unique
        - All numbers are within the 1–99 range
        Returns:
            bool: True if valid, False otherwise.
        """
        flat = [num for row in self.card for num in row]

        if len(flat) != 16:
            return False
        if len(set(flat)) != 16:
            return False
        if not all(1 <= num <= 99 for num in flat):
            return False

        return True

    def display_card(self):
        """
        Displays the Bingo card in a user-friendly grid format.
        """
        print(f"\n🎟️  Bingo Card for {self.player_name}")
        print("-" * 25)
        for row in self.card:
            print(" | ".join(f"{num:2d}" for num in row))
        print("-" * 25)

    def get_card_numbers(self):
        """
        Returns the numbers in the card as a flat list.
        Useful for testing or comparisons.
        """
        return [num for row in self.card for num in row]

# ------------------------------------------------------------
# Example usage (manual test)
# ------------------------------------------------------------
if __name__ == "__main__":
    # Create a Bingo card for a sample player
    player_card = BingoCard("Laura")

    # Display the card
    player_card.display_card()

    # Validate the card
    print("\n✅ Card valid:", player_card._validate_card())