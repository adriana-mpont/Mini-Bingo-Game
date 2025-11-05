from src.game.card import BingoCard
from src.game.draw import NumberDrawer


class MiniBingo:
    """Main interface that connects the card and number drawer."""

    def __init__(self):
        self.card = BingoCard()
        self.drawer = NumberDrawer()
        self.rounds = 0

    def choose_mode(self):
        """Lets the player choose one of three predefined modes."""
        print("\n🎮 Choose Game Mode:")
        print("1. Competitive (30 rounds)")
        print("2. Normal (45 rounds)")
        print("3. Easy (99 rounds)")

        while True:
            choice = input("Select a mode (1, 2, or 3): ").strip()
            if choice == "1":
                self.rounds = 30
                print("\n🏁 Mode selected: Competitive (30 rounds)")
                break
            elif choice == "2":
                self.rounds = 45
                print("\n🎯 Mode selected: Normal (45 rounds)")
                break
            elif choice == "3":
                self.rounds = 99
                print("\n🌿 Mode selected: Easy (99 rounds)")
                break
            else:
                print("⚠️ Invalid option. Please choose 1, 2, or 3.")

    def start(self):
        """Starts the Bingo game with chosen mode and manual round progression."""
        print("\n🧩 Welcome to Mini Bingo 🧩")
        self.choose_mode()
        self.card.display_card()

        for round_number in range(1, self.rounds + 1):
            input(f"\n👉 Press Enter to draw number for Round {round_number}...")
            number = self.drawer.draw_number()
            if number is None:
                print("No more numbers to draw.")
                break
            print(f"➡️ Drawn number: {number}")
            
            if self.card.mark_number(number):
                print("Number found and marked on your card!")
            else:
                print("Number not on your card.")
            
            self.card.display_card()            
            self.drawer.display_drawn_numbers()

        print("\n Thanks for playing ") 
