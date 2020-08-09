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

  # initialize UI and draw the board
  def __initUI(self):
    self.parent.title('Sudoko Solver')
    self.pack(fill=BOTH, expand=1)
    # canvas for the board to be drawn
    self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
    self.canvas.pack(fill=BOTH, side=TOP)
    self.__draw_board(self.board)

  # redraw the board after the value of a cell changes
  def redraw(self, board, row, col, iterations=0, time=0):
    # time and iterations
    self.parent.title('Time: %fs\tIterations: %d' % (time, iterations))
    # reset canvas
    self.canvas.delete('all')
    # redraw the board
    self.__draw_board(board, row, col)

  # draw the board
  def __draw_board(self, board, row=-1, col=-1):
    self.__draw_cells(row, col)
    self.__draw_grid()
    self.__draw_values(board)

  # draw the grid
  def __draw_grid(self):
    # 10 lines
    for i in range(10):
      # black for main lines that separate board into 3x3, gray for other sublines
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

  # draw the cells
  def __draw_cells(self, row=-1, col=-1):
    # column
    for i in range(9):
      # row
      for j in range(9):
        x0 = MARGIN + i * SIDE
        y0 = MARGIN + j * SIDE
        x1 = MARGIN + (i+1) * SIDE
        y1 = MARGIN + (j+1) * SIDE
        if col != i or row != j:
          # all other cells
          self.canvas.create_rectangle(x0, y0, x1, y1, outline='gray')
        else:
          # current cell
          self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', width=3)

  # draw the values in the cells
  def __draw_values(self, board):
    # delete the values the solver generated
    self.canvas.delete('numbers')
    # row
    for i in range(9):
      # column
      for j in range(9):
        # center of cell
        x = MARGIN + j * SIDE + SIDE / 2
        y = MARGIN + i * SIDE + SIDE / 2
        # temporary variable for current coordinates
        tmp = [i, j]
        # if current coordinates is  part of the clues (the given values at the beginning), color of values of clues is black
        if not tmp in self.clues:
          # if current cell's value is not empty (0), color of the values are gray
          if board[i][j] != 0:
            self.canvas.create_text(x, y, text=board[i][j], tags='numbers', fill='gray')
        else:
          self.canvas.create_text(x, y, text=board[i][j], tags='clues', fill='black')
