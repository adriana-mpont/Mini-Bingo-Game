
from ui.display import MiniBingo

def main():
    """Run a minimal playable Mini Bingo session (Sprint 2 demo)."""
    print(" Welcome to Mini Bingo - Sprint 2 Demo \n")

    game = MiniBingo()

    # For Sprint 2: allow player to choose mode and manually advance rounds
    game.start()  # rounds handled inside display.py for manual mode selection

    print("\n Sprint 2 session finished. Thank you for playing!")

if __name__ == "__main__":
    main()
