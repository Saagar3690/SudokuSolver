import random
import time
from itertools import product

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
  found, row, col = find_empty(gameboard, 0, 9, 1)

  # No empty cells indicates board is full - base case
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




# check if the board is solvable
def solveable(board, count=0):
  # Find the first empty cell - left to right first, then up to down
  found, row, col = find_empty(board, 0, 9, 1)

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



# Algorithm X - fastest for solving board
# @credits: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html for the algorithm
def solve_Algorithm_X(board, window, tk):
  R, C = 3, 3
  N = R*C
  X = ([('rc', rc) for rc in product(range(N), range(N))] +
    [('rn', rn) for rn in product(range(N), range(1, N+1))] +
    [('cn', cn) for cn in product(range(N), range(1, N+1))] +
    [('bn', bn) for bn in product(range(N), range(1, N+1))])
  Y = dict()

  for r, c, n in product(range(N), range(N), range(1, N+1)):
    b = (r//R) * R + (c//C)
    Y[(r, c, n)] = [
      ('rc', (r, c)),
      ('rn', (r, n)),
      ('cn', (c, n)),
      ('bn', (b, n))
    ]

  X, Y = exact_cover(X, Y)

  for i, row in enumerate(board):
    for j, n in enumerate(row):
      if n:
        select(X, Y, (i, j, n))

  for solution in solveX(X, Y, []):
    for (r, c, n) in solution:
      window.redraw(board, r, c)
      tk.update()
      board[r][c] = n
      yield board



# helper method for Algorithm X
# @credits: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html for the algorithm
def exact_cover(X, Y):
  X = {j: set() for j in X}

  for i, row in Y.items():
    for j in row:
      global iterations
      iterations += 1
      X[j].add(i)

  return X, Y




# helper method for Algorithm X
# @credits: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html for the algorithm
def solveX(X, Y, solution):
  if not X:
    yield list(solution)
  else:
    c = min(X, key=lambda c: len(X[c]))
    for r in list(X[c]):
      solution.append(r)
      cols = select(X, Y, r)
      for s in solveX(X, Y, solution):
        global iterations
        iterations += 1
        yield s
      deselect(X, Y, r, cols)
      solution.pop()




# helper method for Algorithm X
# @credits: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html for the algorithm
def select(X, Y, r):
  cols = []

  for j in Y[r]:
    for i in X[j]:
      for k in Y[i]:
        global iterations
        iterations += 1
        if k != j:
          X[k].remove(i)
    cols.append(X.pop(j))

  return cols




# helper method for Algorithm X
# @credits: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html for the algorithm
def deselect(X, Y, r, cols):
  for j in reversed(Y[r]):
    X[j] = cols.pop()
    for i in X[j]:
      for k in Y[i]:
        global iterations
        iterations += 1
        if k !=j :
          X[k].add(i)




# Backtracking Algorithm
# default: traverse left to right, top to bottom and slowest at solving board (better when more clues at the top of the board initially)
# reverse: traverse right to left, bottom to top and slowest at solving board (better when more clues at the bottom of the board initially)
# optimized: traverse based on the cell with least number of possibilities (minimizes branching factor) and 2nd fastest for solving board
def solve(board, window, tk, start, reverse=False, optimized=False):
  # Find the first empty cell - left to right first, then up to down
  if optimized:
    found, row, col = find_empty_optimized(board)
  else:
    if reverse:
      found, row, col = find_empty(board, 8, -1, -1)
    else:
      found, row, col = find_empty(board, 0, 9, 1)

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
      if solve(board, window, tk, start, reverse, optimized):
        return True
      # if previous subset solution doesn't work, reset the value at location in board
      board[row][col] = 0

  # if there are no values that make it work, return to the previous recursive call
  # if this is the first call, the board cannot be solved
  return False




# Finds first empty cell in board with the least number of possibilities
# least number of possibilities is defined as the cell with lowest number of have-not-chosen numbers that are viable in the row, column, and 3x3 block
def find_empty_optimized(board):
  # location variables for the cell with least number of possibilities
  rowOfMin, colOfMin = -1, -1
  # counter of least number of possibilities
  minCount = 10
  # traverse through entire grid
  for row in range(9):
    for col in range(9):
      # if current cell is empty
      if board[row][col] == 0:
        # counter for number of possibilities
        count = 0
        # try all numbers
        for i in range(1, 10):
          # check if number is valid in row, column, and 3x3 block
          if checkRow(board, i, row) and checkCol(board, i, col) and checkBox(board, i, row, col):
            # increment if it is a valid number
            count += 1
        # check if the number of possibilities for current cell is lower than the previous cell with lowest number of possibilities
        if count < minCount:
          # if so, update variables respectively
          minCount = count
          rowOfMin = row
          colOfMin = col

  # if default values, there are no empty cells, so return False, else return True and location of empty cell with least number of possibilities
  if rowOfMin == -1 and colOfMin == -1:
    return False, -1, -1
  else:
    return True, rowOfMin, colOfMin




# Finds first empty cell in board
def find_empty(board, start, end, increment):
  # traverse through entire grid
  for row in range(start, end, increment):
    for col in range(start, end, increment):
      # if current cell is empty, return location of current cell
      if board[row][col] == 0:
        return True, row, col

  return False, -1, -1




# Checks if the value already exists in the row
def checkRow(board, i, row):
  # traverse through row and check if the number exists already
  for col in range(9):
    if board[row][col] == i:
      return False

  return True




# Checks if the value already exists in the column
def checkCol(board, i, col):
  # traverse through column and check if the number exists already
  for row in range(9):
    if board[row][col] == i:
      return False

  return True




# Checks if the value already exists in the 3x3 box
def checkBox(board, i, row, col):
  row_start = row - row % 3
  col_start = col - col % 3

  # traverse through 3x3 block and check if the number exists already
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
