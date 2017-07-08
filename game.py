import numpy as np
import tkinter as tk
import random
import time

random.seed(12345)

# referencing the board: Board.board[dim4, dim3, dim2, dim1]

class Board:

	def __init__(self, dim4_size, dim3_size, dim2_size, dim1_size):
		self.dim_size = [0, dim1_size, dim2_size, dim3_size, dim4_size]
		self.cell_size = 32
		self.board = np.array([[[[0]*dim1_size]*dim2_size]*dim3_size]*dim4_size)

		self.dim_sel = [0, 0, 0, 0, 0]
		self.turnNum = 1

	def coord(self, x, dim):
		x_coord = max(0, min(self.dim_size[dim]-1, x // self.cell_size))
		return (x)

	def randomizeBoard(self):
		for d4 in range(self.dim_size[4]):
			for d3 in range(self.dim_size[3]):
				for d2 in range(self.dim_size[2]):
					for d1 in range(self.dim_size[1]):
						# self.board[d4, d3, d2, d1] = random.randint(0,2)
						if self.board[d4, d3, d2, d1] == 0 and random.randint(0,40) == 0:
							self.placePiece(random.randint(1,2), d1)

		Board.shiftSel(0, 0)

	def toName(self, piece):
		if piece == 1:
			return "W"
		if piece == 2:
			return "B"

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

		self.board[d4, d3, d2, d1] = piece

		msg = "{}({},{},{},{}) [{}]".format(self.toName(piece), d1+1, d2+1, d3+1, d4+1, self.turnNum)
		print(msg)
		Application.turnsText.insert("end", msg +"\n")
		Application.turnsText.see("end")

		self.turnNum += 1

	def shiftSel(self, d4, d3):
		self.dim_sel[4] += d4
		self.dim_sel[3] += d3
		Application.refreshBoardFrame()

	def shiftSoftSel(self, d2, d1):
		self.dim_sel[2] = d2
		self.dim_sel[1] = d1
		Application.coordsLabel['text'] = "Coords: {},{},{},{}".format(self.dim_sel[1]+1, self.dim_sel[2]+1, self.dim_sel[3]+1, self.dim_sel[4]+1)

class Application(tk.Tk):

	def __init__(self, Board):
		tk.Tk.__init__(self)
		self.title("4D Connect Four")

		self.initBoardFrame()
		self.initStatusBar()
		self.initTurns()

	def initBoardFrame(self):
		self.boardCanvasWidth = Board.cell_size*Board.dim_size[1]+4
		self.boardCanvasHeight = Board.cell_size*Board.dim_size[2]+4

		self.boardFrame = tk.Frame(self)

		self.boardCanvas = tk.Canvas(self.boardFrame, width=self.boardCanvasWidth, height=self.boardCanvasHeight, bg="tan4")
		self.boardCanvas.bind("<Motion>", self.updateSoftCoords)
		self.drawBoardSlice(Board.dim_sel[4], Board.dim_sel[3], self.boardCanvas)
		self.boardCanvas.pack()

		self.boardNavigation = tk.Frame(self.boardFrame, width=self.boardCanvasWidth, height=48)
		self.drawBoardNavigation(self.boardNavigation)
		self.boardNavigation.pack()

		self.boardFrame.grid(column=0, row=0, sticky="w")

	def drawBoardSlice(self, d4, d3, frame):
		for d2 in range(Board.dim_size[2]):
			for d1 in range(Board.dim_size[1]):

				# fill color
				if d1 == Board.dim_size[1]:
					fill = "tan2"
				else:
					fill = "tan3"

				# draw tile
				x = d1*Board.cell_size
				y = (Board.dim_size[2]-1-d2)*Board.cell_size

				tileCoords = (x+6, y+6, x+34, y+34)
				frame.create_rectangle(tileCoords, fill=fill, outline="black", width=2)

				# draw piece (if there is one)
				pieceCoords = (x+10, y+10, x+29, y+29)
				if Board.board[d4, d3, d2, d1] == 1:
					self.boardCanvas.create_oval(pieceCoords, width=2, fill="white")
				if Board.board[d4, d3, d2, d1] == 2:
					self.boardCanvas.create_oval(pieceCoords, width=2, fill="black")

	def drawBoardNavigation(self, frame):
		# dim 3
		dim3Down_state = "disabled"
		dim3Up_state = "disabled"

		if Board.dim_sel[3] > 0: dim3Down_state = "normal"
		if Board.dim_sel[3] < Board.dim_size[3]-1: dim3Up_state = "normal"

		dim3Down = tk.Button(frame, state=dim3Down_state, text=" < ", bg="tan3", fg="white", activebackground="tan2", activeforeground="white", command = lambda: Board.shiftSel(0, -1))
		dim3Down.grid(column=0, row=0)
		dim3= tk.Label(frame, text="{} / {}".format(Board.dim_sel[3]+1, Board.dim_size[3]), padx=6)
		dim3.grid(column=1, row=0)
		dim3Up = tk.Button(frame, state=dim3Up_state, text=" > ", bg="tan3", fg="white", activebackground="tan2", activeforeground="white", command = lambda: Board.shiftSel(0, 1))
		dim3Up.grid(column=2, row=0)

		# divider
		divider = tk.Label(frame, text="      ")
		divider.grid(column=3, row=0)

		# dim 4
		dim4Down_state = "disabled"
		dim4Up_state = "disabled"

		if Board.dim_sel[4] > 0: dim4Down_state = "normal"
		if Board.dim_sel[4] < Board.dim_size[4]-1: dim4Up_state = "normal"

		dim4Down = tk.Button(frame, state=dim4Down_state, text=" < ", bg="tan3", fg="white", activebackground="tan2", activeforeground="white", command = lambda: Board.shiftSel(-1, 0))
		dim4Down.grid(column=4, row=0)
		dim4= tk.Label(frame, text="{} / {}".format(Board.dim_sel[4]+1, Board.dim_size[4]), padx=6)
		dim4.grid(column=5, row=0)
		dim4Up = tk.Button(frame, state=dim4Up_state, text=" > ", bg="tan3", fg="white", activebackground="tan2", activeforeground="white", command = lambda: Board.shiftSel(1, 0))
		dim4Up.grid(column=6, row=0)

	def refreshBoardFrame(self):
		self.boardFrame.destroy()
		# self.boardNavigation.destroy()
		self.initBoardFrame()
		self.statusFrame.destroy()
		self.initStatusBar()

	def initStatusBar(self):
		self.statusFrame = tk.Frame(self)
		self.coordsLabel = tk.Label(self.statusFrame, text="Coords: {},{},{},{}".format(Board.dim_sel[1]+1, Board.dim_sel[2]+1, Board.dim_sel[3]+1, Board.dim_sel[4]+1), bd=1, relief="sunken", width=54, anchor="w", bg="#dfdfdf")
		self.coordsLabel.pack(pady=3, padx=3)
		self.statusFrame.grid(column=0, row=1, columnspan=2)

	def initTurns(self):
		self.turnsFrame = tk.Frame()

		self.turnsText = tk.Text(self.turnsFrame, width=17, height=15, background="white")
		self.turnsText.pack()

		# self.turnsScroll = tk.Scrollbar(self.turnsFrame)
		# self.turnsScroll.pack(side="right", fill="y")
		# self.turnsScroll.config(command=self.turnsText.yview)

		self.turnsFrame.grid(column=1, row=0, sticky="w")

	def toCoord(self, x):
		x = max(0,min(Board.dim_size[1]-1, x // Board.cell_size))
		return x

	def updateSoftCoords(self, event):
		d1 = self.toCoord(event.x)
		d2 = self.toCoord(event.y)
		Board.shiftSoftSel(d2, d1)


Board = Board(7, 7, 7, 7) # d4, d3, d2, d1
Application = Application(Board)

Board.randomizeBoard()

Application.mainloop()