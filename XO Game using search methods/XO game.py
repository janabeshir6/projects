import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import copy
from queue import Queue, PriorityQueue

#Initializing the main window and its title
root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [['' for _ in range(3)] for _ in range(3)] #3x3 grid
player1 = 'X'  # Human player
player2 = 'O'  # Computer

buttons = [[None for _ in range(3)] for _ in range(3)] #Creating buttons for each cell in the grid

selectedAlgorithm = StringVar(root) #Creating a dropdown menu to choose between the search algorithms
selectedAlgorithm.set("DFS")  # Default selection


def checkWin(board, mark):
    for row in board: #Check all rows
        if all([cell == mark for cell in row]):
            return True
    for col in range(3): #Check all columns
        if all([board[row][col] == mark for row in range(3)]):
            return True
    if all([board[i][i] == mark for i in range(3)]) or all([board[i][2 - i] == mark for i in range(3)]): #Check diagonals
        return True
    return False


def checkFull(board): #Checking if board is full
    return all(cell != '' for row in board for cell in row)


def onClick(row, col): #Function is triggered when player clicks on cell
    #If cell is empty and player 2 hasn't won yet, then it's player 1's move
    if board[row][col] == '' and not checkWin(board, player2): 
        board[row][col] = player1
        buttons[row][col].config(text=player1) #Configure/update the button to show 'X' inputted by player 1
        if checkWin(board, player1):
            messagebox.showinfo("Tic-Tac-Toe", "Player 1 wins!")
            resetBoard()
            return
        elif checkFull(board): #Check if it's a draw
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            resetBoard()
            return
        # After player move, call computer's move
        computerMove()


def computerMove():
    # Call search algorithm to determine computer's move
    move = uninformedSearchMove(board)
    if move:
        row, col = move
        board[row][col] = player2
        buttons[row][col].config(text=player2) #Configures/updates the button selected to show O
        if checkWin(board, player2):
            messagebox.showinfo("Tic-Tac-Toe", "Player 2 (Computer) wins!")
            resetBoard()
        elif checkFull(board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            resetBoard()


# Depth-First Search (DFS) algorithm
def dfs(board):
    stack = [(copy.deepcopy(board), [])] #DFS uses stack (LIFO) (board state, move path)
    while stack:
        state, path = stack.pop()
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':
                    newState = copy.deepcopy(state)
                    newState[i][j] = player2
                    if checkWin(newState, player2):
                        return (i, j)
                    stack.append((newState, path + [(i, j)]))
    return path[0] if path else None #Returns the first move if no winning move is found


# Breadth-First Search (BFS) algorithm
def bfs(board):
    queue = Queue()
    queue.put((copy.deepcopy(board), []))
    while not queue.empty():
        state, path = queue.get()
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':
                    newState = copy.deepcopy(state)
                    newState[i][j] = player2
                    if checkWin(newState, player2):
                        return (i, j)
                    queue.put((newState, path + [(i, j)]))
    return path[0] if path else None


# Uniform Cost Search (UCS) algorithm
def ucs(board):
    queue = PriorityQueue()
    queue.put((0, copy.deepcopy(board), []))
    while not queue.empty():
        cost, state, path = queue.get()
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':
                    newState = copy.deepcopy(state)
                    newState[i][j] = player2
                    if checkWin(newState, player2):
                        return (i, j)
                    queue.put((cost + 1, newState, path + [(i, j)]))
    return path[0] if path else None


# Iterative Deepening Search algorithm
def iterativeDeepening(board, max_depth=5):
    for depth in range(1, max_depth + 1):
        move = depthLimited(board, depth)
        if move:
            return move
    return None


def depthLimited(board, limit):
    stack = [(copy.deepcopy(board), [], 0)]
    while stack:
        state, path, depth = stack.pop()
        if depth >= limit:
            continue
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':
                    newState = copy.deepcopy(state)
                    newState[i][j] = player2
                    if checkWin(newState, player2):
                        return (i, j)
                    stack.append((newState, path + [(i, j)], depth + 1))
    return path[0] if path else None


# Select search algorithm based on user choice
def uninformedSearchMove(board):
    if selectedAlgorithm.get() == "DFS":
        return dfs(board)
    elif selectedAlgorithm.get() == "BFS":
        return bfs(board)
    elif selectedAlgorithm.get() == "UCS":
        return ucs(board)
    elif selectedAlgorithm.get() == "Iterative Deepening":
        return iterativeDeepening(board)


# Reset the game board
def resetBoard():
    global board
    board = [['' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='')


# Initialize the board buttons and layout
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font='Helvetica 20 bold', height=3, width=6,
                                  command=lambda row=i, col=j: onClick(row, col))
        buttons[i][j].grid(row=i, column=j)

# Algorithm selection menu
algorithmMenu = OptionMenu(root, selectedAlgorithm, "DFS", "BFS", "UCS", "Iterative Deepening")
algorithmMenu.grid(row=3, column=0, columnspan=3)

root.mainloop()
