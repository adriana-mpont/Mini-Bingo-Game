from ui.display import MiniBingo

def main():
    """Run a minimal playable Mini Bingo session (Sprint 1 demo)."""
    print("🎉 Welcome to Mini Bingo - Sprint 1 Demo 🎉\n")

    game = MiniBingo()

    # Sprint 1: just 5 rounds for demonstration
    game.start(rounds=5)

    print("\n✅ Sprint 1 session finished. Thank you for playing!")

if __name__ == "__main__":
    main()
