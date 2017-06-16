import numpy as np

#  init board
universes = 7
layers = 7
rows = 7
columns = 7
board = np.array([[[['-']*columns]*layers]*rows]*columns)

def main():
	for _ in range(20):
		offerPlacement('X')
		print(isWinner('X'))
		offerPlacement('O')
		print(isWinner('O'))

# display a layer (2D array)
def displayLayer(u, l):
	print('[  U-{} L-{}  ]'.format(u, l))
	for r in range(rows-1,-1,-1):
		displayedRow = ''
		for c in range(columns):
			displayedRow += (str(board[u][l][r][c]) + ' ')
		print(displayedRow)

# placement
def placePiece(c, piece, displayDetails=True, displayEffectedLayer=True):
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

	# place the piece on the actual board
	board[pU][pL][pR][c] = piece

	# extra info to print
	if displayDetails:
		print('[{}] Placed at Column: {}, Landed at: ({},{},{},{})'.format(piece, c, pU, pL, pR, c))
	if displayEffectedLayer:
		displayLayer(pU,pL)

def offerPlacement(piece):
	while True:
		try:
			placement = min(input('Place [{}] in column: '.format(piece)),columns)
			placePiece(placement,piece)
			break
		except NameError:
			print('Please enter a column (0-{})'.format(columns-1))

def checkForRow(piece, uDif, lDif, rDif, cDif):
	for u in range(universes):
		for l in range(layers):
			for r in range(rows):
				for c in range(columns):
					# yeah i know this looks disgusting but it works so hey
					if board[u+uDif*0][l+lDif*0][r+rDif*0][c+cDif*0] == piece and board[u+uDif*1][l+lDif*1][r+rDif*1][c+cDif*1] == piece and board[u+uDif*2][l+lDif*2][r+rDif*2][c+cDif*2] == piece and board[u+uDif*3][l+lDif*3][r+rDif*3][c+cDif*3] == piece:
						return True


def isWinner(piece):
	# types of relations:
	''' 
	+...  .+..  ..+.  ...+ 					(simple rows) (1D)
	++..  .++.  ..++  +..+  +.+.  .+.+ 		(single diagonals) (2D)
	+++.  ++.+  +.++  .+++					(double diagonals) (3D)
	++++ 									(triple diagonals) (4D)

	+ is up 1 each step
	. same each step
	'''

	# simple rows
	if checkForRow(piece, 1, 0, 0, 0): return True
	if checkForRow(piece, 0, 1, 0, 1): return True
	if checkForRow(piece, 0, 0, 1, 0): return True
	if checkForRow(piece, 0, 0, 0, 1): return True

	# simple diagonal
	if checkForRow(piece, 1, 1, 0, 0): return True
	if checkForRow(piece, 0, 1, 1, 0): return True
	if checkForRow(piece, 0, 0, 1, 1): return True
	if checkForRow(piece, 1, 0, 0, 1): return True
	if checkForRow(piece, 1, 0, 1, 0): return True
	if checkForRow(piece, 0, 1, 0, 1): return True

	# double diagonals 
	if checkForRow(piece, 1, 1, 1, 0): return True
	if checkForRow(piece, 1, 1, 0, 1): return True
	if checkForRow(piece, 1, 0, 1, 1): return True
	if checkForRow(piece, 0, 1, 1, 1): return True

	# triple diagonals
	if checkForRow(piece, 1, 1, 1, 1): return True


if __name__ == '__main__':
	main()