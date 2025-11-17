
from ui.gui import MiniBingoGUI

def main():
    """Run a minimal playable Mini Bingo session (Sprint 2 demo)."""
    history = History()
    info = InfoTab()
    matches = 1

    while True: 
        info.display()
        game = MiniBingo()
        # For Sprint 2: allow player to choose mode and manually advance rounds
        did_win = game.start() # rounds handled inside display.py for manual mode selection
        history.update_history(did_win)
        while True:
            replay = input("\nWould you like to play another round? (Yes / No): ").strip().lower()
            if replay == "yes":
                history.print_summary()
                matches += 1
                print(f"\nStarting match number {matches}.\nGood luck!")
                break
            elif replay == "no":
                history.print_summary()
                print("\nThe game has finished. Thank you for playing!\n")
                return
            else:
                print("⚠️ Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    app = MiniBingoGUI()
    app.mainloop()
