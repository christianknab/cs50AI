"""
Tic Tac Toe Player
"""

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    sum1 = sum([i.count(EMPTY) for i in board])
    
    if sum1 % 2 != 0:
        return X
    if sum1 % 2 == 0:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Loop through every element on the board
    for i in range(3):
        for j in range(3):

            # Add possible action if EMPTY element
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep copy board
    board_copy = deepcopy(board)
    i, j = action

    # Create new board if possible
    if board_copy[i][j] != EMPTY:
        raise Exception
    else:
        board_copy[i][j] = player(board)
    
    return board_copy


def checkRow(board):
    """Returns player if there is a row win"""
    # Loop through each row
    for i in range(3):
        row = set()

        # Loop though each element in the row
        for j in range(3):
            row.add(board[i][j])

        # If only one unique element that is not empty, return the player
        if len(row) == 1:
            if EMPTY not in row:
                return list(row)[0]

    return None


def checkColumn(board):
    """Returns player if there is a column win"""
    # Loop through each row
    for i in range(3):
        col = set()

        # Loop though each element in the row
        for j in range(3):
            col.add(board[j][i])

        # If only one unique element that is not empty, return the player
        if len(col) == 1:
            if EMPTY not in col:
                return list(col)[0]

    return None
            

def checkDiagonal(board):
    """Returns player if there is a diagonal win"""
    # Check left to right diagonal
    if len(set([board[i][i] for i in range(3)])) == 1:
        return board[0][0]

    # Check right to left diagonal
    if len(set([board[i][2 - i] for i in range(3)])) == 1:
        return board[0][2]

    return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check win in a row
    if checkRow(board) != None:
        return checkRow(board)

    # Check win in a column
    elif checkColumn(board) != None:
        return checkColumn(board)

    # Check win in a diagonal
    elif checkDiagonal(board) != None:
        return checkDiagonal(board)

    # No win
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def maxValue(state):
        """
        Picks the action with the highest value of minValue()
        """
        best_action = ()

        # Check if the board is done
        if terminal(state):
            return utility(state), best_action

        # Set initial minimum value
        v = -5

        # Loop through each possible action
        for action in actions(state):

            # Find the minimum value from the result of each action
            temp = minValue(result(state, action))[0]

            # Choose the largest minimum value
            if temp > v:
                best_action = action
                v = temp

        return v, best_action


    def minValue(state):
        """
        Picks the action with the lowest value of maxVlaue()
        """
        best_action = ()

        # Check if the board is done
        if terminal(state):
            return utility(state), best_action
    
        # Set initial maximum value
        v = 5

        # Loop through each possible action
        for action in actions(state):

            # Find the maxiumum value from the result of each action
            temp = maxValue(result(state, action))[0]

            # Choose the smallest maximum value
            if temp < v:
                best_action = action
                v = temp

        return v, best_action


    # Check if game is over
    if terminal(board):
        return None

    current_player = player(board)

    # Return value based on whose turn it is
    if current_player == X:
        return maxValue(board)[1]
    else:
        return minValue(board)[1]
