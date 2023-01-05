from copy import deepcopy
import itertools
from os import remove
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark cell as one of the moves made in the game
        self.moves_made.add(cell)

        # Mark as a safe cell
        self.mark_safe(cell)

        # Initialize variables
        cells = set()
        count_copy = deepcopy(count)
        
        # Find all surrounding cells
        surrounding_cells = self.surrounding_cells(cell)

        # Creating new knowledge set
        # For every cell in the surrounding cells
        for c in surrounding_cells:

            # If the cell is a known mine, take away one count for subset
            if c in self.mines:
                count_copy -= 1

            # If the cell is not a known mine or safe, add to subset
            if c not in self.mines | self.safes:
                cells.add(c)
        
        # Add new knowledge object
        new_sentence = Sentence(cells, count_copy)

        # If the new sentence has knowledge information, add to knowledge list
        if len(new_sentence.cells) != 0:
            self.knowledge.append(new_sentence)

        # Update known mines and safes
        self.update_knowledge()

        # Make a deeper inference with subset method
        self.subset_method()


    def surrounding_cells(self, cell):
        """
        Returns all surrounding cells around cell
        """
        
        surrounding_cells = set()
        for row in range(self.height):
            for col in range(self.width):
                if abs(cell[0] - row) <= 1 and abs(cell[1] - col) <= 1 and (row, col) != cell:
                    surrounding_cells.add((row, col))

        return surrounding_cells
    

    def update_knowledge(self):
        """
        Looks through existing knowledge to check for new found safes and mines
        """
        # Make deep copy of knowledge
        knowledge_copy = deepcopy(self.knowledge)


        # Loop through every logic sentence in knowledge
        for sentence in knowledge_copy:

            # Delete every empty knowledge sentence
            if len(sentence.cells) == 0:
                try:
                    self.knowledge.remove(sentence)
                except ValueError:
                    pass
            
            # Look at all known mines and safes per logic sentence
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            # Mark every mine and safe in overall knowledge
            if mines:
                for mine in mines:
                    self.mark_mine(mine)
                    self.update_knowledge()            # Call itself because new mine found
            
            if safes:
                for safe in safes:
                    self.mark_safe(safe)
                    self.update_knowledge()            # Call itself because new safe found


    def subset_method(self):
        """
        Uses the subset method to make inferences and change current
        knowledge based on surrounding knowledge
        """
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:

                # If sentence 1 is a subset of sentence 2
                if sentence1.cells.issubset(sentence2.cells):

                    # Update new logic sentence using the subset method
                    updated_cells = sentence2.cells - sentence1.cells
                    updated_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(updated_cells, updated_count)

                    # Find every known safe and mine per sentence
                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()

                    # If there are known safes and mines, mark it
                    if mines:
                        for mine in mines:
                            self.mark_mine(mine)
                    
                    if safes:
                        for safe in safes:
                            self.mark_safe(safe)
                    

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Initialize variables
        moves_made = self.moves_made
        safes = self.safes

        # Return a safe move in safe set as long as the move hasn't been made
        for safe in safes:
            if safe not in moves_made:
                return safe
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Initialize variables
        height = self.height
        width = self.width
        unknown_cells = []

        # Add unknown cells to list
        for row in range(height):
            for col in range(width):
                cell = (row, col)
                if cell not in self.mines and cell not in self.moves_made:
                    unknown_cells.append(cell)
        
        length = len(unknown_cells)

        # If there are cells left, choose a random index
        if length != 0:
            random_number = random.randrange(length)
            return unknown_cells[random_number]
        return None