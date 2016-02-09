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
		mature = 20
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
		mature = 40
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

	def plantGoodCrop(self):
		if self.goodSeeds>0:
			(row, col) = self.chosenCell
			if self.board[row][col] == self.emptyColor:
				self.board[row][col] = GoodCrop()
				self.goodSeeds -= 1
				self.spec = "You plant a good crop"
			else: 
				self.spec = "Can't plant here"
		else:
			self.spec = "You don't have a seed for good crop"

	def plantCheapCrop(self):
		if self.cheapSeeds>0:
			(row, col) = self.chosenCell
			if self.board[row][col] == self.emptyColor:
				self.board[row][col] = CheapCrop()
				self.cheapSeeds -= 1
				self.spec = "You plant a cheap crop"
			else: 
				self.spec = "Can't plant here"
		else:
			 self.spec = "You don't have a seed for cheap crop"

	def buyGoodSeed(self):
		seedPrice = 2
		if self.balance >=seedPrice:
			self.goodSeeds += 1
			self.balance -= seedPrice
			self.spec = "You buy a good crop seeds"
		else:
			self.spec = "You don't have enough money"

	def buyCheapSeed(self):
		seedPrice = 1
		if self.balance>=seedPrice:
			self.cheapSeeds += 1
			self.balance -= seedPrice
			self.spec = "You buy a cheep crop seed"
		else:
			self.spec = "You don't have enough money"

	def buyWater(self):
		waterPrice = 1
		if self.balance>=waterPrice:
			self.water += 1
			self.balance -= waterPrice
			self.spec = "You buy a water"
		else:
			self.spec = "You don't have enough money"

	def harvest(self):
		board = self.board
		(row, col) = self.chosenCell
		if isinstance(board[row][col], Crop):
			if board[row][col].isMature:
				self.balance += board[row][col].price
				board[row][col] = self.emptyColor
				self.spec = "You havest a crop"
			else: 
				self.spec = "It is not mature"
		else:
			self.spec = "You can't harvest without planting anything"

	def irrigate(self):
		board = self.board
		(row, col) = self.chosenCell
		if self.water==0:
			self.spec = "You have no water"
		else:
			if isinstance(board[row][col], Crop):
				if not board[row][col].isMature:
					accelarate = 10
					for x in xrange(accelarate):
						self.board[row][col].grow()
					self.spec = "You irrigate a crop, it grows a lot"
				else:
					self.spec = "The crop has already been matrue"
			else:
				self.spec = "No crop to water here"


	def onKeyPressed(self, event):
		if (event.keysym == 'p'): self.isGameStart=True 
		if self.isGameStart:
			if (event.keysym == '1'): 
				self.plantGoodCrop() # plant a good crop in current cell
			elif (event.keysym == '2'): 
				self.plantCheapCrop() # plant a cheap crop in current cell
			elif (event.keysym == 'g'): self.buyGoodSeed()
			elif (event.keysym == 'c'): self.buyCheapSeed()
			elif (event.keysym == 'w'): self.buyWater()
			elif (event.keysym == 'h'): self.harvest()
			elif (event.keysym == 'i'): 
				# irrigate the crop when pressing 'i'
				self.irrigate()


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
		text = "Balance: %d" % self.balance
		self.canvas.create_text(textX, textY, anchor=W, text=text, fill='blue')		

	def drawSeeds(self):
		margin = self.margin
		(textX, textY) = (self.canvasWidth-margin/2, margin/2)
		text = "goodSeeds: %d cheapSeeds: %d water: %d" % \
							(self.goodSeeds, self.cheapSeeds, self.water)
		self.canvas.create_text(textX, textY, anchor=E, text=text, fill='blue')

	def drawSpec(self):
		(textX, textY) = (self.canvasWidth/2, self.canvasHeight/2)
		self.canvas.create_text(textX, textY, text=self.spec, anchor=W, 
								fill='red', font='Times 30 bold')

	def drawGame(self):
		self.drawBoard()
		if self.isChosen and self.chosenCell!=None:
			self.drawHighlightCell()
		self.drawBalance()
		self.drawSeeds()
		self.drawSpec()

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
		(cx, cy) = (self.canvasWidth/2, self.canvasHeight/2)
		size = min(self.canvasWidth,self.canvasHeight)/4
		self.canvas.create_rectangle(cx-size, cy-size, cx+size, 
								cy+size, fill='Thistle')
		(left, top) = (cx-size, cy-size)
		linesDistance = 30
		comments = """
This is a farm game, you can plant crops in the  2d grid. You have 
two kinds of crops: a good one worth 20 dollers in the market 
but takes longer to grow and a cheaper one worth 10 dollers but grow faster
1. click in a certain cell to choose a place to edit
2. press '1' to plant a good crop
3. press '2' to plant a cheap crop 
3. press 'g' to buy a good crop seed
4. press 'c' to buy a cheap crop seed
5. press 'w' to buy a water
6. press 'i' to irrigate this
"""
		count = 1
		for line in comments.splitlines():
			self.canvas.create_text(left, top+count*linesDistance, anchor=NW, 
                            text=line, fill='red', font='arial 18')
			count += 1

	def redrawAll(self):
		self.canvas.delete(ALL)
		if not self.isHelpScreen:
			if self.isGameStart:
				self.drawGame()
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
		self.balance = 10
		self.chosenCell = None
		self.isChosen = True
		self.goodSeeds = 0
		self.cheapSeeds = 0
		self.water = 0
		self.spec = ""

farGame = FarmGame(15, 10)

farGame.run()


