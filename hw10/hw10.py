# hw10.py
# Zekun Lyu + zlyu + R

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass

# define a new game class
class playSameGame(EventBasedAnimationClass):
	def __init__(self, rows, cols, numColors):
		# constructor will initialize rows, cols and number of colors
		(self.rows, self.cols) = (rows, cols)
		self.numColors = numColors
		cellSize = 30
		margin = 50
		(self.cellSize, self.margin) = (cellSize, margin)
		(canvasWid, canvasHei) = (2*margin + cols*cellSize, 
									2*margin + rows*cellSize)
		super(playSameGame, self).__init__(canvasWid, canvasHei)
		(self.canvasWid, self.canvasHei) = (canvasWid, canvasHei)

	def onKeyPressed(self, event):
		# act to key pressing event
		if event.char == 'r': self.initAnimation()

	def isValid(self, row, col):
		# take in position (row, col) of cell, check if it is a valid cell
		# a valid cell should be in the board and is not empty
		(rows, cols) = (self.rows, self.cols)
		if row<0 or row>=rows or col<0 or col>=cols:
			return False
		if self.board[row][col]==0:
			return False
		return True

	def checkGameOver(self):
		# check if the game is over now
		(rows, cols) = (self.rows, self.cols)
		board = self.board
		# loop over each cell in the game board
		# if a cell has the same color with its adjacent cell
		# return False, if all the cell have no neighbour in same color
		# return True
		for row in xrange(rows):
			for col in xrange(cols):
				if self.isValid(row+1,col) and \
				board[row][col]==board[row+1][col]: return False
				if self.isValid(row-1,col) and \
				board[row][col]==board[row-1][col]: return False
				if self.isValid(row,col+1) and \
				board[row][col]==board[row][col+1]: return False
				if self.isValid(row,col-1) and \
				board[row][col]==board[row][col-1]: return False
		return True



	def onTimerFired(self):
		# act to timer fired event
		# if the game is over, set self.gameOver to be True
		# clear highlight set and update highest score if necessary
		if self.checkGameOver(): 
			self.gameOver = True
			self.highlight = set()
			if self.score>self.highestScore or self.highestScore==None:
				self.writeFile()
		# if game is not over
		if not self.gameOver and self.start:
			# if timer is 0, deduct 20 points and reset timer to 5
			if self.timer == 0:
				self.score = max(0,self.score-20)
				self.timer = 23
			# if not, self.timer minus 1
			else:
				self.timer -= 1

	def findConnection(self, row, col, color):
		# take in position of a neighbour cell and the 
		# color of the current cell, add all the connected cells 
		# into self.highlight set 
		board = self.board
		(rows, cols) = (self.rows, self.cols)
		# if we reach out of boundary, return back
		if row>=rows or row<0 or col>=cols or col<0: return
		# if the neighbour cell have the same color with current cell
		# and its position is not in the highlight set
		# add it to highlight set and go on to check its neighbour
		if board[row][col]==color and not (row,col) in self.highlight:
			self.highlight.add((row,col))
			self.findConnection(row+1, col, color)
			self.findConnection(row-1, col, color)
			self.findConnection(row, col-1, color)
			self.findConnection(row, col+1, color)

	def killSameCell(self):
		# this function will remove the circle in the highlight position
		# that is to say, fill all the position in the current position set
		# with empty signal 0
		n = len(self.highlight)
		if (n>1):
			for cell in self.highlight:
				self.board[cell[0]][cell[1]] = 0
			self.score += n*n

	def cascadeToBottom(self):
		# fill top cells into the bottom empty place
		(rows, cols) = (self.rows, self.cols)
		# create a newBoard to store the board after cascade
		newBoard = [([0] * cols) for row in xrange(rows)]
		# check each column from bottom up
		for col in xrange(cols):
			# index is the row of the cell to be fill in the new bottom
			index = rows-1
			for row in xrange(rows-1,-1,-1):
				# fill the newboard with non-empty elements of oldBoard
				if self.board[row][col]!=0:
					newBoard[index][col] = self.board[row][col]
					index -= 1
		# update self.board
		self.board = newBoard

	def isEmptyCol(self, col):
		# this function take a col and check if this column is empty
		# if it is empty, return True, if not,return False
		(rows, cols) = (self.rows, self.cols)
		board = self.board
		for row in xrange(rows):
			if board[row][col]!=0:
				return False
		return True



	def cascadeToLeft(self):
		(rows, cols) = (self.rows, self.cols)
		# create a newBoard to store the board after cascade
		newBoard = [([0] * cols) for row in xrange(rows)]
		# colIndex is the index of column of newBoard that
		# will be filled
		colIndex = 0
		for col in xrange(cols):
			# check each column from left to right
			# if a certain colmn is not empty
			# assign it to the colIndex column of new Board
			if not self.isEmptyCol(col):
				for row in xrange(rows):
					newBoard[row][colIndex] = self.board[row][col]
				colIndex += 1
		# update self.board
		self.board = newBoard



	def onMousePressed(self, event):
		# act to mouse pressing event
		# if the mouse click in board, game is begining
		(x, y) = (event.x, event.y)
		(margin, cellSize) = (self.margin, self.cellSize)
		(rows, cols) =(self.rows, self.cols)
		(col, row) = ((x-margin)/cellSize, (y-margin)/cellSize)
		if row<rows and row>=0 and col<cols and col>=0:
			self.start = True
		# if the game is not over, kill all the connected cells
		# and do cascade
		if not self.gameOver:
			self.killSameCell()
			self.highlight = set()
			self.cascadeToBottom()
			self.cascadeToLeft()
			self.highlightRegion()
			self.timer = 23

	def highlightRegion(self):
		# this function find all the connected cell of the current cell

		# firstly clear the highlight set
		self.highlight = set()
		# then find the current cell
		(x, y) = (self.x, self.y)
		(rows, cols) = (self.rows, self.cols)
		(margin, cellSize) = (self.margin, self.cellSize)
		board = self.board
		(row, col) = ((y-margin)/cellSize, (x-margin)/cellSize)
		# if cell is in the valid place
		# find connectted cells
		if (row<rows and row>=0 and col<cols and col>=0 and\
			board[row][col]!=0):
			self.findConnection(row, col, board[row][col])


	def mouseMotion(self, event):
		# react mouse motion event
		if not self.gameOver:
			(self.x, self.y) = (event.x, event.y)
			self.highlightRegion()


	def drawCell(self, row, col):
		# draw a cell based on the given position
		(margin, cellSize) = (self.margin ,self.cellSize)
		board = self.board
		canvas = self.canvas
		if board[row][col]!=0:
			color = board[row][col]
			r = cellSize/3 if (row, col) in self.highlight else cellSize/2
			(cx, cy) = (margin+(col+0.5)*cellSize, margin+(row+0.5)*cellSize)
			canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)


	def drawBoard(self):
		# draw the game board
		(rows, cols) = (self.rows, self.cols)
		for row in xrange(rows):
			for col in xrange(cols):
				self.drawCell(row, col)

	def drawTitle(self):
		# draw the game title
		(titleX, titleY) = (self.canvasWid/2, self.margin/2)
		title = "playSameGame"
		self.canvas.create_text(titleX, titleY, 
								text=title, font='Times 20 bold')

	def drawScore(self):
		# display score
		(left, top) = (self.margin, self.canvasHei-self.margin+10)
		(wid, hei) = (80,30)
		self.canvas.create_rectangle(left, top, left+wid, top+hei,
										fill='Medium Orchid')
		(cx, cy) = (left+wid/2, top+hei/2)
		text = "score: %d" % self.score
		self.canvas.create_text(cx, cy, text=text)

	def drawTimer(self):
		# display timer
		margin = self.margin
		(wid, hei) = (80,30)
		(left, top) = (self.canvasWid-margin-wid, self.canvasHei-margin+10)
		self.canvas.create_rectangle(left, top, left+wid, top+hei,
										fill='Medium Orchid')
		(cx, cy) = (left+wid/2, top+hei/2)
		text = "time: %d" % (self.timer/4)
		self.canvas.create_text(cx, cy, text=text)

	def drawHighScore(self):
		# display high score
		(x, y) = (self.canvasWid/2, self.canvasHei-self.margin/2)
		score = self.highestScore
		if score==None:
			score = 0
		text = 'High Score: %d' % score
		self.canvas.create_text(x, y, text=text)


	def drawGame(self):
		# draw game information
		self.drawBoard()
		self.drawTitle()
		self.drawScore()
		self.drawTimer()
		self.drawHighScore()

	def drawGameOver(self):
		# draw game over spec
		(x, y) = (self.canvasWid/2, self.canvasHei/2)
		self.canvas.create_text(x, y, text='GAME END!', 
								fill='red', font='arial 40 bold')


	def redrawAll(self):
		self.canvas.delete(ALL)
		self.drawGame()
		if self.gameOver:
			self.drawGameOver()


	def generateColor(self):
		# randomly generate a color
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		return "#%02x%02x%02x" % (r, g, b)


	def loadBoard(self):
		# load board
		self.colors = []
		(rows, cols) = (self.rows, self.cols)
		self.board = [([0] * cols) for row in xrange(rows)]
		for x in xrange(self.numColors):
			color = self.generateColor()
			self.colors.append(color)

		for row in xrange(self.rows):
			for col in xrange(self.cols):
				index = random.randint(0,self.numColors-1)
				self.board[row][col] = self.colors[index]

	def readFile(self):
		# read high score from the file
		# if there is a file, open it and read the highest score
		try:
			with open("sameGameHighScore.txt","rt") as fin:
				return int(fin.read())
		# if there is no file, return None
		except:
			return None

	def writeFile(self):
		# write the highest score to file
		with open("sameGameHighScore.txt","wt") as fout:
			fout.write(str(self.score))
		


	def initAnimation(self):
		# initialize animation
		self.root.bind("<Motion>", self.mouseMotion)
		self.loadBoard()
		self.gameOver = False
		self.highlight = set()
		(self.x, self.y) = (0, 0)
		self.highestScore = self.readFile()
		self.score = 0
		self.timer = 23
		self.start = False

playSameGame(10, 15, 4).run()

def loadBoard1():
	board=[
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue', 'blue' , 'blue','blue','blue'],
			[ 0,'red', 'red','red', 'red','red','red'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue',  'red', 'blue', 'red', 'blue','green'],
			[ 0,'yellow', 'yellow','yellow','yellow','yellow', 'orange']
		]
	return board

def loadBoard2():
	board=[
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'red', 'red','red', 'red','red','red', 0],
			[ 'blue', 'blue','blue', 'blue','blue','blue', 0],
			[ 'blue',  'red', 'blue', 'red', 'blue','green', 0],
			[ 'yellow', 'yellow','yellow','yellow','yellow', 'orange', 0]
		]
	return board

def loadBoard3():
	board=[[0,0],[1,0]]
	return board

def loadBoard4():
	board=[
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue', 0 , 'blue','blue','blue'],
			[ 0,'red', 'red','red', 'red','red','red'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue',  'red', 'blue', 'red', 'blue','green'],
			[ 0,'yellow', 'yellow','yellow','yellow','yellow', 'orange']
		]
	return board

def loadBoard5():
	board=[
			[ 0,'blue', 'blue',0, 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue', 'blue', 'blue' , 'blue','blue','blue'],
			[ 0,'red', 'red','red', 'red','red','red'],
			[ 0,'blue', 'blue','blue', 'blue','blue','blue'],
			[ 0,'blue',  'red', 'blue', 'red', 'blue','green'],
			[ 0,'yellow', 'yellow','yellow','yellow','yellow', 'orange']
		]
	return board

def testCheckGameOver(game):
	print "Testing checkGameOver()...",
	game.board = loadBoard1()
	assert(game.checkGameOver()==False)
	game = playSameGame(2,2,1)
	game.board = loadBoard3()
	assert(game.checkGameOver()==True)
	print "Passed!"

def testCheckCascadeToLeft(game):
	print "Testing cascadeToLeft...",
	game.board = loadBoard1()
	game.cascadeToLeft()
	assert(game.board==loadBoard2())
	print "Passed"

def testCheckCascadeToBottom(game):
	print "Testing cascadeToBottom...",
	game.board = loadBoard4()
	game.cascadeToBottom()
	assert(game.board==loadBoard5())
	print "Passed"

def testPlaySameGame():
	game = playSameGame(9, 7, 5)
	testCheckGameOver(game)
	testCheckCascadeToLeft(game)
	testCheckCascadeToBottom(game)

if __name__ == "__main__":
	testPlaySameGame()



