import tkinter as tk
from tkinter import messagebox
from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from src.ui.display import InfoTab

class MiniBingoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Bingo Game")
        self.configure(bg="#e0f7fa")
        self.resizable(False, False)

        # --- Game state ---
        self.card = None
        self.drawer = None
        self.rounds = 0
        self.current_round = 0
        self.marked = set()
        self.completed_lines = set()
        self.card_labels = []
        self.total_lines = 0
        self.bingo_achieved = False

        # --- UI widgets ---
        self.card_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="solid")
        self.card_frame.pack(pady=20)

        self.drawn_frame = tk.Frame(self, bg="#b3e5fc", bd=2, relief="ridge", padx=10, pady=10)
        self.drawn_frame.pack(pady=10)
        self.drawn_label = tk.Label(self.drawn_frame, text="--", font=("Arial", 36, "bold"),
                                    fg="#ffffff", bg="#29b6f6", width=4, height=2)
        self.drawn_label.pack(pady=5)

        self.draw_btn = tk.Button(self, text="Draw Number", font=("Arial", 14, "bold"),
                                  fg="white", bg="#ffab91", activebackground="#ff7043",
                                  relief="raised", bd=3, width=20, command=self.draw_number, state=tk.DISABLED)
        self.draw_btn.pack(pady=10)

        self.drawn_history_frame = tk.Frame(self, bg="#e0f7fa")
        self.drawn_history_frame.pack(pady=10, fill="x")
        self.drawn_history_labels = []

        # Show intro and mode selection at start
        self.show_intro()

    # --- Intro popup with InfoTab rules ---
    def show_intro(self):
        intro_win = tk.Toplevel(self)
        intro_win.title("Welcome to Mini Bingo")
        intro_win.geometry("400x300")
        intro_win.configure(bg="#b2ebf2")
        intro_win.grab_set()

        tk.Label(intro_win, text="Welcome to Mini Bingo!", font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)
        rules_text = "\n".join(InfoTab().rules_text)
        tk.Label(intro_win, text=rules_text, font=("Arial", 12), bg="#b2ebf2",
                 justify="left", wraplength=380).pack(padx=10, pady=10)

        tk.Button(intro_win, text="Start", font=("Arial", 12, "bold"), bg="#ffffff", fg="#29b6f6",
                  command=lambda: [intro_win.destroy(), self.show_mode_selection()]).pack(pady=10)

    # --- Mode selection ---
    def show_mode_selection(self):
        mode_win = tk.Toplevel(self)
        mode_win.title("Choose Game Mode")
        mode_win.geometry("360x260")
        mode_win.configure(bg="#b2ebf2")
        mode_win.grab_set()

        tk.Label(mode_win, text="Choose Game Mode", font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)

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
            tk.Label(frame, text=f"{mode_name} ({rounds} rounds)", font=("Arial", 14, "bold"), bg=color, fg="white").pack(side="left", padx=5)
            tk.Button(frame, text="Select", bg="white", fg=color, font=("Arial", 12, "bold"),
                      command=lambda r=rounds: set_mode(r)).pack(side="right", padx=5)

    # --- Start game ---
    def start_game(self):
        self.card = BingoCard()
        self.drawer = NumberDrawer()
        self.marked = set()
        self.completed_lines = set()
        self.current_round = 0
        self.total_lines = 0
        self.bingo_achieved = False
        self.drawn_history_labels.clear()
        for widget in self.drawn_history_frame.winfo_children():
            widget.destroy()
        self.display_card()
        self.draw_btn.config(state=tk.NORMAL)

    # --- Display card ---
    def display_card(self):
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

    # --- Draw number ---
    def draw_number(self):
        if not self.drawer:
            return
        if self.current_round >= self.rounds:
            messagebox.showinfo("Game Over", f"Reached maximum rounds ({self.rounds})!")
            self.end_round()
            return

        number = self.drawer.draw_number()
        if number is None:
            messagebox.showinfo("Game Over", "No more numbers to draw!")
            self.end_round()
            return

        self.current_round += 1
        self.drawn_label.config(text=str(number))

        # Draw history
        lbl = tk.Label(self.drawn_history_frame, text=str(number), font=("Arial", 12, "bold"),
                       bg="#ffffff", fg="#333333", bd=1, relief="solid", width=4)
        lbl.pack(side="left", padx=2)
        self.drawn_history_labels.append(lbl)

        # Mark card
        for r, row in enumerate(self.card.grid):
            for c, num in enumerate(row):
                if num == number:
                    self.card_labels[r][c].config(bg="#81c784", fg="white")
                    self.marked.add(num)

        # Check line
        if self.check_line():
            self.total_lines += 1
            messagebox.showinfo("LINE!", f"LINE completed! Total lines: {self.total_lines}")

        # Check bingo
        if self.check_bingo():
            self.bingo_achieved = True
            messagebox.showinfo("BINGO!", "BINGO! You won!")
            self.end_round()

    def check_line(self):
        new_line = False
        size = self.card.size
        for r in range(size):
            if r in self.completed_lines:
                continue
            if all(self.card.grid[r][c] in self.marked for c in range(size)):
                self.completed_lines.add(r)
                new_line = True
        for c in range(size):
            if c + size in self.completed_lines:
                continue
            if all(self.card.grid[r][c] in self.marked for r in range(size)):
                self.completed_lines.add(c + size)
                new_line = True
        return new_line

    def check_bingo(self):
        return all(num in self.marked for num in self.card.get_card_numbers())

    def end_round(self):
        self.draw_btn.config(state=tk.DISABLED)
        summary = f"Round summary:\n- Rounds played: {self.current_round}\n- Lines: {self.total_lines}\n- Bingo: {'Yes' if self.bingo_achieved else 'No'}"
        replay_win = tk.Toplevel(self)
        replay_win.title("Game Summary")
        replay_win.geometry("300x200")
        replay_win.grab_set()

        tk.Label(replay_win, text=summary, font=("Arial", 12), justify="left").pack(pady=10)
        tk.Label(replay_win, text="Play again?", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(replay_win, text="Yes", font=("Arial", 12, "bold"), bg="#4db6ac", fg="white",
                  command=lambda: [replay_win.destroy(), self.start_game()]).pack(side="left", padx=30, pady=20)
        tk.Button(replay_win, text="No", font=("Arial", 12, "bold"), bg="#ff8a65", fg="white",
                  command=lambda: [replay_win.destroy(), self.quit()]).pack(side="right", padx=30, pady=20)


if __name__ == "__main__":
    app = MiniBingoGUI()
    app.mainloop()
