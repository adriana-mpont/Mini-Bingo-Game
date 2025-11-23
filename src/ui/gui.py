import tkinter as tk
from tkinter import Toplevel, Label
from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from src.ui.display import InfoTab
import random
import time

#Defining a class named MiniBingo GUI inheriting from Tk (the main Tkinter window).
class MiniBingoGUI(tk.Tk):
    
    #Defining the constructor method that initializes the GUI
    def __init__(self):
        #Initializing the Tk superclass, setting up the root window.
        super().__init__()
        #Maximizing the window to full screen
        self.state('zoomed')
        #Setting the text for the window title.
        self.title("Mini Bingo Game")
        #Setting the default background color of the main window. 
        self.configure(bg="#e0f7fa")
        #Disabling resizing the window in both width and height
        self.resizable(False, False)

        # --- Game state ---
        #Creating a placeholder for the current bingo card instance (when game starts). 
        self.card = None
        #Creating a placeholder for the number drawer instance (when game starts).
        self.drawer = None
        #Storing the number of rounds the game is set to run (based on chosen mode).
        self.rounds = 0
        #Tracking the number of rounds played so far (so number of current round).
        self.current_round = 0
        #Storing the numbers marked on the user's card.
        self.marked = set()
        #Storing the completed rows/columns on the user's card. 
        self.completed_lines = set()
        #Holding references to each lable widget representing the card cells. 
        self.card_labels = []
        #Storing the total number of lines the player has completed on the card.
        self.total_lines = 0
        #Creating a flag indicating whether the player has completed the full card (bingo). 
        self.bingo_achieved = False

        # --- UI widgets ---
        #Creating a visible frame that will contain the bingo card grid. 
        self.card_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="solid")
        #Placing the frame in the window vertical padding spacing. 
        self.card_frame.pack(pady=20)

        #Crating a frame to display the most recently drawn number. 
        self.drawn_frame = tk.Frame(self, bg="#b3e5fc", bd=2, relief="ridge", padx=10, pady=10)
        #Placing the frame in the window with vertical padding, stretching horizontally. 
        self.drawn_frame.pack(pady=10, fill="x")

        #Labling widget that shows the latest drawn number in large text
        self.drawn_label = tk.Label(
            self.drawn_frame,
            text="--",
            font=("Arial", 36, "bold"),
            fg="#ffffff",
            bg="#29b6f6",
            width=4,
            height=2
        )
        #Placing the lable inside the frame in the window with a small margin.
        self.drawn_label.pack(pady=5)

        #Creating a scrollable container frame for drawn numbers history.
        self.drawn_history_container = tk.Frame(self, bg="#e0f7fa")
        #Placing the container with padding and full width.
        self.drawn_history_container.pack(pady=10, fill="x")

        #Enabling scrolling content horizontally (with a fixed displayed height).
        self.drawn_history_canvas = tk.Canvas(self.drawn_history_container, bg="#e0f7fa", height=60)
        #Creating a scrollbar to control horizontal movement
        self.scrollbar = tk.Scrollbar(self.drawn_history_container, orient="horizontal", command=self.drawn_history_canvas.xview)
        #Creating an actual inner frame that will hold number labels. 
        self.scrollable_frame = tk.Frame(self.drawn_history_canvas, bg="#e0f7fa")

        #Binding an event listener to update the scrollable region (triggered whenever the frame is resized). 
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.drawn_history_canvas.configure(scrollregion=self.drawn_history_canvas.bbox("all"))
        )

        #Placing the scrollable frame (anchoring it to the top-left corner).
        self.drawn_history_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        #Linking the scrolling updates to the scrollbar widget.
        self.drawn_history_canvas.configure(xscrollcommand=self.scrollbar.set)

        #Displaying the canvas above the scrollbar.
        self.drawn_history_canvas.pack(side="top", fill="x", expand=True)
        #Packing scrollbar below the canvas.
        self.scrollbar.pack(side="bottom", fill="x")

        #Storing reference to displayed labels for drawn numbers in a list. 
        self.drawn_history_labels = []

        #Creating a button for drawing a new random number (clicking triggers draw_number() method).
        self.draw_btn = tk.Button(
            self,
            text="Draw Number",
            font=("Arial", 14, "bold"),
            fg="black",
            bg="#ffab91",
            activebackground="#ff7043",
            relief="raised",
            bd=3,
            width=20,
            command=self.draw_number,
            state=tk.DISABLED
        )
        #Placing the button in the window with spacing. 
        self.draw_btn.pack(pady=10)

        #Creating a botton for opening the rules pop-up window (clicking displays the rules window).
        self.rules_btn = tk.Button(
            self,
            text="Show Rules",
            font=("Arial", 12, "bold"),
            fg="black",  # text color
            bg="#4db6ac",  # button background
            activeforeground="black",  # text color when pressed
            activebackground="#26a69a",  # background when pressed
            relief="raised",
            bd=3,
            width=20,
            command=self.show_rules
        )
        #Placing the button in the window with padding. 
        self.rules_btn.pack(pady=5)

        # Show intro
        #Immediately opening an intro pop-up window when the game starts.
        self.show_intro()

    #Defining a method to show a fast anumated number preview before a real draw.
    def roulette_animation(self):
        """Show fast random numbers before revealing the real drawn number"""
        #Creating a variable to tore the maximum number that can be shown in the animation (max number drawable). 
        max_number = 99
        #Creating a loop that runs the animation 15 times.
        for _ in range(15):
            #Generating a random temporary number for the animation. 
            temp_num = random.randint(1, max_number)
            #Updating the GUI label to show this temporary number.
            self.drawn_label.config(text=str(temp_num))
            #Forcing the GUI to refresh so the change appears on screen immediately.
            self.update()
            #Briefly pausing between updates to create animation effect.
            time.sleep(0.05)

    #Defining a method to display a pop-up window with the game rules
    def show_rules(self):
        """Display the game rules in a popup."""
        #Creating a new small window on top of the main window.
        rules_win = tk.Toplevel(self)
        #Setting the title of the rules window.
        rules_win.title("Game Rules")
        #Setting the size of the pop-up window.
        rules_win.geometry("400x300")
        #Setting the background color of the pop-up window.
        rules_win.configure(bg="#b2ebf2")
        #Locking focus to this window until it's closed.
        rules_win.grab_set()  # Focus on the rules window

        #Creating a label for the pop-up title header (with padding). 
        tk.Label(
            rules_win,
            text="Mini Bingo Rules",
            font=("Arial", 16, "bold"),
            bg="#b2ebf2"
        ).pack(pady=10)

        #Retrieving the rules text list and formatting it as multiple lines.
        rules_text = "\n".join(InfoTab().rules_text)
        #Creating another label for the detailed rules text (with padding).
        tk.Label(
            rules_win,
            text=rules_text,
            font=("Arial", 12),
            bg="#b2ebf2",
            justify="left",
            wraplength=380
        ).pack(padx=10, pady=10)

        #Adding a close button to dismiss the pop-up (below the text).
        tk.Button(
            rules_win,
            text="Close",
            font=("Arial", 12, "bold"),
            bg="#4db6ac",
            fg="black",
            command=rules_win.destroy
        ).pack(pady=10)

    #Defining a method to display a temporary pop-up for LINE or BINGO.
    def show_effect(self, achievement):
        """Display floating WELL DONE message for LINE or BINGO"""
        #Creating a new overlay window.
        popup = tk.Toplevel(self)
        #Removing window borders and decorations.
        popup.overrideredirect(True)
        #Setting the background to white. 
        popup.configure(bg="#ffffff")
        #Ensuring this pop-up stays abother the other windows.
        popup.attributes("-topmost", True)

        #Creating the message text based on whether it's LINE or BINGO.
        msg = f"WELL DONE! You got a {achievement}!"
        #Creating a label inside the pop-up to show the message.
        label = tk.Label(popup, text=msg, font=("Arial", 24, "bold"), fg="#ff5733", bg="#ffffff")
        #Placing the label with padding.
        label.pack(padx=20, pady=20)

        #Ensuring geometry is updated before positioning.
        popup.update_idletasks()
        #Getting the width of the screen.
        screen_width = self.winfo_screenwidth()
        #Getting the height of the screen.
        screen_height = self.winfo_screenheight()
        #Centering the pop-up horizontally.
        x = (screen_width // 2) - (popup.winfo_width() // 2)
        #Centering the pop-up vertically.
        y = (screen_height // 2) - (popup.winfo_height() // 2)
        #Applying the calculated position to the window.
        popup.geometry(f"+{x}+{y}")

        #Begin fading out the pop-up after 4 seconds.
        popup.after(4000, lambda: self.fade_popup(popup))

    #Defining a method to handle gradual disappearing of the pop-up
    def fade_popup(self, popup, step=0):
        #Checking if enough fade steps are done.
        if step > 20:
            #In this case, remove the pop from the window.
            popup.destroy()
            #Exiting function.
            return
        #Calculating the opacity value descending from 1.
        alpha = 1 - (step / 20)
        #Applying the new transparency level.
        popup.attributes("-alpha", alpha)
        #Scheduling the next fade step.
        popup.after(50, lambda: self.fade_popup(popup, step + 1))

    #Defining a method toshow welcome instructions when the game starts.
    def show_intro(self):
        #Creating the pop-up window
        intro_win = tk.Toplevel(self)
        #Setting the pop-up title.
        intro_win.title("Welcome to Mini Bingo")
        #Setting the pop-up size.
        intro_win.geometry("400x300")
        #Setting the pop-up background color.
        intro_win.configure(bg="#b2ebf2")
        #Locking focus to this intro table
        intro_win.grab_set()

        #Adding the title label.
        tk.Label(intro_win, text="Welcome to Mini Bingo!", font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)
        #Converting the rules list to a multiline string. 
        rules_text = "\n".join(InfoTab().rules_text)
        #Displaying the rules below the intro text.
        tk.Label(intro_win, text=rules_text, font=("Arial", 12), bg="#b2ebf2", justify="left", wraplength=380).pack(padx=10, pady=10)

        #Creating a start button, which closes the intro and opens the mode selection.
        tk.Button(intro_win, text="Start", font=("Arial", 12, "bold"), bg="#ffffff", fg="#29b6f6",
                  command=lambda: [intro_win.destroy(), self.show_mode_selection()]).pack(pady=10)

    #Defining a method to display the available game modes.
    def show_mode_selection(self):
        #Creating the mode selection window
        mode_win = tk.Toplevel(self)
        #Setting the window title.
        mode_win.title("Choose Game Mode")
        #Setting the window size.
        mode_win.geometry("360x260")
        #Setting the window background color.
        mode_win.configure(bg="#b2ebf2")
        #Ensuring this window stays in focus. 
        mode_win.grab_set()

        #Adding the title label.
        tk.Label(mode_win, text="Choose Game Mode", font=("Arial", 16, "bold"), bg="#b2ebf2").pack(pady=10)

        #Defining an internal function to apply the selected method.
        def set_mode(rounds):
            #Storing the chosen number of rounds. 
            self.rounds = rounds
            #Closing the mode selection window.
            mode_win.destroy()
            #Immediately starting the game.
            self.start_game()

        #Creating a variable to store the available game modes (with name, round number, and color). 
        modes = [
            ("Competitive", 30, "#ff8a65"),
            ("Normal", 70, "#4db6ac"),
            ("Easy", 99, "#9575cd")
        ]

        #Creating a loop over all available modes.
        for mode_name, rounds, color in modes:
            #Creating a colored block for each mode).
            frame = tk.Frame(mode_win, bg=color, bd=2, relief="ridge", padx=10, pady=10)
            #Placing the frame in the window.
            frame.pack(pady=8, fill="x", padx=20)
            #Adding descriptive text inside the frame.
            tk.Label(frame, text=f"{mode_name} ({rounds} rounds)", font=("Arial", 14, "bold"), bg=color, fg="white").pack(side="left", padx=5)
            #Creating a button to select the mode. 
            tk.Button(frame, text="Select", bg="white", fg=color, font=("Arial", 12, "bold"), command=lambda r=rounds: set_mode(r)).pack(side="right", padx=5)

    #Defining a method to begin/reset a new game session. 
    def start_game(self):
        #Creating a new bingo card object.
        self.card = BingoCard()
        #Creating a new number drawer object (tracking the numebr that have been drawn).
        self.drawer = NumberDrawer()
        #Creating a set of numbers that are marked on the user's card.
        self.marked = set()
        #Tracking which rows/columns have been counted as completed lines.
        self.completed_lines = set()
        #Resetting the number of draws made in this game. 
        self.current_round = 0
        #Resetting the count of lines made in this game. 
        self.total_lines = 0
        #Creating a flag indicating whether a full bingo has been achieved in this game.
        self.bingo_achieved = False

        # Reset drawn history
        #Creating a loop through all history labels currently on screen.
        for widget in self.scrollable_frame.winfo_children():
            #Removing each widget from GUI.
            widget.destroy()
            #Also clearing internal list tracking those labels. 
        self.drawn_history_labels.clear()

        #Displaying the new card on screen.
        self.display_card()
        #Enabling the draw button so the game can start. 
        self.draw_btn.config(state=tk.NORMAL)

    #Defining a method to draw the numebrs of the bingo card in the GUI grid. 
    def display_card(self):
        #Creating a loop through every widhget inside self.card_frame.
        for widget in self.card_frame.winfo_children():
            #Deleting each old label. 
            widget.destroy()

        #Creating a matrix storing label widgets for each numebr cell. 
        self.card_labels = []
        #Creating a loop over each row of the card numbers. 
        for r, row in enumerate(self.card.grid):
            #Hold the row's label widgets in a temporary list.
            row_labels = []
            #Creating a loop through each number in the row.
            for c, num in enumerate(row):
                #Creating a visual cell showing the number.
                lbl = tk.Label(self.card_frame, text=str(num), font=("Arial", 18, "bold"), width=4, height=2, bd=2, relief="ridge", bg="#ffffff")
                #Placing the label in the correct grid position. 
                lbl.grid(row=r, column=c, padx=5, pady=5)
                #Storing the label in this row. 
                row_labels.append(lbl)
            #Adding the completed row to the master grid.
            self.card_labels.append(row_labels)

    #Defining a method to update the sidebar list showing all numbers drawn.
    def update_drawn_history(self, number):
        #Creating a small label for the new drawn numebr. 
        lbl = tk.Label(self.scrollable_frame, text=str(number), font=("Arial", 12, "bold"), bg="#e0f7fa", fg="#000000", width=4, relief="ridge", bd=1)
        #Placing the label horizontally in the scrollable frame.
        lbl.pack(side="left", padx=2, pady=2)
        #Adding it to the internal list of history labels. 
        self.drawn_history_labels.append(lbl)
        #Scrolling the display to the far right, so the latest number is visible. 
        self.drawn_history_canvas.xview_moveto(1)

    #Defining a method to create the main logic for drawing the next random number.
    def draw_number(self):
        #Checking if drawer exists or round limit reached.
        if not self.drawer or self.current_round >= self.rounds:
            #In this case, ending the game immediately. 
            self.end_round()
            return

        #Running the visual animation before revealing the drawn number.
        self.roulette_animation()
        #Drawing a number from the available pool. 
        number = self.drawer.draw_number()
        #Checking if there are no numbers left to draw.
        if number is None:
            #In this case, ending the game.
            self.end_round()
            return

        #Incrementing the number of draws made by 1. 
        self.current_round += 1
        #Updating UI label to show the drawn number.
        self.drawn_label.config(text=str(number))
        #Adding the number to the visual scroll history.
        self.update_drawn_history(number)

        # Mark number on card
        #Creating a loop through all card cell values (all rows and all numbers). 
        for r, row in enumerate(self.card.grid):
            for c, num in enumerate(row):
                #Checking if the cell matches the drawn numebr.
                if num == number:
                    #In this case, changing its appearance to mark it visually. 
                    self.card_labels[r][c].config(bg="#81c784", fg="white")
                    #Recording this marked number logically. 
                    self.marked.add(num)

        #Checking whether the last draw completed a new horixontal/vertical line.
        if self.check_line():
            #In this case, displaying the LINE celebration message.
            self.show_effect("LINE")
        #Checking whether the last draw completed the entire card (bingo).
        if self.check_bingo():
            #In this case, marking the bingo achievement.
            self.bingo_achieved = True
            #Displaying the BINGO celebration message.
            self.show_effect("BINGO")
            #Disabling drawing further because the game is over (win). 
            self.draw_btn.config(state=tk.DISABLED)
            #Showing the game summary and exiting. 
            self.end_round()

    #Defining a method to determine if any new lines (row/columns) have been fully marked.
    def check_line(self):
        #Creating a flag to track whether a new line was found this draw.
        new_line = False
        #Storing the number of rows/columsn in the card (4x4).
        size = self.card.size

        # Check rows
        #Creating a loop through each row.
        for r in range(size):
            #Checking if the row was already counted as completed.
            if r in self.completed_lines:
                #In this case, skipping it. 
                continue
            #Checking if every cell in this row is marked.
            if all(self.card.grid[r][c] in self.marked for c in range(size)):
                #In this case, registering this row as completed.
                self.completed_lines.add(r)
                #Indicating a new line was found
                new_line = True

        # Check columns
        #Creating a loop through each column.
        for c in range(size):
            #Assigning each column a unique ID (distinct from row ID).
            col_id = c + size
            #Checking if the column was already counted as completed.
            if col_id in self.completed_lines:
                #In this case, skipping it. 
                continue
            #Checking if every cell in this column is marked.
            if all(self.card.grid[r][c] in self.marked for r in range(size)):
                #In this case, registering this column as completed.
                self.completed_lines.add(col_id)
                #Indicating a new line was found
                new_line = True

        #Returnin whether any new completed line was found. 
        return new_line

    #Defining a method to check if all the numbers on the card have been marked. 
    def check_bingo(self):
        #Returning True only if every number in the card is marked.
        return all(num in self.marked for num in self.card.get_card_numbers())

    #Defining a method to end the game (no more draws allowed). 
    def end_round(self):
        #Disabling draw button (so, no further interaction occurs).
        self.draw_btn.config(state=tk.DISABLED)
        #Creating a summary text for the final results pop-up. 
        summary = f"Round summary:\n- Rounds played: {self.current_round}\n- Lines: {len(self.completed_lines)}\n- Bingo: {'Yes' if self.bingo_achieved else 'No'}"

        #Creating the pop-up window to shor the resilts and the replay option. 
        replay_win = tk.Toplevel(self)
        #Setting the window title. 
        replay_win.title("Game Summary")
        #Setting the window size. 
        replay_win.geometry("300x200")
        #Keeping this window in focus until closed.
        replay_win.grab_set()

        #Displaying the result summary text.
        tk.Label(replay_win, text=summary, font=("Arial", 12), justify="left").pack(pady=10)
        #Asking the user whether they want to replay. 
        tk.Label(replay_win, text="Play again?", font=("Arial", 12, "bold")).pack(pady=5)

        #Creating a YES button (clicking it destroys the result pop-up and restarts the game).
        tk.Button(replay_win, text="Yes", font=("Arial", 12, "bold"), bg="#4db6ac", fg="white",
                  command=lambda: [replay_win.destroy(), self.start_game()]).pack(side="left", padx=30, pady=20)

        #Creating a NO button (clicking it destroys the result pop-up and exits the game).
        tk.Button(replay_win, text="No", font=("Arial", 12, "bold"), bg="#ff8a65", fg="white",
                  command=lambda: [replay_win.destroy(), self.quit()]).pack(side="right", padx=30, pady=20)


# Run game
#Ensuring this block only runs if this file is executed directly.
if __name__ == "__main__":
    #Creating the main window.
    app = MiniBingoGUI()
    #ENtering the Tkinter event loop to display and run the GUI
    app.mainloop()
