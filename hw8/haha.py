# hw7.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################




######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class Tetris(BasicAnimationClass):
    def __init__(self, rows, cols):
        margin = 5
        cellSize = 30
        canvasWidth = 2*margin + cols*cellSize
        canvasHeight = 2*margin + rows*cellSize
        super(Tetris, self).__init__(canvasWidth, canvasHeight)
        self.margin = margin
        self.cellSize = cellSize
        self.rows = rows
        self.cols = cols

	#def onKeyPressed(self):

	#def onTimerFired(self):
"""
	def drawTetrisBoard(self):
		#draw the tetris board given a 2d list storing
		#color of each cell
		board = self.tetrisBoard
		cols = self.cols
		rows = self.rows
		cellSize = self.cellSize
		outline = 2
		for row in xrange(rows):
			for col in xrange(cols):
				(left, top, right, bottom) = (row*cellSize, col*cellSize,
											(row+1)*cellSize, (col+1*cellSize))
				self.canvas.create_rectangle(left, top, right, botom, 
										fill=board[row][col], outline=outline)

	def redrawAll(self):
		self.canvas.delete(ALL)
		drawTetrisBoard()


	def loadTetrisBoard(self):
		rows = self.rows
		cols = self.cols
		board = []
		for row in range(rows): board +=[['blue'] * cols]
		board[0][0] = 'red'
		board[0][cols-1] = 'white'
		board[rows-1][0] = 'green'
		board[rows-1][cols-1] = 'gray'
		self.tetrisBoard = board

	def initAnimation(self):
		self.loadTetrisBoard()
"""
tetris = Tetris(15, 10)  # play Tetris on a 15x10 board
						 # (must work for any reasonable dimensions)
tetris.run()