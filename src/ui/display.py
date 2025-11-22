from src.game.card import BingoCard
from src.game.draw import NumberDrawer
from dataclasses import dataclass
from tabulate import tabulate


@dataclass
#Defining a class named History as a dataclass, which automatically generates an initializer and representation.
class History:
    """Tracks the current playing session: games played, wins, and losses."""
    #Defining a data attribute with the values of total games played. Initializing the attribute at 0.
    games_played: int = 0
    #Defining a data attribute with the values of number of wins. Initializing the attribute at 0.
    wins: int = 0
    #Defining a data attribute with the values of number of losses. Initializing the attribute at 0.
    losses: int = 0

    #Defining a method to update the game statistics
    def update_history(self, win: bool):
        """Updates the count of games played, wins, and losses."""
        #Incrementing the total count of completed game by 1.
        self.games_played += 1
        #Checking if the game was won.
        if win:
            #In this case, incrementing the win counter by one. 
            self.wins += 1
        #If the game was lost.
        else:
            #In this case, incrementing the loss counter by one.
            self.losses += 1

    #Defining a method to show the summary of accumulated results.
    def print_summary(self):
        """Displays the session summary in a table."""
        #Creating a list of lists, where each row represents one statistic (attribute) and its value. 
        data = [
            ["Rounds Played", self.games_played],
            ["Wins", self.wins],
            ["Losses", self.losses]
        ]
        #Setting a title to display before the summary of results table. 
        title = "📊SESSION SUMMARY"
        #Printing the title and a line separator of matching width. 
        print(f"\n{title}\n" + "-" * (len(title) + 2))
        #Displaying the summary of the results in a formatted grid style.
        print(tabulate(data, headers=["Statistic", "Count"], tablefmt="fancy_grid"))

#Defining a class named InfoTab, which displays the rules of the game
class InfoTab:
    """Displays the rules to follow the game."""

    #Defining the initializer method.
    def __init__(self):
        #Creating a list of strings containing the rules that will be displayed to the player. 
        self.rules_text = [
            "MINI BINGO RULES",
            "---------------------------",
            "• The game uses a 4x4 Bingo card.",
            "• Numbers are drawn from 1 to 99.",
            "• Numbers appear one at a time.",
            "• A LINE is completed when an entire row or column is marked.",
            "• BINGO is achieved when all numbers are marked."
        ]

    #Defining a method to print the game rules. 
    def display(self):
        #Printing a title for the rule section.
        print("\n=== INFORMATION TAB ===\n")
        #Creting a loop through the rules in the list.
        for line in self.rules_text:
            #Printing each line. 
            print(line)
        #Printing a closing line for visual separation.
        print("=======================\n")


#Defining a class named MiniBingo, which represents the main game controller for the console version.
class MiniBingo:
    """Console interface that connects the card and number drawer."""

    #Defining the constructor to initialize a new game. 
    def __init__(self):
        #Creating a new bingo card for the player.
        self.card = BingoCard()
        #Creating a number drawer instance to provide random non-repeating numbers.
        self.drawer = NumberDrawer()
        #Initializing the number of rounds to 0 (will be set depending on the mode chosen).
        self.rounds = 0
        #Creating an info instance to display the rules during the game.
        self.info = InfoTab()

    #Defining a method to let the user select from predefined game lengths. 
    def choose_mode(self):
        """Lets the player choose one of three predefined modes."""
        #Displaying the available mode options to the player.
        print("\n🎮 Choose Game Mode:")
        print("1. Competitive (30 rounds)")
        print("2. Normal (45 rounds)")
        print("3. Easy (99 rounds)")

        #Starting a loop that continues until the user makes a valid choice. 
        while True:
            #Asking the player for input: select a mode. The answer is standardized: whitespaces are removed.
            choice = input("Select a mode (1, 2, or 3): ").strip()

            #Checking if the user input is "1"
            if choice == "1":
                #Setting the round count to 30.
                self.rounds = 30
                #Printing the mode selected: Competitive, and the number of rounds: 30 to the user. 
                print("\n🏁 Mode selected: Competitive (30 rounds)")
                break
            #Checking if the user input is "2"
            elif choice == "2":
                #Setting the round count to 70.
                self.rounds = 70
                #Printing the mode selected: Normal, and the number of rounds: 70 to the user. 
                print("\n🎯 Mode selected: Normal (70 rounds)")
                break
            #Checking if the user input is "3"
            elif choice == "3":
                #Setting the round count to 99 (maximum number).
                self.rounds = 99
                #Printing the mode selected: Eary, and the number of rounds: 99 to the user.
                print("\n🌿 Mode selected: Easy (99 rounds)")
                break
            #Handling any other user input.
            else:
                #Displaying an error message and re-prompting.
                print("⚠️ Invalid option. Please choose 1, 2, or 3.")

    #Defining a method to run a full game session. 
    def start(self):
        """Starts the Bingo game with chosen mode and manual round progression."""
        #Preinting a welcome message.
        print("\n🧩 Welcome to Mini Bingo 🧩")
        #Calling the mode selection method.
        self.choose_mode()
        #Displaying the rules.
        self.info.display()
        #Showing the initial bingo card. 
        self.card.display_card()

        #Creating a flag indicating whether the player wins the game. Initialized as False. 
        won = False

        #Creating a loop through each round, starting at 1 up to the number of rounds selected.
        for round_number in range(1, self.rounds + 1):
            #Prompting the user to proceed to the next draw (next round).
            input(f"\n👉 Press Enter to draw number for Round {round_number}...")

            #Drawing a number from the random pool.
            number = self.drawer.draw_number()
            #Checking if no number remains available.
            if number is None:
                #Notifying the player that there are no numbers left to be drawn.
                print("No more numbers to draw.")
                #Ending the game loop.
                break

            #Displaying the newly drawn number.
            print(f"➡️ Drawn number: {number}")

            #Checking if the number exists on the card and marking it.
            if self.card.mark_number(number):
                #Informing the player that the number was found and marked. 
                print("Number found and marked on your card!")
            #If the number isn't present. 
            else:
                #Informing the player that the number was not found.
                print("Number not on your card.")

            #Displaying the rules again.
            self.info.display()
            #Showing the updated card state (with the possible new marked number).
            self.card.display_card()
            #Showing all the previously drawn numbers.
            self.drawer.display_drawn_numbers()

            #Checking if the latest move completed a line (row or column).
            if self.card.check_line():
                #If true, announcing it. 
                print("🎉 LINE! You completed a row or column!")

            #Checking if the latest move completed the full card (bingo).
            if self.card.check_bingo():
                #If true, announcing it. 
                print("🏆 BINGO! You completed the entire card!")
                #Updating the win flag.
                won = True
                #Ending the game loop.
                break

        #Printing a closing message after the loop finishes.
        print("\nThanks for playing")
