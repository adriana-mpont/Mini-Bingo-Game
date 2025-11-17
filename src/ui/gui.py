import tkinter as tk
from tkinter import messagebox
from src.game.card import BingoCard
from src.game.draw import NumberDrawer

class MiniBingoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Bingo Game")
        self.configure(bg="#e0f7fa")
        self.resizable(False, False)

        # Game state
        self.card = None
        self.drawer = None
        self.rounds = 0
        self.marked = set()
        self.completed_lines = set()
        self.card_labels = []

        # --- UI widgets ---
        # Card display
        self.card_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="solid")
        self.card_frame.pack(pady=20)

        # Drawn number display
        self.drawn_frame = tk.Frame(self, bg="#b3e5fc", bd=2, relief="ridge", padx=10, pady=10)
        self.drawn_frame.pack(pady=10)
        self.drawn_label = tk.Label(self.drawn_frame, text="--", font=("Arial", 36, "bold"),
                                    fg="#ffffff", bg="#29b6f6", width=4, height=2)
        self.drawn_label.pack(pady=5)

        # Draw button
        self.draw_btn = tk.Button(self, text="Draw Number", font=("Arial", 14, "bold"),
                                  fg="white", bg="#ffab91", activebackground="#ff7043",
                                  relief="raised", bd=3, width=20, command=self.draw_number, state=tk.DISABLED)
        self.draw_btn.pack(pady=10)

        # Drawn numbers history strip
        self.drawn_history_frame = tk.Frame(self, bg="#e0f7fa")
        self.drawn_history_frame.pack(pady=10, fill="x")
        self.drawn_history_labels = []

        # Show mode selection on start
        self.show_mode_selection()

    def show_mode_selection(self):
        """Popup to select game mode"""
        mode_win = tk.Toplevel(self)
        mode_win.title("Choose Game Mode")
        mode_win.configure(bg="#b2ebf2")
        mode_win.geometry("360x260")
        mode_win.grab_set()

        tk.Label(mode_win, text="Choose Game Mode",
                 font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)

        def set_mode(rounds):
            self.rounds = rounds
            mode_win.destroy()
            self.start_game()

        modes = [
            ("Competitive", 30, "#ff8a65"),
            ("Normal", 45, "#4db6ac"),
            ("Easy", 99, "#9575cd")
        ]

        for mode_name, rounds, color in modes:
            frame = tk.Frame(mode_win, bg=color, bd=2, relief="ridge", padx=10, pady=10)
            frame.pack(pady=8, fill="x", padx=20)
            tk.Label(frame, text=f"{mode_name} ({rounds} rounds)",
                     font=("Arial", 14, "bold"), bg=color, fg="white").pack(side="left", padx=5)
            tk.Button(frame, text="Select", bg="white", fg=color, font=("Arial", 12, "bold"),
                      command=lambda r=rounds: set_mode(r)).pack(side="right", padx=5)

    def start_game(self):
        """Initialize game state and display card"""
        self.card = BingoCard()
        self.drawer = NumberDrawer()
        self.marked = set()
        self.completed_lines = set()
        self.display_card()
        self.draw_btn.config(state=tk.NORMAL)

    def display_card(self):
        """Display 4x4 bingo card with buttons/labels"""
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        self.card_labels = []

        for r, row in enumerate(self.card.grid):
            row_labels = []
            for c, num in enumerate(row):
                lbl = tk.Label(self.card_frame, text=str(num), font=("Arial", 18, "bold"),
                               width=4, height=2, bd=2, relief="ridge", bg="#ffffff")
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(lbl)
            self.card_labels.append(row_labels)

    def draw_number(self):
        """Draw a number, highlight card, and check for line/bingo"""
        if not self.drawer:
            return
        number = self.drawer.draw_number()
        if number is None:
            messagebox.showinfo("Game Over", "No more numbers to draw!")
            self.draw_btn.config(state=tk.DISABLED)
            return

        # Update big number display
        self.drawn_label.config(text=str(number))

        # Update history strip
        lbl = tk.Label(self.drawn_history_frame, text=str(number), font=("Arial", 12, "bold"),
                       bg="#ffffff", fg="#333333", bd=1, relief="solid", width=4)
        lbl.pack(side="left", padx=2)
        self.drawn_history_labels.append(lbl)

        # Mark number on card
        for r, row in enumerate(self.card.grid):
            for c, num in enumerate(row):
                if num == number:
                    self.card_labels[r][c].config(bg="#81c784", fg="white")
                    self.marked.add(num)

        # Check for new line(s)
        if self.check_line():
            messagebox.showinfo("LINE!", "LINE completed!")

        # Check for Bingo
        if self.check_bingo():
            messagebox.showinfo("BINGO!", "BINGO! You won!")
            self.draw_btn.config(state=tk.DISABLED)

    def check_line(self):
        """Check rows and columns for completed line (once per line)"""
        new_line = False
        size = self.card.size
        # Check rows
        for r in range(size):
            if r in self.completed_lines:
                continue
            if all(self.card.grid[r][c] in self.marked for c in range(size)):
                self.completed_lines.add(r)
                new_line = True
        # Check columns
        for c in range(size):
            if c + size in self.completed_lines:
                continue
            if all(self.card.grid[r][c] in self.marked for r in range(size)):
                self.completed_lines.add(c + size)
                new_line = True
        return new_line

    def check_bingo(self):
        """Check if all numbers are marked"""
        return all(num in self.marked for num in self.card.get_card_numbers())

if __name__ == "__main__":
    app = MiniBingoGUI()
    app.mainloop()
