# Mini Bingo (Terminal Game)

This project is a terminal-based interactive Bingo game where a player selects a game duration mode (30 / 70 / 99 rounds) and plays through random number draws that automatically mark the card. The system detects **Line** and **Bingo** conditions in real time and the session history persists until the program is closed.

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


#### Requirements
- Python 3 installed locally


