# Mini Bingo (Terminal version and GUI version Game)

This project is a terminal-based interactive Bingo game where a player selects a game duration mode (30 / 70 / 99 rounds) and plays through random number draws that automatically mark the card. The system detects **Line** and **Bingo** conditions in real time and the session history persists until the program is closed.

There is also the availability of running locally a GUI version of the Mini Bingo game for clearer visuals. The functionality remains the same as in the terminal version.

---

## Organization:
This project was organized by separating core gameplay logic from UI and test modules.

- `game` package → random 4x4 card generation, random draw engine, win condition logic.
- `ui` package → terminal display, screen formatting and messaging.
- `tests` directory → unit tests validating correctness of card uniqueness, mode selection, win detection and draw non-repetition.
- this modular separation results in low coupling, high clarity and easier feature expansion through upcoming sprints.

---

## Clean Code principles applied:
- **Package Module**: clear packages and modules, grouping logic by purpose.
- **Consistent Naming**: descriptive naming for functions + classes reflecting their responsibility.
- **Small, Focused Functions**: core logic split into clear, testable operations (generate_card, draw_number, check_win).
- **No Duplication**: repeated operations such as marking or uniqueness enforcement are centralized.
- **Readable and Maintainable**: predictable control flow, clean syntax, no hidden side effects.
- **Test Coverage**: unit tests cover core logic, randomization boundaries, edge cases and failure states to ensure stability and reliability.

---

## How to Run
To run the **terminal version** we have 2 options: 
  1. Run it locally: You run the main.py file.
  2. Run it in Docker (follow these steps): 
      Step 1: You access from the terminal the directory where your code is located.
      Step 2: You enter in the terminal **docker compose build** in order to build the image.
      Step 3: You enter in the terminal **docker compose run --rm mini-bingo-app**.

To run the **Graphical User Interface version** you must run it locally by running the gui.py file.

#### Requirements
- Python 3.8 or newer installed locally (in order to run the terminal version or GUI version)
- Docker installed and running (in order to run the terminal version from Docker)


