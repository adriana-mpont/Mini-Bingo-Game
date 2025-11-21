import tkinter as tk
from tkinter import Toplevel, Label
from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from src.ui.display import InfoTab
import random
import time

class MiniBingoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('zoomed')
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
        self.drawn_frame.pack(pady=10, fill="x")

        self.drawn_label = tk.Label(
            self.drawn_frame,
            text="--",
            font=("Arial", 36, "bold"),
            fg="#ffffff",
            bg="#29b6f6",
            width=4,
            height=2
        )
        self.drawn_label.pack(pady=5)

        # Scrollable frame for drawn numbers history
        self.drawn_history_container = tk.Frame(self, bg="#e0f7fa")
        self.drawn_history_container.pack(pady=10, fill="x")

        self.drawn_history_canvas = tk.Canvas(self.drawn_history_container, bg="#e0f7fa", height=60)
        self.scrollbar = tk.Scrollbar(self.drawn_history_container, orient="horizontal", command=self.drawn_history_canvas.xview)
        self.scrollable_frame = tk.Frame(self.drawn_history_canvas, bg="#e0f7fa")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.drawn_history_canvas.configure(scrollregion=self.drawn_history_canvas.bbox("all"))
        )

        self.drawn_history_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.drawn_history_canvas.configure(xscrollcommand=self.scrollbar.set)

        self.drawn_history_canvas.pack(side="top", fill="x", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")

        self.drawn_history_labels = []

        self.draw_btn = tk.Button(
            self,
            text="Draw Number",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#ffab91",
            activebackground="#ff7043",
            relief="raised",
            bd=3,
            width=20,
            command=self.draw_number,
            state=tk.DISABLED
        )
        self.draw_btn.pack(pady=10)

        # Show intro
        self.show_intro()

    def roulette_animation(self):
        """Show fast random numbers before revealing the real drawn number"""
        max_number = 99
        for _ in range(15):
            temp_num = random.randint(1, max_number)
            self.drawn_label.config(text=str(temp_num))
            self.update()
            time.sleep(0.05)

    def show_effect(self, achievement):
        """Display floating WELL DONE message for LINE or BINGO"""
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        popup.configure(bg="#ffffff")
        popup.attributes("-topmost", True)

        msg = f"WELL DONE! You got a {achievement}!"
        label = tk.Label(popup, text=msg, font=("Arial", 24, "bold"), fg="#ff5733", bg="#ffffff")
        label.pack(padx=20, pady=20)

        popup.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (popup.winfo_width() // 2)
        y = (screen_height // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

        popup.after(4000, lambda: self.fade_popup(popup))

    def fade_popup(self, popup, step=0):
        if step > 20:
            popup.destroy()
            return
        alpha = 1 - (step / 20)
        popup.attributes("-alpha", alpha)
        popup.after(50, lambda: self.fade_popup(popup, step + 1))

    def show_intro(self):
        intro_win = tk.Toplevel(self)
        intro_win.title("Welcome to Mini Bingo")
        intro_win.geometry("400x300")
        intro_win.configure(bg="#b2ebf2")
        intro_win.grab_set()

        tk.Label(intro_win, text="Welcome to Mini Bingo!", font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)
        rules_text = "\n".join(InfoTab().rules_text)
        tk.Label(intro_win, text=rules_text, font=("Arial", 12), bg="#b2ebf2", justify="left", wraplength=380).pack(padx=10, pady=10)

        tk.Button(intro_win, text="Start", font=("Arial", 12, "bold"), bg="#ffffff", fg="#29b6f6",
                  command=lambda: [intro_win.destroy(), self.show_mode_selection()]).pack(pady=10)

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
            ("Normal", 70, "#4db6ac"),
            ("Easy", 99, "#9575cd")
        ]

        for mode_name, rounds, color in modes:
            frame = tk.Frame(mode_win, bg=color, bd=2, relief="ridge", padx=10, pady=10)
            frame.pack(pady=8, fill="x", padx=20)
            tk.Label(frame, text=f"{mode_name} ({rounds} rounds)", font=("Arial", 14, "bold"), bg=color, fg="white").pack(side="left", padx=5)
            tk.Button(frame, text="Select", bg="white", fg=color, font=("Arial", 12, "bold"), command=lambda r=rounds: set_mode(r)).pack(side="right", padx=5)

    def start_game(self):
        self.card = BingoCard()
        self.drawer = NumberDrawer()
        self.marked = set()
        self.completed_lines = set()
        self.current_round = 0
        self.total_lines = 0
        self.bingo_achieved = False

        # Reset drawn history
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.drawn_history_labels.clear()

        self.display_card()
        self.draw_btn.config(state=tk.NORMAL)

    def display_card(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        self.card_labels = []
        for r, row in enumerate(self.card.grid):
            row_labels = []
            for c, num in enumerate(row):
                lbl = tk.Label(self.card_frame, text=str(num), font=("Arial", 18, "bold"), width=4, height=2, bd=2, relief="ridge", bg="#ffffff")
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(lbl)
            self.card_labels.append(row_labels)

    def update_drawn_history(self, number):
        lbl = tk.Label(self.scrollable_frame, text=str(number), font=("Arial", 12, "bold"), bg="#e0f7fa", fg="#000000", width=4, relief="ridge", bd=1)
        lbl.pack(side="left", padx=2, pady=2)
        self.drawn_history_labels.append(lbl)
        # Scroll to end
        self.drawn_history_canvas.xview_moveto(1)

    def draw_number(self):
        if not self.drawer or self.current_round >= self.rounds:
            self.end_round()
            return

        self.roulette_animation()
        number = self.drawer.draw_number()
        if number is None:
            self.end_round()
            return

        self.current_round += 1
        self.drawn_label.config(text=str(number))
        self.update_drawn_history(number)

        # Mark number on card
        for r, row in enumerate(self.card.grid):
            for c, num in enumerate(row):
                if num == number:
                    self.card_labels[r][c].config(bg="#81c784", fg="white")
                    self.marked.add(num)

        if self.check_line():
            self.show_effect("LINE")
        if self.check_bingo():
            self.bingo_achieved = True
            self.show_effect("BINGO")
            self.draw_btn.config(state=tk.DISABLED)
            self.end_round()

    def check_line(self):
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
            col_id = c + size
            if col_id in self.completed_lines:
                continue
            if all(self.card.grid[r][c] in self.marked for r in range(size)):
                self.completed_lines.add(col_id)
                new_line = True

        return new_line

    def check_bingo(self):
        return all(num in self.marked for num in self.card.get_card_numbers())

    def end_round(self):
        self.draw_btn.config(state=tk.DISABLED)
        summary = f"Round summary:\n- Rounds played: {self.current_round}\n- Lines: {len(self.completed_lines)}\n- Bingo: {'Yes' if self.bingo_achieved else 'No'}"

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


# --- Run app ---
if __name__ == "__main__":
    app = MiniBingoGUI()
    app.mainloop()
