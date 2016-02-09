# SnakeClassAnimation.py

# Adapted from: snake8.py from here:
# http://www.kosbie.net/cmu/fall-10/15-110/handouts/snake/snake.html

# Steps required to adapt code:
# 1) Convert functions to methods
# 2) Convert canvas.data["foo"] to self.foo
# 3) Drop canvas as parameter (just use self.canvas)
# 4) Drop calls to redrawAll (framework does that for you now)
# 5) Change "timerFired" to "onTimerFired"
# 6) Change "keyPressed" to "onKeyPressed"
# 7) Change "init" to "initAnimation"
# 8) Add call to self.app.setTimerDelay(250) to initAnimation
# 9) Drop call to canvas.after in timerFired (framework does that for you, too)
# 10) Move width/height calculation from run() function into __init__ method
# 11) Drop the rest of the run() function (again, framework does this already)
# 12) Change call to run(8,16) to: SnakeClassAnimation(8, 16).run()

import random
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class SnakeClassAnimation(BasicAnimationClass):
    def __init__(self, rows, cols):
        margin = 5
        cellSize = 30
        canvasWidth = 2*margin + cols*cellSize
        canvasHeight = 2*margin + rows*cellSize
        super(SnakeClassAnimation, self).__init__(canvasWidth, canvasHeight)
        self.margin = margin
        self.cellSize = cellSize
        self.rows = rows
        self.cols = cols

    def onKeyPressed(self, event):
        self.ignoreNextTimerEvent = True # for better timing
        # first process keys that work even if the game is over
        if (event.char == "q"):   self.gameOver()
        elif (event.char == "r"): self.initAnimation()
        elif (event.char == "d"): self.inDebugMode = not self.inDebugMode
        # now process keys that only work if the game is not over
        if (self.isGameOver == False):
            if (event.keysym == "Up"):      self.moveSnake(-1, 0)
            elif (event.keysym == "Down"):  self.moveSnake(+1, 0)
            elif (event.keysym == "Left"):  self.moveSnake(0,-1)
            elif (event.keysym == "Right"): self.moveSnake(0,+1)

    def moveSnake(self, drow, dcol):
        # move the snake one step forward in the given direction.
        self.snakeDrow = drow # store direction for next timer event
        self.snakeDcol = dcol
        snakeBoard = self.snakeBoard
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        headRow = self.headRow
        headCol = self.headCol
        newHeadRow = headRow + drow
        newHeadCol = headCol + dcol
        if ((newHeadRow < 0) or (newHeadRow >= rows) or
            (newHeadCol < 0) or (newHeadCol >= cols)):
            # snake ran off the board
            self.gameOver()
        elif (snakeBoard[newHeadRow][newHeadCol] > 0):
            # snake ran into itself!
            self.gameOver()
        elif (snakeBoard[newHeadRow][newHeadCol] < 0):
            # eating food!  Yum!
            snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
            self.headRow = newHeadRow
            self.headCol = newHeadCol
            self.placeFood()
        else:
            # normal move forward (not eating food)
            snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
            self.headRow = newHeadRow
            self.headCol = newHeadCol
            self.removeTail()

    def removeTail(self):
        # find every snake cell and subtract 1 from it.  When we're done,
        # the old tail (which was 1) will become 0, so will not be part of the snake.
        # So the snake shrinks by 1 value, the tail.
        snakeBoard = self.snakeBoard
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                if (snakeBoard[row][col] > 0):
                    snakeBoard[row][col] -= 1

    def gameOver(self):
        self.isGameOver = True

    def onTimerFired(self):
        ignoreThisTimerEvent = self.ignoreNextTimerEvent
        self.ignoreNextTimerEvent = False
        if ((self.isGameOver == False) and
            (ignoreThisTimerEvent == False)):
            # only process timerFired if game is not over
            drow = self.snakeDrow
            dcol = self.snakeDcol
            self.moveSnake(drow, dcol)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawSnakeBoard()
        if (self.isGameOver == True):
            cx = self.width/2
            cy = self.height/2
            self.canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))

    def drawSnakeBoard(self):
        snakeBoard = self.snakeBoard
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                self.drawSnakeCell(row, col)

    def drawSnakeCell(self, row, col):
        margin = self.margin
        cellSize = self.cellSize
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill="white")
        if (self.snakeBoard[row][col] > 0):
            # draw part of the snake body
            self.canvas.create_oval(left, top, right, bottom, fill="blue")
        elif (self.snakeBoard[row][col] < 0):
            # draw food
            self.canvas.create_oval(left, top, right, bottom, fill="green")
        # for debugging, draw the number in the cell
        if (self.inDebugMode == True):
            self.canvas.create_text(left+cellSize/2,top+cellSize/2,
                               text=str(self.snakeBoard[row][col]),font=("Helvatica", 14, "bold"))

    def loadSnakeBoard(self):
        rows = self.rows
        cols = self.cols
        snakeBoard = [ ]
        for row in range(rows): snakeBoard += [[0] * cols]
        snakeBoard[rows/2][cols/2] = 1
        self.snakeBoard = snakeBoard
        self.findSnakeHead()
        self.placeFood()

    def placeFood(self):
        # place food (-1) in a random location on the snakeBoard, but
        # keep picking random locations until we find one that is not
        # part of the snake!
        snakeBoard = self.snakeBoard
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        while True:
            row = random.randint(0,rows-1)
            col = random.randint(0,cols-1)
            if (snakeBoard[row][col] == 0):
                break
        snakeBoard[row][col] = -1

    def findSnakeHead(self):
        # find where snakeBoard[row][col] is largest, and
        # store this location in headRow, headCol
        snakeBoard = self.snakeBoard
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        headRow = 0
        headCol = 0
        for row in range(rows):
            for col in range(cols):
                if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                    headRow = row
                    headCol = col
        self.headRow = headRow
        self.headCol = headCol

    def printInstructions(self):
        print "Snake!"
        print "Use the arrow keys to move the snake."
        print "Eat food to grow."
        print "Stay on the board!"
        print "And don't crash into yourself!"
        print "Press 'd' for debug mode."
        print "Press 'r' to restart."

    def initAnimation(self):
        self.printInstructions()
        self.loadSnakeBoard()
        self.inDebugMode = False
        self.isGameOver = False
        self.snakeDrow = 0
        self.snakeDcol = -1 # start moving left
        self.ignoreNextTimerEvent = False
        self.app.setTimerDelay(250)

SnakeClassAnimation(8, 16).run()
