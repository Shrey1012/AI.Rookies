import numpy as np
import random
import json


# Function to save data as JSON
def saveData(data):
    with open('data.json', 'w') as outfile:
        json.dump(data.__dict__, outfile)


# Class representing the Menace Player
class Menace:
    def __init__(self):
        # Dictionary to store the matchboxes
        self.matchboxes = {}
        # Counter for number of wins, draws and losses
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0

    # Function to save the data to a JSON file
    def save(self):
        saveData(self)


# Function to check if the move is valid
def ValidMove(board, move):
    if 0 <= move <= 8 and board[move] == " ":
        # If the move is within the range 0-8 and the spot is empty, it is a valid move
        return True
    else:
        # Otherwise, it is an invalid move
        return False


# Define a function to get empty spaces in the board
def getEmptySpaces(currentState):
    count = []
    for i in range(len(currentState)):
        if currentState[i] == ' ':
            count.append(i)
    return np.array(count)


# Define a function to print the current state of the board
def printBoard(board):
    print("\n    %s | %s | %s\n"
          "  ---+---+---\n"
          "    %s | %s | %s\n"
          "   ---+---+---\n"
          "    %s | %s | %s" % (board[0], board[1], board[2],
                                board[3], board[4], board[5],
                                board[6], board[7], board[8]))


# Define a function to check if game over and return the value accordingly
def isGameOver(currentState):
    # Copy the current state to a new variable 'state'
    state = currentState.copy()

    # check for Horizontal win
    for i in range(0, 7, 3):
        if state[i] == state[i + 1] == state[i + 2]:
            if state[i] == 'X':
                return 10
            elif state[i] == 'O':
                return -10

    # check vertical win
    for i in range(0, 3):
        if state[i] == state[i + 3] == state[i + 6]:
            if state[i] == 'X':
                return 10
            elif state[i] == 'O':
                return -10

    # check diagonal win
    if state[0] == state[4] == state[8]:
        if state[0] == 'X':
            return 10
        elif state[0] == 'O':
            return -10
    if state[2] == state[4] == state[6]:
        if state[2] == 'X':
            return 10
        elif state[2] == 'O':
            return -10

    # Check if it is a draw
    if len(getEmptySpaces(state)) == 0:
        return 0

    # Return -1 if game is not over
    return -1


def GetMove(board, player):
    """
    This function returns a move for a given player and board state.

    Args:
    board: array representing the current state of the board
    player: instance of the Menace class

    Returns:
    If player is a Menace instance, returns the index of the move to be made.
    If player is None, prompts user for input and returns the integer value entered.

    """
    if player:
        # Convert board to a string for use as a dictionary key
        board = ''.join(board)

        # If current board state has not been seen before, initialize matchbox with beads for each possible move
        if board not in player.matchboxes:
            new_beads = [index for index, value in enumerate(board) if value == ' ']
            player.matchboxes[board] = new_beads * ((len(new_beads) + 2) // 2)

        # Randomly choose a bead from the current matchbox and record the move
        beads = player.matchboxes[board]
        if len(beads):
            bead = random.choice(beads)
            player.moves_played.append((board, bead))
        else:
            bead = -1
        return bead

    else:
        # Prompt user for input and validate move
        while True:
            move = int(input("Enter your move : "))
            if ValidMove(board, move):
                return move
            else:
                print("Invalid Input")


def SetMenaceData(player, result):
    """
    Updates the matchboxes and statistics for the given Menace instance based on the game outcome.

    Args:
    player: instance of the Menace class
    result: string indicating the outcome of the game (win, lose, or draw)

    """
    if result == "win":
        # If player won, add 3 beads to the matchboxes corresponding to all moves played
        for (board, bead) in player.moves_played:
            player.matchboxes[board].extend([bead, bead, bead])
        player.num_win += 1
    elif result == "lose":
        # If player lost, remove the bead used for each move played from the corresponding matchboxes
        for (board, bead) in player.moves_played:
            matchbox = player.matchboxes[board]
            del matchbox[matchbox.index(bead)]
        player.num_lose += 1
    elif result == "draw":
        # If game was a draw, add a bead to the matchboxes corresponding to all moves played
        for (board, bead) in player.moves_played:
            player.matchboxes[board].append(bead)
        player.num_draw += 1

    # Save the updated player instance
    player.save()


def TrainMenace(player1, player2):
    """
    Trains two Menace instances by playing a series of Tic Tac Toe games.

    Args:
    player1: instance of the Menace class
    player2: instance of the Menace class

    """
    # Play 500 games between the two Menace players
    for i in range(0, 500):
        # Reset the moves_played list and the game board for each iteration
        player1.moves_played = []
        player2.moves_played = []
        # Create a new empty board
        board = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

        # Play the game until a winner is determined
        while isGameOver(board) == -1:
            move = GetMove(board, player1)
            board[move] = "O"
            move = GetMove(board, player2)
            board[move] = "X"
        points = isGameOver(board)
        if points == 10:
            SetMenaceData(firstPlayer, "win")
        elif points == -10:
            SetMenaceData(firstPlayer, "lose")
        elif points == 0:
            SetMenaceData(firstPlayer, "draw")


# create a new instance of Menace and assign it to firstPlayer
firstPlayer = Menace()

try:
    # try to open data.json and read its contents
    f = open('data.json')
    content = f.read()

    # if the file has content, load the saved data into firstPlayer's attributes
    if len(content) > 0:
        savedData = json.load(open('data.json'))
        firstPlayer.matchboxes = savedData["matchboxes"]
        firstPlayer.num_win = savedData["num_win"]
        firstPlayer.num_lose = savedData["num_lose"]
        firstPlayer.num_draw = savedData["num_draw"]
except:
    # if the file does not exist or is empty, train firstPlayer and a new instance of Menace named secondPlayer
    secondPlayer = Menace()
    TrainMenace(firstPlayer, secondPlayer)
    print("No Pre Game exist")

# open data.json again and create a new instance of Menace named secondPlayer
f = open('data.json')
content = f.read()
secondPlayer = Menace()

# train secondPlayer with firstPlayer by calling the TrainMenace function
TrainMenace(firstPlayer, secondPlayer)

print("No Pre Game exist")

board = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
printBoard(board)

choice = input("Enter 'y' if you want to play the first move:")
firstPlayer.moves_played = []
if choice.lower() == 'y' or choice.lower() == 'yes':
    print("You are O")
    printBoard(board)
    while isGameOver(board) == -1:
        move = GetMove(board, None)
        board[move] = "O"
        printBoard(board)
        if isGameOver(board) != -1:
            break
        move = GetMove(board, firstPlayer)
        board[move] = "X"
        printBoard(board)
        print("\nMENACE moved : ", move)
    # if you win -10 is returned
    # if you lose 10 is returned
    # if it is a draw 0 is returned
    points = isGameOver(board)
    if points == 10:
        SetMenaceData(firstPlayer, "win")
    elif points == -10:
        SetMenaceData(firstPlayer, "lose")
    elif points == 0:
        SetMenaceData(firstPlayer, "draw")
else:
    print("You are X")
    printBoard(board)
    while isGameOver(board) == -1:
        move = GetMove(board, firstPlayer)
        board[move] = "O"
        printBoard(board)
        print("\nMENACE moved : ", move)
        if isGameOver(board) != -1:
            break
        move = GetMove(board, None)
        board[move] = "X"
        printBoard(board)

    # if you win 10 is returned
    # if you lose -10 is returned
    # if it is a draw 0 is returned
    points = isGameOver(board)
    if points == -10:
        SetMenaceData(firstPlayer, "win")
    elif points == 10:
        SetMenaceData(firstPlayer, "lose")
    elif points == 0:
        SetMenaceData(firstPlayer, "draw")
