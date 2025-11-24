import random

#Defining a class named NumberDrawer, which draws unique random numbers. 
class NumberDrawer:
    """Handles random number drawing from 1–99 without repetition."""

    #Defining the constructor, including the parameter for maximum number (99).
    def __init__(self, max_number: int = 99):
        #Storing the maximum number that can be drawn.
        self.max_number = max_number
        #Creating a set containing the numbers that have not been drawn yet.
        #Initialized with every number from 1 to the maximum. 
        self.available_numbers = set(range(1, max_number + 1))
        #Initializing a list to keep track of the numbers that have already been drawn. 
        self.drawn_numbers = []

    #Defining a method to draw a new random number.
    def draw_number(self):
        """Draws a random number and removes it from the available pool."""
        #Checking if there are no numbers left to draw.
        if not self.available_numbers:
            #If there are none left, printing a message to tell the user that every number has been used.
            print(" All numbers have been drawn!")
            #Indicating that no new number could be drawn.
            return None

        #Randomly selecting a number from the set of available numbers, by converting it to a list first.
        number = random.choice(list(self.available_numbers))
        #Removing the drawn number from the set of available numbers.
        self.available_numbers.remove(number)
        #Adding the drawn number to the set of already selected number.
        self.drawn_numbers.append(number)
        #Returning the drawn number.
        return number

    #Defining a method to show every number that has been drawn so far.
    def display_drawn_numbers(self):
        """Displays all drawn numbers in sorted order."""
        #Printing the title "Numbers drawn so far:".
        print("\n Numbers drawn so far:")
        #Checking if any number has been drawn yet.
        if self.drawn_numbers:
            #If numbers exist, converting them to strings, sorting them, and printing them separated by a comma.
            print(", ".join(map(str, self.drawn_numbers)))
        else:
            #If numbers don't exist, informing the user no draws have ocurred yet. 
            print(" No numbers drawn yet.")
