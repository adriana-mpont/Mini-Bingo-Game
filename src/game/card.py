import random

#Defining a class named BingoCard, which represents a single bingo card.
class BingoCard:
    """Represents a 4x4 Bingo card with unique random numbers."""

    #Defining the constructor, including parameters for card size and maximum number.
    def __init__(self, size: int = 4, number_range: int = 99):
        #Storing the size of the bingo card: 4x4.
        self.size = size
        #Storing the maximum number that can appear on the card.
        self.number_range = number_range
        #Generating the bingo card grid, using the method _generate_card().
        self.grid = self._generate_card()
        #Creating a matrix of the same size as the card (4x4) to track whether each cell has been marked.
        #All cells are initialized as False.
        self.marked = [[False for _ in range(self.size)] for _ in range(self.size)]
        #Initializing a list tracking whether each row has already been declared a completed line.
        #To prevent repeated messages.
        self.line_rows_announced = [False] * self.size
        #Initializing a list tracking whether each column has already been declared a completed line.
        #To prevent repeated messages.
        self.line_cols_announced = [False] * self.size

    #Defining a helper method that creates the card. 
    def _generate_card(self):
        """Generates a grid of unique random numbers between 1–99."""
        #Randomly selecting 4x4 (size) unique numbers within the allowed range.
        numbers = random.sample(range(1, self.number_range + 1), self.size ** 2)
        #Slicing the list of elements to form a matrix of size 4x4 (grid).
        return [numbers[i:i + self.size] for i in range(0, len(numbers), self.size)]

    #Defining a method to validate the card created.
    def validate_card(self) -> bool:
        """Validates that the card contains 16 unique numbers within range."""
        #Retrieving all numbers from the grid in a flat list, using the method get_card_numbers().
        flat_numbers = self.get_card_numbers()
        #Checking that all the numbers in the card are unique (no duplicates).
        #And checking that every number is within the allowed range. 
        return len(flat_numbers) == len(set(flat_numbers)) and all(
            1 <= n <= self.number_range for n in flat_numbers
        )

    #Defining a helper method that returns all numbers in a single flat list.
    def get_card_numbers(self):
        """Returns all numbers in a flat list."""
        #Flattening all the numbers from the matrix (grid) into a 1D list.
        return [num for row in self.grid for num in row]

    #Defining a method to mark a number if it is present on the card.
    def mark_number(self, number: int) -> bool:
        """Marks the number on the card if found. 
        Returns True if the number was present and marked, False otherwise. """
        #Creating a loop through each row.
        for i in range(self.size):
            #Creating a loop through each column (within the row).
            for j in range(self.size):
                #Checking if the current cell matches the number.
                if self.grid[i][j] == number:
                    #If the current cell matches the number, marking it as True.
                    self.marked[i][j] = True
                    #Returning True if the number was marked and found.
                    return True
        #Returning False if the number was not found, therefore not marked. 
        return False

    #Defining a method to show the card on the screen.        
    def display_card(self):
        """Displays the Bingo card in a grid format."""
        #Printing the title "Your Bingo Card".
        print("\n Your Bingo Card")
        #Printing a separator before showing the grid.
        print("-" * (self.size * 6))

        #Creating a loop over the size of the matrix (grid).
        for i in range(self.size):
            #Initializing a list to display each row. 
            row_display = []
            #Creating a loop over each cell of the row.
            for j in range(self.size):
                #Getting the number present in that cell.
                num = self.grid[i][j]
                #Checking if the number has already been marked.
                if self.marked[i][j]:
                    #If marked, storing the number inside brackets.
                    row_display.append(f"[{num:02}]")  
                else:
                    #If not marked, storing the number without brackets.
                    row_display.append(f" {num:02} ") 
            #Printing the completed row.
            print(" ".join(row_display))
        #Printing another separator after the grid.
        print("-" * (self.size * 6))

    #Defining a method to check if any full row or column has been completed (all numbers marked).
    def check_line(self) -> bool:
        """Checks if any row or column is fully marked (a 'Line')."""
        #Creating a loop through each row and each number in it. 
        for i, row in enumerate(self.marked):
            #Checking if the row is fully marked, and if it hasn't been announced already.
            if all(row) and not self.line_rows_announced[i]:
                #In this case, marking the row as announced.
                self.line_rows_announced[i] = True
                #Returning True because a new line was completed. 
                return True

        #Creating a loop through each column index. 
        for j in range(self.size):
            #Checking if the column is fully marked, and if it hasn't been announced already.
            if all(self.marked[i][j] for i in range(self.size)) and not self.line_cols_announced[j]:
                #In this case, marking the column as announced.
                self.line_cols_announced[j] = True
                #Returning True because a new line was completed.
                return True

        #Returning False is no new row or columns has been completed. 
        return False

    #Defining a method to check if the entire card has been completed (all number marked).
    def check_bingo(self) -> bool:
        """Checks if the entire card is marked (a 'Bingo')."""
        #Checking if every cell in the grid is marked. And returning True if the entire card is completed. 
        return all(all(row) for row in self.marked)
