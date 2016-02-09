# hw7.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################




######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
import copy
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class Tetris(BasicAnimationClass):
	def __init__(self, rows, cols):
		margin = 30
		cellSize = 30
		self.canvasWidth = 2*margin + cols*cellSize
		self.canvasHeight = 2*margin + rows*cellSize
		super(Tetris,self).__init__(self.canvasWidth,self.canvasHeight)
		self.margin = margin
		self.cellSize = cellSize
		self.rows = rows
		self.cols = cols
		self.piece = None
		self.pieceColor = None
		self.fallingPieceRow = None
		self.fallingPieceCol = None

	def fallingPieceIsLegal(self):
		piece = self.piece
		board = self.tetrisBoard
		(pieceRows, pieceCols) = (len(piece),len(piece[0]))
		(rows, cols) = (self.rows, self.cols)
		(startRow, startCol) = (self.fallingPieceRow, self.fallingPieceCol)
		for row in xrange(pieceRows):
			for col in xrange(pieceCols):
				if piece[row][col] == True:
					if startRow + row >= rows: return False
					if startCol + col >= cols: return False
					if startRow + row < 0: return False
					if startCol + col < 0: return False
					emptyColor = 'blue'
					if (board[startRow+row][startCol+col]!=emptyColor):
						return False
		return True

	def moveFallingPiece(self, drow, dcol):
		self.fallingPieceRow += drow
		self.fallingPieceCol += dcol
		if not self.fallingPieceIsLegal():
			self.fallingPieceRow -= drow
			self.fallingPieceCol -= dcol
			return False
		return True
		
	def rotateFallingPiece(self):
		oldPiece = self.piece
		(rows, cols) = (len(oldPiece), len(oldPiece[0]))
		newPiece = []
		for row in range(cols): newPiece +=[[None] * rows]
		for row in xrange(rows):
			for col in xrange(cols):
				newPiece[cols-1-col][row] = oldPiece[row][col]
		self.piece = newPiece
		if not self.fallingPieceIsLegal():
			self.piece = oldPiece

				
	def onKeyPressed(self, event):
		self.ignoreNextTimerEvent = True
		if (event.keysym == "r") : self.initAnimation()
		if (not self.isGameOver):
			if (event.keysym == "Down"): self.moveFallingPiece(+1,0)
			elif (event.keysym == "Left"): self.moveFallingPiece(0,-1)
			elif (event.keysym == "Right"): self.moveFallingPiece(0,+1)
			elif (event.keysym == "Up"): self.rotateFallingPiece()

	def isFullRow(self,row):
		emptyColor = "blue"
		board = self.tetrisBoard
		for col in xrange(self.cols):
			if board[row][col] == emptyColor: return False
		return True


	def removeFullRows(self):
		(board, rows, cols) = (copy.deepcopy(self.tetrisBoard), self.rows, self.cols)
		newBoard = []
		oldRow = rows
		emptyColor = 'blue'
		while(oldRow > 0):
			oldRow -= 1;
			if (self.isFullRow(oldRow) == False):
				newBoard = [board[oldRow]] + newBoard
		fullRows = rows - len(newBoard)
		self.score += fullRows*fullRows
		for x in xrange(fullRows):
			newBoard = [[emptyColor]*cols] + newBoard
		self.tetrisBoard = newBoard


	def placeFallingPiece(self):
		startRow = self.fallingPieceRow;
		startCol = self.fallingPieceCol;
		(piece, pieceColor) = (self.piece, self.pieceColor)
		(rows, cols) = (len(piece),len(piece[0]))
		for row in xrange(rows):
			for col in xrange(cols):
				if (piece[row][col]==True):
					self.tetrisBoard[startRow+row][startCol+col] = pieceColor
		self.removeFullRows()

	def onTimerFired(self):
		'''ignoreThisTimerEvent = self.ignoreNextTimerEvent
		self.ignoreNextTimerEvent = False
		if (ignoreThisTimerEvent == False) and (self.isGameOver==False):'''
		if (self.isGameOver==False):
			if not self.moveFallingPiece(+1,0):
				self.placeFallingPiece()
				self.newFallingPiece()
				if (self.fallingPieceIsLegal() == False):
					self.isGameOver = True

	def initPieces(self):
		#Seven "standard" pieces (tetrominoes)
		iPiece = [[ True,  True,  True,  True]]
		jPiece = [[ True, False, False ],[ True, True,  True]]
  		lPiece = [[ False, False, True],[ True,  True,  True]]
		oPiece = [[ True, True],[ True, True]]
		sPiece = [[ False, True, True],[ True,  True, False ]]
		tPiece = [[ False, True, False ],[ True,  True, True]]
		zPiece = [[ True,  True, False ],[ False, True, True]]
		tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, \
							sPiece, tPiece, zPiece ]
		tetrisPieceColors = [ "red", "yellow", "magenta", \
								"pink", "cyan", "green", "orange" ]
		return (tetrisPieces,tetrisPieceColors)


	def newFallingPiece(self):		
		(tetrisPieces,tetrisPieceColors) = self.initPieces()
		n = random.randint(0,6)
		(self.piece, self.pieceColor) = (tetrisPieces[n], tetrisPieceColors[n])
		self.fallingPieceRow = 0
		middle = self.cols/2  - len(self.piece[0])/2
		self.fallingPieceCol = middle


	def drawCell(self, row, col, color):
		cellSize = self.cellSize
		margin = self.margin
		cellMargin = 2
		(outerLeft, outerTop) = (margin+col*cellSize, margin+row*cellSize)
		(innerLeft, innerTop) = (outerLeft+cellMargin, outerTop+cellMargin)
		self.canvas.create_rectangle(outerLeft, outerTop, outerLeft+cellSize, 
								outerTop+cellSize, fill='black')
		self.canvas.create_rectangle(outerLeft, outerTop, outerLeft+
								cellSize-cellMargin, 
								outerTop+cellSize-cellMargin, fill=color)

	def drawBoard(self):
		#draw the tetris board given a 2d list storing
		#color of each cell
		board = self.tetrisBoard
		cols = self.cols
		rows = self.rows
		margin = self.margin
		cellSize = self.cellSize
		outline = 2
		top = margin
		for row in xrange(rows):
			for col in xrange(cols):
				color = self.tetrisBoard[row][col]
				self.drawCell(row, col, color)

	def drawFallingPiece(self):
		startRow = self.fallingPieceRow;
		startCol = self.fallingPieceCol;
		(piece, pieceColor) = (self.piece, self.pieceColor)
		(rows, cols) = (len(piece),len(piece[0]))
		for row in xrange(rows):
			for col in xrange(cols):
				if (piece[row][col]==True):
					self.drawCell(startRow+row, startCol+col, pieceColor)

	def drawScore(self):
		margin = self.margin
		(textX, textY) = (margin/2, margin/2)
		text = "Score: %d" % self.score
		self.canvas.create_text(textX, textY, anchor=W, text=text, fill='blue')				
	
	def drawSpec(self):
		margin = self.margin
		(textX, textY) = (self.canvasWidth-margin/2, margin/2)
		text = "Press 'r' to restart!"
		self.canvas.create_text(textX, textY, anchor=E, text=text, fill='blue')				


	def drawGame(self):
		self.canvas.create_rectangle(0, 0, self.canvasWidth, 
										self.canvasHeight, fill='orange')
		self.drawBoard()
		self.drawFallingPiece()
		self.drawScore();
		self.drawSpec();


	def drawGameOver(self):
		(cx, cy) = (self.canvasWidth/2, self.canvasHeight/2)
		text = "Game Over!"
		self.canvas.create_text(cx, cy, text=text, 
								fill='red', font='arial 40 bold')

	def redrawAll(self):
		self.canvas.delete(ALL)
		self.drawGame();
		if self.isGameOver:
			self.drawGameOver();


	def loadTetrisBoard(self):
		rows = self.rows
		cols = self.cols
		board = []
		for row in range(rows): board +=[["blue"] * cols]
		'''board[0][0] = "red"
		board[0][cols-1] = "white"
		board[rows-1][0] = "green"
		board[rows-1][cols-1] = "gray"'''
		self.tetrisBoard = board

	def initAnimation(self):
		self.loadTetrisBoard()
		self.newFallingPiece()
		self.app.setTimerDelay(500)
		self.ignoreNextTimerEvent = False
		self.isGameOver = False
		self.score = 0

tetris = Tetris(15, 10)  # play Tetris on a 15x10 board
						 # (must work for any reasonable dimensions)
tetris.run()