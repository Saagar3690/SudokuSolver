import time
import game
import ui

from tkinter import *

def main():
  board = game.user_input()
  clues = []
  for row in range(9):
    for col in range(9):
      if board[row][col] != 0:
        clues.append([row, col])

  root = Tk()
  window = ui.UI(root, board, clues)
  start = time.time()

  done = False
  while True:
    root.update_idletasks()
    root.update()
    game.solve(board, window, root, start)
    if not done:
      window.redraw(board, game.iterations, round(time.time() - start, 10))
      done = True



if __name__ == '__main__':
  main()
