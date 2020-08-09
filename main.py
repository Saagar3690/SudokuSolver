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
  # button to generate the board - calls generate function
  genButton = Button(root, text="Generate", command=lambda: generate(e.get()))
  genButton.grid(row=5)
  root.mainloop()

# creates second frame with board
def generate(input):
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
  start_button = Button(top, text="Start", width=10, command=lambda : start(board, window, top))
  start_button.pack()
  # close the second frame and go back to home
  back_button = Button(top, text="Go Back", width=10, command=top.destroy)
  back_button.pack(pady=(0, 10))

# starts the backtracking algorithm
def start(board, window, top):
  # start time
  start = time.time()

  # tracker for when algorithm is finished
  done = False
  while True:
    top.update_idletasks()
    top.update()
    # backtracking algorithm called to solve the board
    game.solve(board, window, top, start)
    # once algorithm finishes, update the time taken and number of iterations
    if not done:
      window.redraw(board, -1, -1, game.iterations, round(time.time() - start, 10))
      done = True

# main
if __name__ == '__main__':
  main()
