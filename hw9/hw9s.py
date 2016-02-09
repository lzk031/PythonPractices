# hw9s.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################

def isLegal(letter, row, col, constraints, rows=5, cols=5):
	# this function take in a letter and the position we
	# wanner fill it in and the constraints to follow,
	# and check if this move is legal

	# if the position is out of bound, return False
	if row>=rows or row<0 or col>=cols or col<0: return False

	# then check if the letter's position follow the constraints
	# if so, return True, otherwise, return False
	constr = constraints.index(letter)
	if constr == 0 or constr == 12:
		if row == col: return True
	if constr == 6 or constr == 18:
		if (row+col) == (rows-1): return True
	(tStart, tEnd) = (1,5)
	if constr in range(tStart,tEnd+1) and constr == (col+1): return True
	(rStart, rEnd) = (7, 11)
	if constr in range(rStart,rEnd+1) and (constr-cols-1) == (row+1): 
		return True
	(bStart, bEnd) = (13, 17)
	if constr in range(bStart, bEnd+1) and (constr-2*(rows+1))+col == cols:
		return True
	(lStart, lEnd) = (19, 23)
	if constr in range(lStart, lEnd+1):
		if (constr-3*(rows+1))+row == rows: return True
	return False


def solveABC(constraints, aLocation, rows=5, cols=5):
	# generate the solution board and use the destructive
	# method solve to solve the puzzle and modify solusion board
	# if the solve function return True, return the modified solution board
	# if not, return None
	solution = [([''] * cols) for row in xrange(rows) ]
	(row, col) = (aLocation[0], aLocation[1])
	solution[row][col] = 'A'
	if solve('A', row, col, constraints, solution):
		return solution
	else:
		return None


def solve(letter, row, col, constraints, solution, \
			visited=set()):
# this function take in the letter and the position it is in
# it also take the constraints and the solution board we wannar modify
# then we fill the next letter into the right position
# after the function is called, the solution will be modified into
# the solustion we want
	directions = [[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]]
	# base case: if the old letter is Y, stop recursion
	if letter=="Y":
		return True
	# recursion: if the letter is not Y, that is to say, the board
	# hasn't been totally filled, we should fill the next letter in 
	# correct position
	else:
		# firstly, find the newletter which is next to current letter
		newLetter = chr(ord(letter)+1)
		# try to fill the new letter into all cells near the current cell
		for direc in directions:
			(newCol, newRow) = (col+direc[0], row+direc[1])

			# if we have put some letter in the new cell
			# continue and go on check other direction
			if (newRow, newCol) in visited: continue
			# if this move is legal, fill the new letter
			# and go on fill other letters by calling solve function
			# recursively
			if isLegal(newLetter, newRow, newCol, constraints):
				# add the new cell into the set visited which include
				# all the cells we have visited
				visited.add((newRow, newCol))
				solution[newRow][newCol] = newLetter
				# if solved, return True
				if solve(newLetter, newRow, newCol, \
							constraints, solution, visited):
					return True

				# if the puzzle is not solved, fill the current
				# cell with empty string and remove current cell from
				# visited set 
				else:
					#solution[newRow][newCol] = ""
					visited.remove((newRow, newCol))

		# if we have try all the directions and get no solution
		# just return False
		return False



######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
import copy
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class Crop(object):
# Crop is an object that have attributes of color, price of seed,
# it's own price, and maturity
	def __init__(self, color, seedPrice, price, mature):
		self.color = color # the color of the crop
		self.seedPrice = seedPrice # price of the seed
		self.price = price # crop price in the market
		self.mature = mature#how long the crop will become mature

	def initialize(self):
		self.isMature = False # if a crop is mature
		self.shade = 1 
		# this stand for crop's color shade which also stand for maturity


	def grow(self):
		# if the crop is not mature, this function will
		# make it grow a little
		if self.shade >= self.mature+1:
			self.isMature = True
		if not self.isMature:
			self.shade += 1;

class CheapCrop(Crop):
	# a cheaper crop which grow faster but at lower price
	def __init__(self):
		color = 'green'
		seedPrice = 1
		price = 10
		mature = 40
		super(CheapCrop, self).__init__(color, seedPrice, price, mature)
		self.initialize()

	def getDrawingData(self):
		# this function get the drawing data of this crop
		self.colorRate = float(self.shade)/(self.mature+1)
		shape = 'square' if not self.isMature else 'circle'
		rate = self.colorRate
		(rStart, gStart, bStart) = (222, 184, 135) #rgb code of empth color
		(red, green, blue) = (0, 255, 0) #rgb code of crop's mature color
		red = rStart+int(rate*(red-rStart))
		green = gStart+int(rate*(green-gStart))
		blue = bStart+int(rate*(blue-bStart))
		color = "#00%02x00" % (self.colorRate*255)
		return (color, shape)


class GoodCrop(Crop):
	# a better crop which grow slower but at higher price
	def __init__(self):
		color = 'yellow'
		seedPrice = 2
		price = 20
		mature = 80
		super(GoodCrop, self).__init__(color, seedPrice, price, mature)
		self.initialize()

	def getDrawingData(self):
		# this function get the drawing data of this crop
		self.colorRate = float(self.shade)/(self.mature+1)
		shape = 'square' if not self.isMature else 'circle'
		rate = self.colorRate
		(rStart, gStart, bStart) = (222, 184, 135) #rgb code of empth color
		(red, green, blue) = (255, 215, 0) #rgb code of crop's mature color
		red = rStart+int(rate*(red-rStart))
		green = gStart+int(rate*(green-gStart))
		blue = bStart+int(rate*(blue-bStart))
		color = "#%02x%02x%02x" % (red,green,blue)
		return (color, shape)

class Farmer(object):
	# Farmer have features of balance, water, goodseeds and cheapseeds
	def __init__(self, balance, water, goodSeeds, cheapSeeds):
		self.balance = balance # amount of money the farmer has
		self.water = water # amount of water the farmer has
		self.goodSeeds = goodSeeds # number of good seeds farmer has
		self.cheapSeeds = cheapSeeds # number of cheap seeds farmer has

	def plantGoodCrop(self, game):
		# plant a good crop in the current cell
		if self.goodSeeds>0:
			(row, col) = game.chosenCell
			if game.board[row][col] == game.emptyColor:
				game.board[row][col] = GoodCrop()
				self.goodSeeds -= 1
				game.spec = "You plant a good crop"
			else: 
				game.spec = "Can't plant here"
		else:
			game.spec = """You don't have a seed for good crop
press 'g' to buy one"""

	def plantCheapCrop(self, game):
		# plant a cheap crop in the current cell
		if self.cheapSeeds>0:
			(row, col) = game.chosenCell
			if game.board[row][col] == game.emptyColor:
				game.board[row][col] = CheapCrop()
				self.cheapSeeds -= 1
				game.spec = "You plant a cheap crop"
			else: 
				game.spec = "Can't plant here"
		else:
			 game.spec = """You don't have a seed for cheap crop
press 'c' to buy one"""

	def buyGoodSeed(self, game):
		# buy a good seed
		seedPrice = 2
		if self.balance >= seedPrice:
			self.goodSeeds += 1
			self.balance -= seedPrice
			game.spec = "You buy a good crop seeds"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def buyCheapSeed(self, game):
		# buy a cheap seed
		seedPrice = 1
		if self.balance>=seedPrice:
			self.cheapSeeds += 1
			self.balance -= seedPrice
			game.spec = "You buy a cheep crop seed"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def buyWater(self, game):
		# buy a water
		waterPrice = 1
		if self.balance>=waterPrice:
			self.water += 1
			self.balance -= waterPrice
			game.spec = "You buy a water"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def harvest(self, game):
		# harvest a crop in the current cell
		board = game.board
		(row, col) = game.chosenCell
		if isinstance(board[row][col], Crop):
			if board[row][col].isMature:
				self.balance += board[row][col].price
				board[row][col] = game.emptyColor
				game.spec = "You havest a crop"
			else: 
				game.spec = "It is not mature"
		else:
			game.spec = "You can't harvest without planting anything"

	def irrigate(self, game):
		# irrigate a crop in the current cell
		board = game.board
		(row, col) = game.chosenCell
		if self.water==0:
			game.spec = """You have no water
press 'w' to buy one"""
		else:
			if isinstance(board[row][col], Crop):
				if not board[row][col].isMature:
					accelarate = 10
					for x in xrange(accelarate):
						game.board[row][col].grow()
					game.spec = "You irrigate a crop, it grows a lot"
				else:
					game.spec = "The crop has already been matrue"
			else:
				game.spec = "No crop to water here"



class FarmGame(BasicAnimationClass):
	# this is a game object which in charge of the whole game
	def __init__(self, rows, cols):
		# initialize size information
		margin = 50
		cellSize = 40
		canvasWidth = 4*margin + 2*cols*cellSize
		canvasHeight = 2*margin + rows*cellSize
		super(FarmGame, self).__init__(canvasWidth, canvasHeight)
		(self.canvasWidth, self.canvasHeight) = (canvasWidth,canvasHeight)
		self.margin = margin
		self.cellSize = cellSize
		self.rows = rows
		self.cols = cols
		self.emptyColor = 'Burlywood'

	def onKeyPressed(self, event):
		# react to the key event
		if (event.char == 'r'): self.initAnimation()
		if (event.char == 'p'): 
			self.isGameStart = True 
			self.isHelpScreen = False
		if (event.char == '?'): 
			self.spec=''
			self.isHelpScreen = True
			self.isGameStart = False
		if self.isGameStart:
			if (event.keysym == '1'): 
				self.farmer.plantGoodCrop(self) 
				# plant a good crop in current cell
			elif (event.keysym == '2'): 
				self.farmer.plantCheapCrop(self) 
				# plant a cheap crop in current cell
			elif (event.keysym == 'g'): self.farmer.buyGoodSeed(self)
			elif (event.keysym == 'c'): self.farmer.buyCheapSeed(self)
			elif (event.keysym == 'w'): self.farmer.buyWater(self)
			elif (event.keysym == 'h'): self.farmer.harvest(self)
			elif (event.keysym == 'i'): 
				# irrigate the crop when pressing 'i'
				self.farmer.irrigate(self)


	def chooseCell(self, x, y):
		# choose a cell given the x and y axis
		x -= self.margin
		y -= self.margin
		col = x/self.cellSize
		row = y/self.cellSize
		(cols, rows) = (self.cols, self.rows)
		if col>=0 and col<cols and row>=0 and row<rows:
			self.chosenCell = (row, col)

	def onMousePressed(self, event):
		# react to mouse pressed event
		if self.isGameStart:
			self.chooseCell(event.x, event.y)

	def growCrops(self):
		# when the time is fired grow all the crops that need to grow
		(cols, rows) = (self.cols, self.rows)
		board = self.board
		for row in xrange(rows):
			for col in xrange(cols):
				if isinstance(board[row][col],Crop):
					board[row][col].grow()

	def onTimerFired(self):
		# react to timer fired event
		self.growCrops()


	def drawBackground(self):
		# draw the back ground
		self.canvas.create_rectangle(0,0,self.canvasWidth,
										self.canvasHeight,fill="black")

	def drawHighlightCell(self):
		# draw the highlight cell
		color = 'pink'
		wid = 5
		(row, col) = self.chosenCell
		(margin, cellSize) = (self.margin, self.cellSize)
		(left, top) = (margin+col*cellSize, margin+row*cellSize)
		self.canvas.create_line(left,top,left+cellSize,top,fill=color,width=wid)
		self.canvas.create_line(left+cellSize,top,left+cellSize,
								top+cellSize,fill=color,width=wid)
		self.canvas.create_line(left+cellSize,top+cellSize,left,
								top+cellSize,fill=color,width=wid)
		self.canvas.create_line(left,top+cellSize,left,top,fill=color,width=wid)

	def drawCell(self, row, col):
		# draw a cell given the row and col
		board = self.board
		(margin, cellSize) = (self.margin, self.cellSize)
		outline = 2
		(left, top) = (margin+col*cellSize, margin+row*cellSize)
		if board[row][col] == self.emptyColor:
			color = self.emptyColor
			self.canvas.create_rectangle(left, top, left+cellSize,
								top+cellSize, fill=color, width=outline)
		elif isinstance(board[row][col],Crop):
			(color, shape) = board[row][col].getDrawingData()
			rate = board[row][col].colorRate
			(left, top) = (left+(1-rate)*cellSize/2, top+(1-rate)*cellSize)
			if shape == 'circle':
				self.canvas.create_oval(left, top, left+cellSize*rate,
								top+cellSize*rate, fill=color)
			else:
				self.canvas.create_rectangle(left, top, left+cellSize*rate,
								top+cellSize*rate, fill=color)



	def drawBoard(self):
		# draw the field board
		board = self.board
		(cols, rows) = (self.cols, self.rows)
		for row in xrange(rows):
			for col in xrange(cols):
				self.drawCell(row, col)
	
	def drawBalance(self):
		# draw teh balance mark
		margin = self.margin
		(textX, textY) = (margin/2, margin/2)
		text = "Balance: %d" % self.farmer.balance
		self.canvas.create_text(textX, textY, anchor=W, text=text, fill='blue')		

	def drawSeeds(self):
		# draw the seeds mark, display number of two kinds of seeds and
		# the water
		margin = self.margin
		(textX, textY) = (self.canvasWidth-margin/2, margin/2)
		text = "goodSeeds: %d cheapSeeds: %d water: %d" % \
							(self.farmer.goodSeeds, self.farmer.cheapSeeds, 
								self.farmer.water)
		self.canvas.create_text(textX, textY, anchor=E, text=text, fill='blue')

	def drawSpec(self):
		# draw the hint during the game
		(textX, textY) = (self.canvasWidth/2, self.canvasHeight/2)
		self.canvas.create_text(textX, textY, text=self.spec, anchor=W, 
								fill='red', font='Times 30 bold')
		linesDistance = 100
		shiftWindowSpec = """       press 'p' to game window    
         press '?' to help window    
         press 'r' to reset  """
		self.canvas.create_text(self.canvasWidth, textY+linesDistance, 
								text=shiftWindowSpec, anchor=E, fill='green',
								font='arial 28')

	def drawInstr(self):
		# draw the instruction during the game
		(left, top, wid, hei) = (self.canvasWidth/2, 50, 400, 250)
		self.canvas.create_rectangle(left, top, left+wid, 
										top+hei, fill='lightblue')
		comments = """
  1. click in a certain cell to choose a cell to edit
  2. press '1' to plant a good crop
  3. press '2' to plant a cheap crop 
  3. press 'g' to buy a good crop seed
  4. press 'c' to buy a cheap crop seed
  5. press 'w' to buy a water
  6. press 'i' to irrigate a crop and 
   	 accelarate it's growth
  7. press 'h' to harvest a crop and sell it 
  Note: square stands for growing and 
	  circle stands for mature crop
"""
		linesDistance = 20
		count = 1
		for line in comments.splitlines():
			self.canvas.create_text(left, top+count*linesDistance, anchor=W, 
                            text=line, font='arial 18')
			count += 1


	def drawGame(self):
		# draw the game window
		self.drawBoard()
		if self.chosenCell!=None:
			self.drawHighlightCell()
		self.drawBalance()
		self.drawSeeds()
		self.drawInstr()

	def drawSplashScreen(self):
		# draw splash screen at the start
		(cx, cy) = (self.canvasWidth/2, self.canvasHeight/2)
		size = min(self.canvasWidth,self.canvasHeight)/4
		self.canvas.create_rectangle(cx-size, cy-size, cx+size, 
								cy+size, fill='Thistle')
		(left, top) = (cx-size, cy-size)
		linesDistance = 30
		comments = """

                         Farm Game

                         Produced by 
                          Zekun Lyu

                 press '?' to help screen
                 press 'p' to start game
"""
		count = 1
		for line in comments.splitlines():
			self.canvas.create_text(left, top+count*linesDistance, anchor=NW, 
                            text=line, fill='black', font='arial 18 bold')
			count += 1

	def drawHelpScreen(self):
		# draw help screen when '?' is pressed
		(cx, top) = (self.canvasWidth/5, 80)
		linesDistance = 30
		self.canvas.create_text(self.canvasWidth/2, top, 
								text="Instruction", font='Times 30 bold')
		comments = """
This is a farm game, you can plant crops in the  2d grid. You have 
two kinds of crops: a good one worth 20 dollars in the market 
but takes longer to grow and a cheaper one worth 10 dollars but grow faster
1. click in a certain cell to choose a cell to edit
2. press '1' to plant a good crop
3. press '2' to plant a cheap crop 
3. press 'g' to buy a good crop seed
4. press 'c' to buy a cheap crop seed
5. press 'w' to buy a water
6. press 'i' to irrigate a crop and accelarate it's growth
7. press 'h' to harvest a crop and sell it 
Note: square stands for growing and circle stands for mature crop
"""
		top += 2*linesDistance
		count = 1
		for line in comments.splitlines():
			self.canvas.create_text(cx, top+count*linesDistance, anchor=W, 
                            text=line, font='Times 18')
			count += 1

	def redrawAll(self):
		self.canvas.delete(ALL)
		if self.isHelpScreen:
			self.drawHelpScreen()
			self.drawSpec()
		elif self.isGameStart:
			self.drawGame()
			self.drawSpec()
		else:
			self.drawSplashScreen()


	def loadBoard(self):
		rows = self.rows
		cols = self.cols
		board = []
		for row in range(rows): 
			board +=[[self.emptyColor] * cols]
			self.board = board


	def initAnimation(self):
		self.loadBoard()
		self.app.setTimerDelay(200) # set timer
		self.isGameStart = False # indicate if the game is start
		self.isHelpScreen = False # indicate if it is in help screen
		self.chosenCell = (0, 0) # the position of the chosen cell
		self.spec = "" # the hint displayed during the game
		self.farmer = Farmer(10, 0, 0, 0)#instantiate a farmer to hold the farm


class HFractal(BasicAnimationClass):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		super(HFractal, self).__init__(self.width, self.height)

	def increaseLevel(self):
		self.level += 1

	def decreaseLevel(self):
		if self.level > 0:
			self.level -= 1


	def onKeyPressed(self, event):
		if (event.keysym == "Up"): self.increaseLevel()
		elif (event.keysym == "Down"): self.decreaseLevel()

	def drawHFractal(self, x, y, wid, hei, level):
		# x, y is represent the center oc the canvas
		# size is the length of the longer side of 
		# the rectangle bordering the h-fractal view
		color = "red"
		canvas = self.canvas
		r = self.ratio
		if level == 0:
			canvas.create_line(x-wid/2, y-hei/2, x-wid/2, y+hei/2, fill=color)
			canvas.create_line(x-wid/2, y, x+wid/2, y, fill=color)
			canvas.create_line(x+wid/2, y-hei/2, x+wid/2, y+hei/2, fill=color)
		else:
			self.drawHFractal(x, y, wid, hei, level-1)
			self.drawHFractal(x-wid/2, y-hei/2, wid/r, hei/r, level-1)
			self.drawHFractal(x-wid/2, y+hei/2, wid/r, hei/r, level-1)
			self.drawHFractal(x+wid/2, y-hei/2, wid/r, hei/r, level-1)
			self.drawHFractal(x+wid/2, y+hei/2, wid/r, hei/r, level-1)


	def redrawAll(self):
		self.canvas.delete(ALL)
		(x, y) = (self.middleX, self.middleY)
		self.drawHFractal(x, y, self.width/2, self.height/2, self.level)

	def initAnimation(self):
		self.level = 0
		self.ratio = 2
		(self.middleX, self.middleY) = (self.width/2, self.height/2)

def playFarmGame():	
	farGame = FarmGame(15, 10)
	farGame.run()

def hFractal():
	hf = HFractal(800, 600)
	hf.run()



def testIsLegal():
	print "Testing isLegal()...",
	constraints = "CHJXBOVLFNURGPEKWTSQDYMI"
	assert(isLegal("C", 2, 2, constraints)==True)
	assert(isLegal("G", 1, 1, constraints)==True)
	assert(isLegal("V", 4, 0, constraints)==True)
	assert(isLegal("S", 3, 1, constraints)==True)
	assert(isLegal("J", 0, 1, constraints)==True)
	assert(isLegal("F", 1, 2, constraints)==True)
	assert(isLegal("W", 4, 1, constraints)==True)
	assert(isLegal("M", 1, 4, constraints)==True)
	assert(isLegal("M", 1, 7, constraints)==False)
	print "Passed!"


def testSolveABC():
	print "Testing solveABC()...",
	constraints = "CHJXBOVLFNURGPEKWTSQDYMI"
	aLocation = (0,4)
	board = solveABC(constraints, aLocation)
	solution = [['I', 'J', 'K', 'L', 'A'],
				['H', 'G', 'F', 'B', 'M'],
				['T', 'Y', 'C', 'E', 'N'],
				['U', 'S', 'X', 'D', 'O'],
				['V', 'W', 'R', 'Q', 'P']
			   ]
	assert(board == solution)
	print "Passed!" 

def testAll():
	testIsLegal()
	testSolveABC()
	playFarmGame()
	hFractal()

if __name__ == "__main__":
	testAll()


