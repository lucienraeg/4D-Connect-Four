import numpy as np
import tkinter as tk
import random

random.seed(12345)

# referencing the board: Board.board[dim4, dim3, dim2, dim1]

class Board:

	def __init__(self, dim4_size, dim3_size, dim2_size, dim1_size):
		self.dim_size = [0, dim1_size, dim2_size, dim3_size, dim4_size]
		self.cell_size = 32
		self.board = np.array([[[[0]*dim1_size]*dim2_size]*dim3_size]*dim4_size)

		self.dim_sel = [0, 0, 0, 0, 0]

	def coord(self, x, dim):
		x_coord = max(0, min(self.dim_size[dim]-1, x // self.cell_size))
		return (x)

	def placePiece(self, piece, d1):
		d4 = self.dim_size[4]-1
		d3 = self.dim_size[3]-1
		d2 = self.dim_size[2]-1
		d1 = d1-1

		# gravity
		while self.board[d4-1, d3, d2, d1] == 0 and d4 > 0:
			d4 -= 1
		while self.board[d4, d3-1, d2, d1] == 0 and d3 > 0:
			d3 -= 1
		while self.board[d4, d3, d2-1, d1] == 0 and d2 > 0:
			d2 -= 1

		print("{}({},{},{},{})".format(piece, d1+1, d2+1, d3+1, d4+1))
		self.board[d4, d3, d2, d1] = piece


class Application(tk.Tk):

	def __init__(self, Board):
		tk.Tk.__init__(self)
		self.title("4D Connect Four")
		self.geometry("480x360")

		# fonts
		self.FNT_SMALL = ("Segoe", 10)
		self.FNT_SMALL_BOLD = ("Segoe UI", 10, "bold")

		self.initBoardFrame()

	def initBoardFrame(self):
		self.boardCanvasWidth = Board.cell_size*Board.dim_size[1]
		self.boardCanvasHeight = Board.cell_size*Board.dim_size[2]

		self.boardFrame = tk.Frame(self)

		self.boardLabel = tk.Label(self.boardFrame, text="Board {},{}".format(Board.dim_sel[4], Board.dim_sel[3]), font=self.FNT_SMALL_BOLD)
		self.boardLabel.pack()

		self.boardCanvas = tk.Canvas(self.boardFrame, width=self.boardCanvasWidth, height=self.boardCanvasHeight, bg="red")
		self.boardCanvas.pack()

		self.boardFrame.grid(column=0, row=0)
		


Board = Board(1, 1, 4, 5) # d4, d3, d2, d1
Application = Application(Board)
Application.mainloop()