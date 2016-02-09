# hw8.py
# Zekun Lyu + zlyu + R
# Xinyue Wu + xinyuew + I

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random
import copy
from Tkinter import *
from basicAnimationClass import BasicAnimationClass

class Tetris(BasicAnimationClass):
    def __init__(self, rows, cols):
        # initialize data and canvas
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
        # check if the current fallingPiece is legal
        piece = self.piece
        board = self.tetrisBoard
        (pieceRows, pieceCols) = (len(piece),len(piece[0]))
        (rows, cols) = (self.rows, self.cols)
        (startRow, startCol) = (self.fallingPieceRow, self.fallingPieceCol)
        for row in xrange(pieceRows):
            for col in xrange(pieceCols):
                if piece[row][col] == True:
                    # when the element in fallingPiece board is true
                    # check if it is at illegal place
                    # illegal situation is: outof bound or collide with 
                    # the unempty cell in board
                    if startRow + row >= rows: return False
                    if startCol + col >= cols: return False
                    if startRow + row < 0: return False
                    if startCol + col < 0: return False
                    emptyColor = 'blue'
                    if (board[startRow+row][startCol+col]!=emptyColor):
                        return False
        return True

    def moveFallingPiece(self, drow, dcol):
        # move the fallingPiece, drow is vertical change
        # dcol is horizontal change
        self.fallingPieceRow += drow
        self.fallingPieceCol += dcol

        # after move, if the fallingpiece is illegal
        # undo this move and return False
        # if not, return True
        if not self.fallingPieceIsLegal():
            self.fallingPieceRow -= drow
            self.fallingPieceCol -= dcol
            return False
        return True
        
    def rotateFallingPiece(self):
        #let the falling piece rotate in conterclock direction
        oldPiece = self.piece#store piece before rotated
        (rows, cols) = (len(oldPiece), len(oldPiece[0]))
        newPiece = [] #store new piece
        for row in range(cols): newPiece +=[[None] * rows]
        for row in xrange(rows):
            for col in xrange(cols):
                newPiece[cols-1-col][row] = oldPiece[row][col]
        self.piece = newPiece
        # if the falling piece after rotated is illegal, undo this rotate
        if not self.fallingPieceIsLegal():
            self.piece = oldPiece

                
    def onKeyPressed(self, event):
        # react to key pressed event
        # when 'r' is pressed, reinitialized the game object
        #if (event.keysym == "r") : self.initAnimation()

        # when isGameOver is not true
        # move the falling piece by pressing 'Down', 'Right' and 'Left'
        # and rotate it by press 'Up'
        if (not self.isGameOver):
            if (event.keysym == "Down"): self.moveFallingPiece(+1,0)
            elif (event.keysym == "Left"): self.moveFallingPiece(0,-1)
            elif (event.keysym == "Right"): self.moveFallingPiece(0,+1)
            elif (event.keysym == "Up"): self.rotateFallingPiece()
            elif (event.char == 'r'): 
                while self.moveFallingPiece(0,+1) : pass

    def isFullRow(self,row):
        # take the number of a certain row and check if this row
        # is full, that is to say, no empty cell in this row
        emptyColor = "blue"
        board = self.tetrisBoard
        for col in xrange(self.cols):
            if board[row][col] == emptyColor: return False
        return True
        


    def removeFullRows(self):
        board = self.tetrisBoard
        rows, cols = self.rows, self.cols
        newRow = oldRow = rows-1
        fullRows = 0
        for x in xrange(rows):
            if not self.isFullRow(oldRow):
                board[newRow] = copy.copy(board[oldRow])
                newRow -= 1
            else:
                fullRows += 1
            oldRow -= 1
        for row in xrange(fullRows):
            board[row] = ['blue']*cols
        self.score += fullRows*fullRows
        """# this function remove all the full rows in current board
        (board, rows, cols) = (copy.deepcopy(self.tetrisBoard), self.rows, self.cols)
        newBoard = []
        oldRow = rows
        emptyColor = 'blue'
        # check each row from downside up
        # if a certain row is not full, add it to the board from downside up
        # if it is full, then update score
        # at last add n empty rows in the top of the newBoard
        # n is the number of full rows in old board
        while(oldRow > 0):
            oldRow -= 1;
            if (self.isFullRow(oldRow) == False):
                newBoard = [board[oldRow]] + newBoard
        fullRows = rows - len(newBoard)
        self.score += fullRows*fullRows
        for x in xrange(fullRows):
            newBoard = [[emptyColor]*cols] + newBoard
        self.tetrisBoard = newBoard"""

    def placeFallingPiece(self):
        # if fallingpiece collides with board, place it into board
        startRow = self.fallingPieceRow;
        startCol = self.fallingPieceCol;
        (piece, pieceColor) = (self.piece, self.pieceColor)
        (rows, cols) = (len(piece),len(piece[0]))
        # check cells of fallingpiece one by one
        # if it is true, assign current pieceColor 
        # to corresponding cell in board
        for row in xrange(rows):
            for col in xrange(cols):
                if (piece[row][col]==True):
                    self.tetrisBoard[startRow+row][startCol+col] = pieceColor
        # after place Falling piece, remove all the full rows and update score
        self.removeFullRows()

    def onTimerFired(self):
        # when timer is fired, move falling piece down by one cell
        if (self.isGameOver==False):
            if not self.moveFallingPiece(+1,0):
                self.placeFallingPiece()
                self.newFallingPiece()
                if (self.fallingPieceIsLegal() == False):
                    self.isGameOver = True

    def initPieces(self):
        # store pieces type and piece color
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
        # randomly generate a piece and piece color  
        # and place it in the middle top  
        (tetrisPieces,tetrisPieceColors) = self.initPieces()
        n = random.randint(0,6)
        (self.piece, self.pieceColor) = (tetrisPieces[n], tetrisPieceColors[n])
        self.fallingPieceRow = 0
        middle = self.cols/2  - len(self.piece[0])/2
        self.fallingPieceCol = middle


    def drawCell(self, row, col, color):
        # drawing the cell given it's row an col
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
        # drawing falling piece
        # to do this, draw the cell in falling piece that is true
        startRow = self.fallingPieceRow;
        startCol = self.fallingPieceCol;
        (piece, pieceColor) = (self.piece, self.pieceColor)
        (rows, cols) = (len(piece),len(piece[0]))
        for row in xrange(rows):
            for col in xrange(cols):
                if (piece[row][col]==True):
                    self.drawCell(startRow+row, startCol+col, pieceColor)

    def drawScore(self):
        # visulaize the score in canvas
        margin = self.margin
        (textX, textY) = (margin/2, margin/2)
        text = "Score: %d" % self.score
        self.canvas.create_text(textX, textY, anchor=W, text=text, fill='blue')             
    
    def drawSpec(self):
        # draw spectation in canvas
        margin = self.margin
        (textX, textY) = (self.canvasWidth-margin/2, margin/2)
        text = "Press 'r' to restart!"
        self.canvas.create_text(textX, textY, anchor=E, text=text, fill='blue')             


    def drawGame(self):
        # visualize the game
        self.canvas.create_rectangle(0, 0, self.canvasWidth, 
                                        self.canvasHeight, fill='orange')
        self.drawBoard()
        self.drawFallingPiece()
        self.drawScore();
        self.drawSpec();


    def drawGameOver(self):
        # when game is over, draw the comments
        (cx, cy) = (self.canvasWidth/2, self.canvasHeight/2)
        text = "Game Over!"
        self.canvas.create_text(cx, cy, text=text, 
                                fill='red', font='arial 40 bold')

    def redrawAll(self):
        # redraw all items
        self.canvas.delete(ALL)
        self.drawGame();
        if self.isGameOver:
            self.drawGameOver();


    def loadTetrisBoard(self):
        rows = self.rows
        cols = self.cols
        board = []
        for row in range(rows): board +=[["blue"] * cols]
        self.tetrisBoard = board

    def initAnimation(self):
        # initialize the game
        self.loadTetrisBoard()
        self.newFallingPiece()
        self.app.setTimerDelay(500)
        self.isGameOver = False
        self.score = 0



tetris = Tetris(15, 10)  # play Tetris on a 15x10 board
                         # (must work for any reasonable dimensions)
tetris.run()

def initializeBoard():
    board=[
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'red','blue',  'red', 'blue', 'red', 'blue','green'],
            [ 'yellow','yellow', 'yellow','yellow','yellow','yellow', 'orange']
        ]
    return board

def initializeBoard2():
    board=[
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'red','red', 'red','red', 'red','red','red'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'red','blue',  'red', 'blue', 'red', 'blue','green'],
            [ 'yellow','yellow', 'yellow','yellow','yellow','yellow', 'orange']
        ]
    return board

def boardAfterCheck():
    board=[
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'blue','blue', 'blue','blue', 'blue','blue','blue'],
            [ 'red','blue',  'red', 'blue', 'red', 'blue','green']
        ]
    return board


def testFallingPieceIsLegal(tetris):
    print "Testing fallingPieceIsLegal...",
    tetris.fallingPieceRow,tetris.fallingPieceCol = 0,1
    assert (tetris.fallingPieceIsLegal()==True)
    tetris.fallingPieceRow,tetris.fallingPieceCol = -1,1
    assert (tetris.fallingPieceIsLegal()==False)
    tetris.fallingPieceRow,tetris.fallingPieceCol = 3,6
    assert (tetris.fallingPieceIsLegal()==False)
    tetris.fallingPieceRow,tetris.fallingPieceCol = 6,1
    assert (tetris.fallingPieceIsLegal()==False)
    print "Passed!"

def testRemoveFullRows(tetris):
    print "Testing removeFullRows...",
    tetris.tetrisBoard = initializeBoard2()
    tetris.score = 0 
    tetris.removeFullRows()
    assert(tetris.tetrisBoard == boardAfterCheck())
    print "Passed!"

def testAll():
    tetris = Tetris(9, 7)
    tetris.tetrisBoard = initializeBoard()
    (tetrisPieces,tetrisPieceColors) = tetris.initPieces()
    (tetris.piece, tetris.pieceColor) = (tetrisPieces[3], tetrisPieceColors[3])
    testFallingPieceIsLegal(tetris)
    testRemoveFullRows(tetris)

if __name__ == "__main__":
    testAll()

