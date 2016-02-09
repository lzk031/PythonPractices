# hw7.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################

def areLegalValues(values):
    #take a list of n integer, return false if there is a number larger than num
    #or less than 0 or a number appear more than once.
    n = len(values);
    for num in values:
        if num < 0 or num > n:
            return False
        elif num == 0:
            continue
        elif values.count(num)>1:
            return False
    return True

def isLegalRow(board, row):
    #this funciton takes a row in block and check if it is a legal row
    #create a list consists of elements in the row and use areLegalValues() to
    #check if it is legal
    return areLegalValues(board[row])



def isLegalCol(board, col):
    #this funciton takes a coloumn in block and check if it is a legal row
    #create a list consists of elements in the coloumn and use areLegalValues() 
    #to check if it is legal
    n = len(board)
    column = []*n
    for x in xrange(n):
        column.append(board[x][col])
    return areLegalValues(column)

def isLegalBlock(board, block):
    #this funciton takes a block in block and check if it is a legal row
    #create a list consists of elements in the block and use areLegalValues() 
    #to check if it is legal
    n = int(round(len(board)**0.5))
    values = list()
    startRow = block/n*n
    startCol = block%n*n
    for row in xrange(n):
        for col in xrange(n):
            values.append(board[startRow+row][startCol+col])
    return areLegalValues(values)

def isLegalSudoku(board):
    #this function check if the given board stands for a valid sudoku
    n = len(board)

    #check each row, if we find a illegal row, return False
    for row in xrange(n):
        if not isLegalRow(board, row):
            return False
    #check each coloum, return false if finding a illegal coloum
    for col in xrange(n):
        if not isLegalCol(board, col):
            return False
    #check each block, return false if finding a illegal block
    for block in xrange(n):
        if not isLegalBlock(board, block):
            return False
    return True


import copy

def friendsOfFriends(d):

    result = dict()
    #find all the people's fof one by one
    for people in d:
        result[people] = set()
    #loop through other people in d which is called friend here
        for friend in d:
            if friend in d[people]:
                fof = copy.copy(d[friend])
                #check if friend's friend is included in people's friend
                #if so, remove them.
                for person in d[friend]:
                    if person in d[people]:
                        fof.remove(person)
                #also remove people himself
                    if people in fof:
                        fof.remove(people)
                result[people].update(fof)
    return result

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
from Tkinter import *
from basicAnimation import BasicAnimationRunner

def fillCell(canvas, event):
    #each time user insert a valid number into a valid position,
    #we update the board, and lists used for undo and redo
    board = canvas.data.board
    (row, col) = (canvas.data.row, canvas.data.col)
    step = canvas.data.step
    #remove the information for the step after the current step
    canvas.data.histValue = canvas.data.histValue[0:step]
    canvas.data.newValue = canvas.data.newValue[0:step]
    canvas.data.histPosition = canvas.data.histPosition[0:step]

    #store the value of the cell before changing it 
    canvas.data.histValue.append(board[row][col])
    board[row][col] = int(event.keysym)

    #store the changed value of the cell
    canvas.data.newValue.append(board[row][col])
    canvas.data.histPosition.append((row, col))
    canvas.data.step += 1

def undo(canvas):
    #go back to the position of last step and give back t
    #he former value to the cell
    board = canvas.data.board
    if canvas.data.step > 0:
        canvas.data.step -= 1
        (row, col) = canvas.data.histPosition[canvas.data.step]
        board[row][col] = canvas.data.histValue[canvas.data.step]


def redo(canvas):
    #go on th the position of next step and refill the value
    board = canvas.data.board    
    maxStep = len(canvas.data.histPosition)
    if canvas.data.step < maxStep:
        (row, col) = canvas.data.histPosition[canvas.data.step]
        board[row][col] = canvas.data.newValue[canvas.data.step]

        canvas.data.step += 1


def onKeyPressed(canvas, event):
    #when key is pressed, check if it is a valid comments
    #and do some control
    board = canvas.data.board
    (row, col) = (canvas.data.row, canvas.data.col)
    n = len(board)
    #if the key is h or g, switch the window
    if(event.keysym == "h"): canvas.data.inHelpScreen = True
    elif(event.keysym == "g"): canvas.data.inHelpScreen = False
    # if it is in the game window, control the game
    if not canvas.data.inHelpScreen:
        #only when the board is legal the user can move his highlight cell
        #when the highlight cell can't move beyond the boundary
        if canvas.data.legal and (event.keysym == "Up") and (row>0):
            canvas.data.row -= 1
        elif canvas.data.legal and (event.keysym == "Down") and (row<n-1):
            canvas.data.row += 1
        elif canvas.data.legal and (event.keysym == "Left") and (col>0):
            canvas.data.col -= 1
        elif canvas.data.legal and (event.keysym == "Right") and (col<n-1):
            canvas.data.col += 1
        elif(event.keysym<=str(n)) and (event.keysym>='1') \
            and canvas.data.editable[row][col]: fillCell(canvas, event)
        elif event.keysym == 'u': undo(canvas)
        elif event.keysym == 'r': redo(canvas)


def checkLegalBoard(canvas):
    #check if the current board stands for a legal sudoku
    board = canvas.data.board
    if not isLegalSudoku(board):
        canvas.data.legal = False
    else:
        canvas.data.legal = True

def isSolved(canvas):
    #check if the puzzle is solved
    #only when a legal board is filled with non-zero numbers, the puzzle will
    #be solved.
    board = canvas.data.board
    n = len(board)
    if not isLegalSudoku(board): return False
    if isLegalSudoku(board):
        for row in xrange(n):
            for col in xrange(n):
                if board[row][col] == 0:
                    return False
        return True



def onTimerFired(canvas):
    #each time goes in, canvas.data.sec add 1, and carry over if necessary
    canvas.data.sec += 1
    if canvas.data.sec%60 == 0:
        canvas.data.min += 1
        canvas.data.sec = 0
    if canvas.data.min == 60:
        canvas.data.hour += 1
        canvas.data.min =0


def initEditable(canvas):
    #this function make a 2d list which tell us if a element in the board is
    #editable, True stand for editable, False stands for uneditable.
    board = canvas.data.board
    n = len(board)
    for row in xrange(n): 
        canvas.data.editable += [[False]*n]
        for col in xrange(n):
            if board[row][col] == 0:
                canvas.data.editable[row][col] = True




def init(canvas, extraArg):
    #n = len(board)
    canvas.app.setTimerDelay(1000)
    canvas.data.board = extraArg
    
    #make a state imply if it is help screen now
    canvas.data.inHelpScreen = False

    #the following three variables store the time used
    canvas.data.sec = 0
    canvas.data.min = 0
    canvas.data.hour = 0

    #create a list having the same dimension with board that tell
    #us which position in the board is editable or chagable
    canvas.data.editable = []
    initEditable(canvas)

    #the following two variale tell us where the current cell is
    canvas.data.row = 0
    canvas.data.col = 0

    canvas.data.legal = True #if the board now is legal

    canvas.data.histPosition = [] #store user's position in each step
    canvas.data.histValue = [] #store the value of the cell before chaged
    canvas.data.newValue = [] #store the new value of the cell after changed

    canvas.data.step = 0 #step of users move

def drawNumber(canvas):
    #this functin take in a 2d list board and 
    #fill in the non-zero number in the grid
    board = canvas.data.board
    (left, top) = (50, 50)
    side = 500
    n = len(board)
    unitLength = float(side)/n 
    for row in xrange(n):
        for col in xrange(n):
            color = 'blue' if canvas.data.editable[row][col] else 'black'
            if board[row][col]!=0:
                number = '%d' % board[row][col]
                (centerX, centerY) = (left+col*unitLength+0.5*unitLength, 
                                        top+row*unitLength+0.5*unitLength)
                canvas.create_text(centerX, centerY, fill=color, 
                                    text=number, font='arial 20')

def drawHighlightCell(canvas):
    #draw highlight cell frame
    board = canvas.data.board
    n = int(len(board)**0.5)
    (left, top) = (50, 50)
    side = 500
    lenthUnit = float(side)/(n*n)
    boldLine = 3
    (cellLeft, cellTop) = (left+canvas.data.col*lenthUnit,
                            top+canvas.data.row*lenthUnit)
    canvas.create_line(cellLeft, cellTop, cellLeft+lenthUnit, 
                        cellTop, fill='gold', width = boldLine)
    canvas.create_line(cellLeft+lenthUnit, cellTop, cellLeft+lenthUnit, 
                        cellTop+lenthUnit, fill='gold', width = boldLine)
    canvas.create_line(cellLeft+lenthUnit, cellTop+lenthUnit, cellLeft, 
                        cellTop+lenthUnit, fill='gold', width = boldLine)
    canvas.create_line(cellLeft, cellTop+lenthUnit, cellLeft, 
                        cellTop, fill='gold', width = boldLine)

def drawGrid(canvas):
    #this functin take in canvas and the board
    #draw the grid of the game, note that the 
    #frame of the block is black, other line is gray
    board = canvas.data.board
    n = int(len(board)**0.5)
    (left, top) = (50, 50)
    side = 500
    lenthUnit = float(side)/(n*n)
    blockSide = float(side)/n
    boldLine = 3
    for i in xrange(n+1):
        canvas.create_line(left, top+i*blockSide, left+side,
                            top+i*blockSide, width=boldLine)
        canvas.create_line(left+i*blockSide, top, left+i*blockSide,
                            top+side, width=boldLine)
    for i in xrange(n*n+1):
        if i%n != 0:
            canvas.create_line(left, top+i*lenthUnit, left+side,
                                top+i*lenthUnit,fill='gray')
            canvas.create_line(left+i*lenthUnit, top, left+i*lenthUnit,
                                top+side, fill='gray')
    drawHighlightCell(canvas)
    
def drawIllegalSignal(canvas):
    #fill in the cell with red to tell the user this move is wrong
    board = canvas.data.board
    (row, col) = (canvas.data.row, canvas.data.col)
    n = len(board)
    (left, top) = (50, 50)
    side = 500
    lenthUnit = float(side)/n
    canvas.create_rectangle(left+col*lenthUnit, top+row*lenthUnit, 
                            left+(col+1)*lenthUnit, top+(row+1)*lenthUnit, 
                            fill='red')

def drawToHelpScreen(canvas):
    #create a mark telling user how to get help
    (left, top) = (420,600)
    (width,height) = (130,50)
    canvas.create_rectangle(left, top, left+width,
                            top+height, fill='Medium Orchid') 
    (textX, textY) = (left+width/2, top+height/2)
    text = "      press 'h'\n to help screen"
    canvas.create_text(textX, textY, fill='gray', 
                    text=text, font='arial 16')    

def redrawAll(canvas):
    canvas.delete(ALL)
    #the canvas is not legal, fill red color in the current cell
    if not canvas.data.legal:
        drawIllegalSignal(canvas)

    #initialize the grid
    drawGrid(canvas)
    #fill in number in to cells
    drawNumber(canvas)
    #draw a mark that tells user how to get to help screen
    drawToHelpScreen(canvas)

def drawBackground(canvas):
    (left, top, right, bottom) = (50, 50, 550, 550)
    canvas.create_rectangle(left, top, right, bottom, fill='Light Sky Blue')
    tittle = 'Help Screen'
    middleX = (left+right)/2
    canvas.create_text(middleX, top, anchor=S,text=tittle, 
                        fill='red', font='arial 24 bold')

def drawHelpCommend(canvas):
    #display the help command in the window
    (left, top, right, bottom) = (50, 50, 550, 550)
    linesDistance = 30
    commends = """

    1. use 'up' 'down' 'left' 'right' to control the 
        highlight frame.

    2. move the highlight frame to a certain cell and 
        fill in a number from keyboard, the valid number 
        is between 1 to the number of rows in the board. 
        Note that the number in black can't be change.

    3. if you enter in a number that make the sudoku illegal,
        the cell will turn red, and you can not move the 
        highlight frame before fixing it.

    4. press 'u' to undo, press 'r' to redo. you can undo and 
        redo arbitary number of steps"""
    count = 1
    for line in commends.splitlines():
        canvas.create_text(left, count*linesDistance, anchor=NW, 
                            text=line, fill='red', font='arial 18')
        count += 1

def drawReturnGame(canvas):
    #draw a mark that tell the user how to return to game window
    (left, top) = (420,600)
    (width,height) = (130,50)
    canvas.create_rectangle(left, top, left+width,
                            top+height, fill='Medium Orchid') 
    (textX, textY) = (left+width/2, top+height/2)
    text = "press 'g' to return"
    canvas.create_text(textX, textY, fill='gray', 
                    text=text, font='arial 16')   


def drawHelpScreen(canvas):
    canvas.delete(ALL)
    drawBackground(canvas)
    drawHelpCommend(canvas)
    drawReturnGame(canvas)

def drawCounter(canvas):
    (left, top) = (50,600)
    (width,height) = (130,50)
    canvas.create_rectangle(left, top, left+width, top+height, fill='green')
    count = "%02d: %02d: %02d" % (canvas.data.hour, 
                                    canvas.data.min, canvas.data.sec)
    (countX, countY) = (left+width/2, top+height/2)
    canvas.create_text(countX, countY, fill='white', 
                    text=count, font='arial 24 bold')

def drawCong(canvas):
    (width, height) = (600, 700)
    (centerX, centerY) = (width/2, height/2)
    canvas.create_text(centerX, centerY, fill='red',
        text='     Congratulations!\nYou solved this puzzle', 
        font='arial 30 bold')


def doSudoku(app, canvas, extraArg):
    init(canvas, extraArg) 
    while app.isRunning():
        #check if the puzzle has been solved, if true, break the loop
        if isSolved(canvas): break

        #check if the current board is legal sudoku
        checkLegalBoard(canvas)

        (eventType,event) = app.getEvent()
        if (eventType == "keyPressed"): onKeyPressed(canvas, event)
        elif (eventType == "timerFired"): onTimerFired(canvas)
        if not canvas.data.inHelpScreen:
            redrawAll(canvas)
        else:
            drawHelpScreen(canvas)
        drawCounter(canvas)

    #if the puzzle is solved, inform the user
    drawCong(canvas)




def playSudoku(initialBoard):
    BasicAnimationRunner(doSudoku, width=600, height=700, extraArg=initialBoard)




def testAreLegalValues():
    print "Testing areLegalValues()...",
    assert (areLegalValues([0])==True)
    assert (areLegalValues([1,2,3,4,4])==False)
    assert (areLegalValues([1,8,2])==False)
    assert (areLegalValues([1,6,2,5,4,3,7])==True)
    print "Passed!"

def testIsLegalRow(board):
    print "Testing isLegalRow...",
    assert (isLegalRow(board,0)==True)
    assert (isLegalRow(board,3)==False)
    assert (isLegalRow(board,5)==True)
    print "Passed!"

def testIsLegalCol(board):
    print "Testing isLegalCol...",
    assert (isLegalCol(board,0)==True)
    assert (isLegalCol(board,7)==False)
    print "Passed!"

def testIsLegalBlock(board):
    print "Testing isLegalBlock...",
    assert (isLegalBlock(board,0)==True)
    assert (isLegalBlock(board,4)==False)
    assert (isLegalBlock(board,8)==False)
    print "Passed!"

def makeTestSudokuBoard1():
    return [
            [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
            [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
            [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
            [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
            [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
            [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
            [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
            [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
            [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
           ]

def makeTestSudokuBoard2():
    return [
          [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
          [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
          [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
          [ 8, 0, 10, 0, 6, 0, 0, 0, 3 ],
          [ 4, 0, 0, 8, 6, 3, 0, 0, 1 ],
          [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
          [ 0, 0, 0, 0, 0, 0, 0, -1, 0 ],   
          [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
          [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
    ] 

def makeTestSudokuBoard3():
    return [
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ] 

def testIsLegalSudoku():
    print "Testing isLegalSudoku...",
    assert (isLegalSudoku(makeTestSudokuBoard1())==True)
    assert (isLegalSudoku(makeTestSudokuBoard2())==False)
    assert (isLegalSudoku(makeTestSudokuBoard3())==True)
    print "Passed!"

def makeFriendsDictionary1():
    return {'barney': set([]), 'dino': set([]), 
        'fred': set(['bam-bam', 'wilma', 'betty', 'barney']), 
        'betty': set([]), 'bam-bam': set([]), 
        'wilma': set(['dino', 'betty', 'fred'])}

def makeFriendsDictionary2():
    return {'A': set(['B', 'D', 'F']), 'C': set([]), 
            'B': set(['A', 'C', 'E', 'D']), 'E': set(['C', 'D']), 
            'D': set(['B', 'E', 'F']), 'F': set(['D'])}

def testFriendsOfFriends():
    print "Testing friendsOfFriends...",
    assert (friendsOfFriends(makeFriendsDictionary1())\
        =={'barney': set([]), 'dino': set([]), 'fred': set(['dino']), 
            'betty': set([]), 'bam-bam': set([]), 
            'wilma': set(['bam-bam', 'barney'])})
    assert (friendsOfFriends(makeFriendsDictionary2())\
        =={'A': set(['C', 'E']), 'C': set([]), 'B': set(['F']), 
            'E': set(['B', 'F']), 'D': set(['A', 'C']), 'F': set(['B', 'E'])})
    print "Passed!"


def runPlaySudoku():
    board1=[
  [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
  [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
  [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
  [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
  [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
  [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
  [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
  [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
  [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
    ] 
    board2=[
    [1,2,3,4],
    [3,4,1,2],
    [2,3,4,1],
    [0,0,0,0]
    ]
    board3=[[0]]
    playSudoku(board1)

def testAll():
    board=[
            [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
            [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
            [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
            [ 8, 0, 10, 0, 6, 0, 0, 0, 3 ],
            [ 4, 0, 0, 8, 6, 3, 0, 0, 1 ],
            [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
            [ 0, 0, 0, 0, 0, 0, 0, -1, 0 ],
            [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
            [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
        ]
    testAreLegalValues()
    testIsLegalRow(board)
    testIsLegalCol(board)
    testIsLegalBlock(board)
    testIsLegalSudoku()
    testFriendsOfFriends()
    runPlaySudoku()

if __name__ == "__main__":
    testAll()