import numpy as np
import random

# game settings
universes = 7
layers = 7
rows = 7
columns = 7

board = np.array([[[['-']*columns]*layers]*rows]*columns)

# tiles are referenced like this:
# board[universe, layer, row, column]
# e.g: board[0, 4, 2, 3] is the 1st universe, 5th layer, 3rd row and 4th column

# display a layer (2D array)
def displayLayer(u, l):
	print('[  U-{} L-{}  ]'.format(u, l))
	for r in range(rows-1,-1,-1):
		displayedRow = ''
		for c in range(columns):
			displayedRow += (str(board[u][l][r][c]) + ' ')
		print(displayedRow)

# placement
def placePiece(c, piece, displayDetails=False):
	# default values to go from
	pU = universes-1
	pL = layers-1
	pR = rows-1
	# (c is already decided)

	# get lowest universe, layer and row possibles
	while str(board[pU-1][pL][pR][c]) == '-' and pU > 0:
		pU -= 1
	while str(board[pU][pL-1][pR][c]) == '-' and pL > 0:
		pL -= 1
	while str(board[pU][pL][pR-1][c]) == '-' and pR > 0:
		pR -= 1


	if displayDetails:
		print('[{}] Placed at Column: {}, Landed at: ({},{},{},{})'.format(piece, c, pU, pL, pR, c))
	# place the piece on the actual board
	board[pU][pL][pR][c] = piece


# place 193 tiles in column 1, transending the row, layer and universe
for _ in range(193):
	placePiece(1, 'X')

displayLayer(0,0)
displayLayer(3,6)