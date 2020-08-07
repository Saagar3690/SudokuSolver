import random
import time

iterations = 0

'''board = [
  [7,8,0,4,0,0,1,2,0],
  [6,0,0,0,7,5,0,0,9],
  [0,0,0,6,0,1,0,7,8],
  [0,0,7,0,4,0,2,6,0],
  [0,0,1,0,5,0,9,3,0],
  [9,0,4,0,6,0,0,0,5],
  [0,7,0,3,0,0,0,1,2],
  [1,2,0,0,0,7,4,0,0],
  [0,4,9,2,0,6,0,0,7],
]'''

gameboard = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
  ]

def deleteCells(cellsToDelete):
  #print(cellsToDelete)
  if cellsToDelete == 0:
    return True

  while True:
    while True:
      row = random.randint(0, 8)
      col = random.randint(0, 8)
      if gameboard[row][col] != 0:
        break
    val = gameboard[row][col]
    gameboard[row][col] = 0
    if solveable(gameboard) == 1:
      return deleteCells(cellsToDelete-1)
    gameboard[row][col] = val

# Generates a Fully Solved Board
def generate():
  found, row, col = find_empty(gameboard)

  if not found:
    return True

  nums = [1,2,3,4,5,6,7,8,9]
  random.shuffle(nums)
  for num in nums:
    if checkRow(gameboard, num, row) and checkCol(gameboard, num, col) and checkBox(gameboard, num, row, col):
      gameboard[row][col] = num
      if generate():
          return True
      gameboard[row][col] = 0

  return False

def solveable(board, count=0):
  # Find the first empty cell - left to right first, then up to down
  found, row, col = find_empty(board)

  # No empty cells indicates board is solved - base case
  if not found:
    return count+1

  # Try all values 1-10 in order
  for i in (range(1, 10)):
    # Check if the value fits into the board - is valid in the row, column, and box
    if checkRow(board, i, row) and checkCol(board, i, col) and checkBox(board, i, row, col):
      # set the location in board to that value
      board[row][col] = i
      # call itself to find subset of solution
      count = solveable(board, count)
      # if previous subset solution doesn't work, reset the value at location in board
      board[row][col] = 0

  # if there are no values that make it work, the board cannot be solved
  return count


def solve(board, window, tk, start):
  # Find the first empty cell - left to right first, then up to down
  found, row, col = find_empty(board)

  # No empty cells indicates board is solved - base case
  if not found:
    return True

  # Try all values 1-10 in order
  for i in (range(1, 10)):
    global iterations
    iterations+=1
    # Check if the value fits into the board - is valid in the row, column, and box
    if checkRow(board, i, row) and checkCol(board, i, col) and checkBox(board, i, row, col):
      # set the location in board to that value
      board[row][col] = i
      # Redraw grid
      window.redraw(board)
      tk.update()
      # call itself to find subset of solution
      if solve(board, window, tk, start):
        return True
      # if previous subset solution doesn't work, reset the value at location in board
      board[row][col] = 0

  # if there are no values that make it work, the board cannot be solved
  return False

# Finds first empty cell in board
def find_empty(board):
  for row in range(9):
    for col in range(9):
      if board[row][col] == 0:
        return True, row, col

  return False, -1, -1

# Checks if the value already exists in the row
def checkRow(board, i, row):
  for col in range(9):
    if board[row][col] == i:
      return False

  return True

# Checks if the value already exists in the column
def checkCol(board, i, col):
  for row in range(9):
    if board[row][col] == i:
      return False

  return True

# Checks if the value already exists in the 3x3 box
def checkBox(board, i, row, col):
  row_start = row - row % 3
  col_start = col - col % 3

  for r_cnt in range(row_start, row_start + 3):
    for c_cnt in range(col_start, col_start + 3):
      if board[r_cnt][c_cnt] == i:
        return False

  return True

# Prints the Sudoku Board
def printBoard(board):
  for row in range(9):
    for col in range(9):
      print(board[row][col], end = " ")
    print('')

def user_input():
  mode = input("Enter c if you want to enter your own board or r for a randomly generated board:\t")
  if mode == 'c':
    board_input = input("Enter your board row by row in one line without spaces. Use 0 for empty spaces (e.g 780400120600075009000601078007040260001050930904060005070300012120007400049206007): \n")

    board = []
    for i in range(9):
      row = [int(board_input[j]) for j in range(9*i, 9*(i+1))]
      board.append(row)

    return board
  elif mode == 'r':
    generate()
    levels = {
      'easy': 30,
      'medium': 40,
      'hard': 50,
      'very hard': 55
    }
    level = input("Please choose the level: easy, medium, hard, very hard:\t")
    deleteCells(levels[level])

    return gameboard

'''printBoard(board)
print('-----------------')
if solve(board):
  printBoard(board)
else:
  print("This board is unsolvable")


generate()
printBoard(gameboard)
print('-----------------')
levels = {
  'easy': 30,
  'medium': 40,
  'hard': 50,
  'very hard': 55
}
level = random.choice(list(levels.keys()))
deleteCells(levels[level])
printBoard(gameboard)
print(level)
'''
