from src.game.card import BingoCard
from src.game.draw import NumberDrawer


class MiniBingo:
    """Main interface that connects the card and number drawer."""

    def __init__(self):
        self.card = BingoCard()
        self.drawer = NumberDrawer()

    def start(self, rounds: int = 5):
        """Starts a minimal playable Bingo session (Sprint 1 demo)."""
        print("\n🧩 Welcome to Mini Bingo 🧩")
        self.card.display_card()

        for round_number in range(1, rounds + 1):
            input(f"\n👉 Press Enter to start round {round_number}...")
            number = self.drawer.draw_number()
            if number:
                print(f"➡️ Drawn number: {number}")
            self.drawer.display_drawn_numbers()
