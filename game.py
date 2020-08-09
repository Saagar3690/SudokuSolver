import random
import time

iterations = 0

# empty board
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



# Delete cellsToDelete number of cells to create a proper sudoku board
def deleteCells(cellsToDelete):
  # base case - if the number of cells to delete has been reached (based on level), return True, indicating the board is done
  if cellsToDelete == 0:
    return True

  # runs until a proper board has been created
  while True:
    # generate the coordinates of the cell until the coordinates lead to a cell that is not empty (0)
    while True:
      row = random.randint(0, 8)
      col = random.randint(0, 8)
      if gameboard[row][col] != 0:
        break
    # store the current value in cell in case it needs to be reverted
    val = gameboard[row][col]
    # set value of current cell to 0
    gameboard[row][col] = 0
    # check if the board is still solvable based on the last deletion, if true, call itself
    if solveable(gameboard) == 1:
      return deleteCells(cellsToDelete-1)
    # since board wasn't solvable, revert the value of the current cell to its old value
    gameboard[row][col] = val




# Generates a Fully Solved Board
def generate():
  # Find the first empty cell - left to right first, then up to down
  found, row, col = find_empty(gameboard)

  # No empty cells indicates board is solved - base case
  if not found:
    return True

  # possible values 1-9
  nums = [1,2,3,4,5,6,7,8,9]
  # randomize the order of nums
  random.shuffle(nums)
  # Try all values in nums based on the random order
  for num in nums:
    # Check if the value fits into the board - is valid in the row, column, and box
    if checkRow(gameboard, num, row) and checkCol(gameboard, num, col) and checkBox(gameboard, num, row, col):
      # set the location in board to that value
      gameboard[row][col] = num
      # call itself to find subset of board
      if generate():
          return True
      # if previous subset of board doesn't work, reset the value at location in board
      gameboard[row][col] = 0

  # if none of the values work, return to previous recursive call
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

  # return the number of different solutions generated for this board
  return count




def solve(board, window, tk, start):
  # Find the first empty cell - left to right first, then up to down
  found, row, col = find_empty(board)

  # No empty cells indicates board is solved - base case
  if not found:
    return True

  # redraw a red border around the current cell for visualizing
  window.redraw(board, row, col)
  tk.update()

  # Try all values 1-10 in order
  for i in (range(1, 10)):
    global iterations
    iterations+=1
    # Check if the value fits into the board - is valid in the row, column, and box
    if checkRow(board, i, row) and checkCol(board, i, col) and checkBox(board, i, row, col):
      # set the location in board to that value
      board[row][col] = i
      # Redraw grid
      window.redraw(board, row, col)
      tk.update()
      # call itself to find subset of solution
      if solve(board, window, tk, start):
        return True
      # if previous subset solution doesn't work, reset the value at location in board
      board[row][col] = 0

  # if there are no values that make it work, return to the previous recursive call
  # if this is the first call, the board cannot be solved
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




# Decides which type of board -- custom or random -- to create based on user input in the GUI
def user_input(mode, ipt):
  # custom - translate user input into a board
  if mode == 'c':
    board = []
    for i in range(9):
      row = [int(ipt[j]) for j in range(9*i, 9*(i+1))]
      board.append(row)

    return board
  # random - generate a proper sudoku board
  elif mode == 'r':
    global gameboard
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

    generate()
    levels = {
      'easy': 30,
      'medium': 40,
      'hard': 50,
      'expert': 55
    }
    deleteCells(levels[ipt])

    return gameboard
