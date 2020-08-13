import time
import game
import ui

from tkinter import *

def main():
  root = Tk()
  root.title('Sudoku Solver')
  # information label
  label = Label(root, text="If you have a custom board, enter your board row by row in one line without spaces. Use 0 for empty spaces (e.g 780400120600075009000601078007040260001050930904060005070300012120007400049206007): \nIf you would like a randomly generated board, type in one of the following levels as shown: easy, medium, hard, or expert")
  label.grid(row=0, padx=10, pady=(10, 0))
  # user input
  e = Entry(root, width=130, borderwidth=5)
  e.grid(row=1)
  # information label
  label2 = Label(root, text="Enter the algorithm you would like to use: Backtracking, Reverse Backtracking, Best First Search, Algorithm X")
  label2.grid(row=2, padx=10, pady=(10, 0))
  # user input
  a = Entry(root, width=130, borderwidth=5)
  a.grid(row=3)
  # button to generate the board - calls generate function
  genButton = Button(root, text="Generate", command=lambda: generate(e.get(), a.get()))
  genButton.grid(row=5)
  root.mainloop()

# creates second frame with board
def generate(input, algorithm):
  # based on input, generate custom or random board of specific level
  if input == 'easy' or input == 'medium' or input == 'hard' or input == 'expert':
    board = game.user_input('r', input)
  else:
    board = game.user_input('c', input)

  # clues (numbers given on board at the start)
  clues = []
  for row in  range(9):
    for col in range(9):
      if board[row][col] != 0:
        clues.append([row, col])

  # create second frame
  top = Toplevel()
  # sudoku ui - the board
  window = ui.UI(top, board, clues)
  # start the solving algorithm
  start_button = Button(top, text="Start", width=10, command=lambda : start(board, window, top, algorithm))
  start_button.pack()
  # close the second frame and go back to home
  back_button = Button(top, text="Go Back", width=10, command=top.destroy)
  back_button.pack(pady=(0, 10))

# starts the backtracking algorithm
def start(board, window, top, algorithm):
  # tracker for when algorithm is finished
  done = False
  while True:
    top.update_idletasks()
    top.update()
    # start time
    start = time.time()
    # reset iterations
    game.iterations = 0
    # call appropriate algorithm based on user input
    if algorithm.lower() == 'reverse backtracking':
      game.solve(board, window, top, start, reverse=True)
    elif algorithm.lower() == 'best first search':
      game.solve(board, window, top, start, optimized=True)
    elif algorithm.lower() ==  'algorithm x':
      for solution in game.solve_Algorithm_X(board, window, top):
        pass
    else:
      game.solve(board, window, top, start)
    # once algorithm finishes, update the time taken and number of iterations
    if not done:
      window.redraw(board, -1, -1, game.iterations, round(time.time() - start, 10), done=True)
      done = True

# main
if __name__ == '__main__':
  main()
