
from ui.display import MiniBingo

def main():
    """Run a minimal playable Mini Bingo session (Sprint 2 demo)."""
    print(" Welcome to Mini Bingo - Sprint 2 Demo \n")

    while True: 
        game = MiniBingo()
        # For Sprint 2: allow player to choose mode and manually advance rounds
        game.start()  # rounds handled inside display.py for manual mode selection

        replay = input("\nWould you like to play another round? (Yes / No)").strip().lower()
        if replay in ("y", "yes"): 
            break
        elif replay in ("n", "no"): 
            print("The game has finished. Thank you for playing!")
            return 

if __name__ == "__main__":
    main()
