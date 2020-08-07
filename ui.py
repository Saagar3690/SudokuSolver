from tkinter import *

MARGIN = 10
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class UI(Frame):
  def __init__(self, parent, board, clues):
    self.parent = parent
    self.board = board
    self.clues = clues
    Frame.__init__(self, parent)
    self.row, self.col = 0, 0
    self.__initUI()

  def __initUI(self):
    self.parent.title('Sudoko Solver')
    self.pack(fill=BOTH, expand=1)
    self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
    self.canvas.pack(fill=BOTH, side=TOP)
    self.__draw_board()

  def redraw(self, board, iterations=0, time=0):
    self.parent.title('Sudoku solved in: %fs\tIterations: %d' % (time, iterations))
    self.__draw_cells(board)

  def __draw_board(self):
    for i in range(10):
      color = "black" if i % 3 == 0 else "gray"

      # Horizontal Lines
      x0 = MARGIN
      y0 = MARGIN + i * SIDE
      x1 = WIDTH - MARGIN
      self.canvas.create_line(x0, y0, x1, y0, fill=color)

      # Vertical Lines
      x0 = MARGIN + i * SIDE
      y0 = MARGIN
      y1 = HEIGHT - MARGIN
      self.canvas.create_line(x0, y0, x0, y1, fill=color)

    self.__draw_cells(self.board)

  def __draw_cells(self, board):
    self.canvas.delete('numbers')
    for i in range(9):
      for j in range(9):
        x = MARGIN + j * SIDE + SIDE / 2
        y = MARGIN + i * SIDE + SIDE / 2
        tmp = [i, j]
        if not tmp in self.clues:
          if board[i][j] != 0:
            self.canvas.create_text(x, y, text=board[i][j], tags='numbers', fill='black')
        else:
          self.canvas.create_text(x, y, text=board[i][j], tags='clues', fill='red')
