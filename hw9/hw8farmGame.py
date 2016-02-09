# hw8.py
# Zekun Lyu + zlyu + R

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
import copy
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class Crop(object):
	def __init__(self, color, seedPrice, price, mature):
		self.color = color
		self.seedPrice = seedPrice
		self.price = price
		self.mature = mature#how long the crop will become mature

	def initialize(self):
		self.isMature = False
		self.shade = 1


	def grow(self):
		if self.shade >= self.mature+1:
			self.isMature = True
		if not self.isMature:
			self.shade += 1;

class CheapCrop(Crop):
	def __init__(self):
		color = 'green'
		seedPrice = 1
		price = 10
		mature = 40
		super(CheapCrop, self).__init__(color, seedPrice, price, mature)
		self.initialize()

	def getDrawingData(self):
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
	def __init__(self):
		color = 'yellow'
		seedPrice = 2
		price = 20
		mature = 80
		super(GoodCrop, self).__init__(color, seedPrice, price, mature)
		self.initialize()

	def getDrawingData(self):
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
	def __init__(self, balance, water, goodSeeds, cheapSeeds):
		self.balance = balance
		self.water = water
		self.goodSeeds = goodSeeds
		self.cheapSeeds = cheapSeeds

	def plantGoodCrop(self, game):
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
		seedPrice = 2
		if self.balance >= seedPrice:
			self.goodSeeds += 1
			self.balance -= seedPrice
			game.spec = "You buy a good crop seeds"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def buyCheapSeed(self, game):
		seedPrice = 1
		if self.balance>=seedPrice:
			self.cheapSeeds += 1
			self.balance -= seedPrice
			game.spec = "You buy a cheep crop seed"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def buyWater(self, game):
		waterPrice = 1
		if self.balance>=waterPrice:
			self.water += 1
			self.balance -= waterPrice
			game.spec = "You buy a water"
		else:
			game.spec = """You don't have enough money
press 'h' to harvest a mature crop"""

	def harvest(self, game):
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
	def __init__(self, rows, cols):
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
				self.farmer.plantGoodCrop(self) # plant a good crop in current cell
			elif (event.keysym == '2'): 
				self.farmer.plantCheapCrop(self) # plant a cheap crop in current cell
			elif (event.keysym == 'g'): self.farmer.buyGoodSeed(self)
			elif (event.keysym == 'c'): self.farmer.buyCheapSeed(self)
			elif (event.keysym == 'w'): self.farmer.buyWater(self)
			elif (event.keysym == 'h'): self.farmer.harvest(self)
			elif (event.keysym == 'i'): 
				# irrigate the crop when pressing 'i'
				self.farmer.irrigate(self)


	def chooseCell(self, x, y):
		x -= self.margin
		y -= self.margin
		col = x/self.cellSize
		row = y/self.cellSize
		(cols, rows) = (self.cols, self.rows)
		if col>=0 and col<cols and row>=0 and row<rows:
			self.chosenCell = (row, col)

	def onMousePressed(self, event):
		self.chooseCell(event.x, event.y)

	def growCrops(self):
		(cols, rows) = (self.cols, self.rows)
		board = self.board
		for row in xrange(rows):
			for col in xrange(cols):
				if isinstance(board[row][col],Crop):
					board[row][col].grow()

	def onTimerFired(self):
		#self.isChosen = not self.isChosen
		self.growCrops()


	def drawBackground(self):
		self.canvas.create_rectangle(0,0,self.canvasWidth,
										self.canvasHeight,fill="black")

	def drawHighlightCell(self):
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
		board = self.board
		(cols, rows) = (self.cols, self.rows)
		for row in xrange(rows):
			for col in xrange(cols):
				self.drawCell(row, col)
	
	def drawBalance(self):
		margin = self.margin
		(textX, textY) = (margin/2, margin/2)
		text = "Balance: %d" % self.farmer.balance
		self.canvas.create_text(textX, textY, anchor=W, text=text, fill='blue')		

	def drawSeeds(self):
		margin = self.margin
		(textX, textY) = (self.canvasWidth-margin/2, margin/2)
		text = "goodSeeds: %d cheapSeeds: %d water: %d" % \
							(self.farmer.goodSeeds, self.farmer.cheapSeeds, 
								self.farmer.water)
		self.canvas.create_text(textX, textY, anchor=E, text=text, fill='blue')

	def drawSpec(self):
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

	def drawGame(self):
		self.drawBoard()
		if self.isChosen and self.chosenCell!=None:
			self.drawHighlightCell()
		self.drawBalance()
		self.drawSeeds()

	def drawSplashScreen(self):
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
		self.app.setTimerDelay(200)
		self.isGameStart = False # test codes, to be changed
		self.isHelpScreen = False
		self.chosenCell = (0, 0)
		self.isChosen = True
		self.spec = ""
		self.farmer = Farmer(10, 0, 0, 0)

farGame = FarmGame(15, 10)

farGame.run()


