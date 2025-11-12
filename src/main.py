
from ui.display import MiniBingo

def main():
    """Run a minimal playable Mini Bingo session (Sprint 2 demo)."""
    matches = 1
    print(" Welcome to Mini Bingo \n")

    while True: 
        game = MiniBingo()
        # For Sprint 2: allow player to choose mode and manually advance rounds
        game.start()  # rounds handled inside display.py for manual mode selection
        while True:
            replay = input("\nWould you like to play another round? (Yes / No)").strip().lower()
            if replay == "yes":
                matches += 1
                print(f"\nStarting match number {matches}.\nGood luck!")
                break
            elif replay == "no":
                print("\nThe game has finished. Thank you for playing!\n")
                return
            else:
                print("⚠️ Invalid input. Please type 'yes' or 'no'.")
if __name__ == "__main__":
    main()
