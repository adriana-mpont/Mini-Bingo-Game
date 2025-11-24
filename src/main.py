
from ui.display import History
from ui.display import InfoTab
from ui.display import MiniBingo

#Defining the main function hat runs the Bingo session
def main():
    """Run a minimal playable Mini Bingo session (Sprint 2 demo)."""
    #Creting a History object to track the results of completed matches.
    history = History()
    #Creating a InfoTab object to display game information and instructions.
    info = InfoTab()
    #Initializing a counter for the number of games played. Starting the matches counter at match 1. 
    matches = 1

    #Starting an infinite loop that allows the player to continue playing new matches until they decide to stop. 
    while True: 
        #Displaying the game information to the player
        info.display()
        #Creating an instance of the game logic calling the class MiniBingo. 
        game = MiniBingo()
        #Starting the gameplay session (rounds are handled and advanced inside display.py for manual mode selection).
        #Storing the results of the matches (indicating whether the player won the matches).
        did_win = game.start()
        #Updating the matches history with the result of the match. 
        history.update_history(did_win)
        #Starting another loop to repeatedly ask the player whether they want to play again, until opposite input is given.
        while True:
            #Asking the player for input: if they want (yes) or not (no) to play another round.
            #The answer is standardized: whitespaces are removed and it is converted to lowercase.
            replay = input("\nWould you like to play another round? (Yes / No): ").strip().lower()
            #Checking if the user input is "yes" (so, if they want to play again).
            if replay == "yes":
                #Printing a summary of the previous matches played so far.
                history.print_summary()
                #Incrementing the match counter by one.
                matches += 1
                #Displaying a massage announting the new match number.
                print(f"\nStarting match number {matches}.\nGood luck!")
                #Breaking out the replay loop and starting the nexr match
                break
            #Checking if the user input is "no" (so, if they choose to stop playing).
            elif replay == "no":
                #Printing the final  summary of all recorded matches.
                history.print_summary()
                history.save()
                #Displaying a closing message for the eng of the game session.
                print("\nThe game has finished. Thank you for playing!\n")
                #Exiting the main() function, and ending the program.
                return
            #Handling any other user input. 
            else:
                #Displaying an error message and re-prompting.
                print("⚠️ Invalid input. Please type 'yes' or 'no'.")

#Ensuring this block only runs if this file is executed directly.
if __name__ == "__main__":
    #Creating a new instance of the graphical visualization.
    main()

