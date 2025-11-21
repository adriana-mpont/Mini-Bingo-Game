import json

from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from dataclasses import dataclass, asdict
from tabulate import tabulate
from pathlib import Path

HISTORY_DIR = Path(os.environ.get("HISTORY_DIR", "data"))
HISTORY_FILE = HISTORY_DIR / "history.json"

@dataclass
class History:
    """Tracks the current playing session: games played, wins, and losses."""
    games_played: int = 0
    wins: int = 0
    losses: int = 0

    def update_history(self, win: bool):
        """Updates the count of games played, wins, and losses."""
        self.games_played += 1
        if win:
            self.wins += 1
        else:
            self.losses += 1

    def print_summary(self):
        """Displays the session summary in a table."""
        data = [
            ["Rounds Played", self.games_played],
            ["Wins", self.wins],
            ["Losses", self.losses]
        ]
        title = "📊SESSION SUMMARY"
        print(f"\n{title}\n" + "-" * (len(title) + 2))
        print(tabulate(data, headers=["Statistic", "Count"], tablefmt="fancy_grid"))

    def save(self):
        """Save the history to a file in a Python dictionary format for the Docker volume.
        With variables in mkdir() we ensure that the directory is created/exists, so that we do not encounter nay errors """
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        with HISTORY_FILE.open("w", encoding= "utf-8") as f:
            json.dump(asdict(self), f, indent = 2)

class InfoTab:
    """Displays the rules to follow the game."""

    def __init__(self):
        self.rules_text = [
            "MINI BINGO RULES",
            "---------------------------",
            "• The game uses a 4x4 Bingo card.",
            "• Numbers are drawn from 1 to 99.",
            "• Numbers appear one at a time.",
            "• A LINE is completed when an entire row or column is marked.",
            "• BINGO is achieved when all numbers are marked."
        ]

    def display(self):
        print("\n=== INFORMATION TAB ===\n")
        for line in self.rules_text:
            print(line)
        print("=======================\n")


class MiniBingo:
    """Console interface that connects the card and number drawer."""

    def __init__(self):
        self.card = BingoCard()
        self.drawer = NumberDrawer()
        self.rounds = 0
        self.info = InfoTab()

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
                self.rounds = 70
                print("\n🎯 Mode selected: Normal (70 rounds)")
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
        self.info.display()
        self.card.display_card()

        won = False

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

            self.info.display()
            self.card.display_card()
            self.drawer.display_drawn_numbers()

            if self.card.check_line():
                print("🎉 LINE! You completed a row or column!")

            if self.card.check_bingo():
                print("🏆 BINGO! You completed the entire card!")
                won = True
                break

        print("\nThanks for playing")