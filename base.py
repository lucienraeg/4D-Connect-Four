import numpy as np

#  init board
connectAim = 5
universes = 7
layers = 7
rows = 7
columns = 7
board = np.array([[[['-']*columns]*layers]*rows]*columns)

def main():
	for _ in range(50):
		offerPlacement('X')
		offerPlacement('O')

# display a layer (2D array)
def displayLayer(u, l):
	print('[  U-{} L-{}  ]'.format(u+1, l+1))
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
		print('[{}] Placed at Column: {}, Landed at: ({},{},{},{})'.format(piece, c+1, pU+1, pL+1, pR+1, c+1))
	if displayEffectedLayer:
		displayLayer(pU,pL)


	if isWinner(piece):
		print('{} has won!'.format(piece))

def offerPlacement(piece):
	while True:
		try:
			placement = max(min(input('Place [{}] in column: '.format(piece)),columns)-1,0)
			placePiece(placement,piece)
			break
		except NameError:
			print('Please enter a column (1-{})'.format(columns))

def checkForRow(piece, uDif, lDif, rDif, cDif):
	for u in range(universes):
		for l in range(layers):
			for r in range(rows):
				for c in range(columns):
					# yeah i know this looks disgusting but it works so hey
					try:
						isConnect = 1
						for i in range(connectAim):
							if board[u+uDif*i][l+lDif*i][r+rDif*i][c+cDif*i] != piece:
								isConnect = 0
								
						return isConnect
					except IndexError:
						return None

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