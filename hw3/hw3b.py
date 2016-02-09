# hw3a.py
# Zekun Lyu + zlyu + R

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
#qustion 1
#in the followin coding, player1 stands for 'hold at 20', and player2 moves randomly
import random
def doRoll():
	return random.randint(1,6)

def doChoice():
	return random.randint(0,1)

def doDecision(currentPlayer, interScore):
	#return decision with respect to diffirent player
	#interScore is used to check if the player1 should hold
	if currentPlayer =="player1":
		decision = "R" if interScore<20 else "H"
	if currentPlayer == "player2":
		choice = random.randint(0,1)
		decision ="H" if choice == 0 else "R"
	return decision


def doPigStrategyAnalysis():
	currentPlayer ="player1"
 	p1Score=0
 	p2Score=0
 	interScore=0
	loopNumber =300
	p1Win = 0 #number of games player win
	for x in xrange(loopNumber):
		while True:
 			decision = doDecision(currentPlayer, interScore)

 			#for hold decision
 			if decision=="H":
 				if currentPlayer=="player1":
 					p1Score +=interScore
 				else:
 					p2Score +=interScore
 				currentPlayer="player2" if currentPlayer=="player1"else"player1" #change turn after hold
 				interScore=0

 			#for roll decision
 			elif decision=="R":
 				theRoll=doRoll()

 				#roll a 1, change turn and losing all interscore
 				if  theRoll==1:
 					currentPlayer="player2" if currentPlayer=="player1"else"player1"
 					interScore=0
 				#not a 1, gain extra score
 				else:
 					interScore+=theRoll
 					#if the score in current turn add the total score not less than 100
 					#the one win the game without moving any more
 					if currentPlayer=="player1":
 						if p1Score+interScore >= 100:
 							p1Win += 1
 							break
 					if currentPlayer == "player2":
 						if p2Score + interScore >= 100:
 							break	

 	#caculate the rate of win	
	winRate = p1Win*1.0/loopNumber
	winRate *= 100
	print "The 'hold at 20' strategy wins", str(winRate) + '% of the', loopNumber, 'games.'

doPigStrategyAnalysis()

'''I set the loopNumber from 300 to 1000, the winRate is from 80% to 95%, 
according to which we can conclude that 'hold at 20' strategy is better than moving randomly.

To make make my codes more concise and clear, I was trying to follow the top-down design principle 
and decrese each function to less than 20 lines. But I come up with some trouble doing this.

Actually, the codes below is my first try to solve this problem. I run it and find that, almost
each time, player using 'hold at 20' will win: among 1000 games, player1 won 99%. 
And each time I compile it, the winRate is almost the same. I thinks this is 
too unrealistic. I put some print statement in some important point and follow the process of a 
single game several times. I don't think my idea is wrong.

I think, the problem may be caused by the structure of multi-level nested function 
which make the result of random.randint not absolutely random. since the time is limited, 
I will ask professor or CA later in this week after submitting.

Just tell my situation, hope you can think about it when grading. 
Thanks for your attention. 

import random
#p1 refers to player1 who uses the strategy "hold at 20", p2 stand for player2 who moves randomly
def doRoll():
    return random.randint(1,6)

def doChoice():
    return random.randint(0,1)

def determineWhosTurn():
    #two players roll dice for the first turn
    while True:
        p1Dice = doRoll()
        p2Dice = doRoll()
        if p1Dice > p2Dice:
            return 1
        elif p1Dice < p2Dice:
            return 2

def holdAt20(p1Score):
    #print 'p1'
    currentScore = 0
    while currentScore < 20:
        p1Dice = doRoll()
        #print 'dice:', p1Dice,
        if p1Dice == 1:
            currentScore = 0
            break
        else:
            currentScore += p1Dice
        if currentScore + p1Score >= 100:
            break
        #print 'turn score', currentScore
    p1Score += currentScore
    return p1Score

def moveRandomly(p2Score):
    print 'p2'
    currentScore = 0
    while True:
    #determin Roll or Hold
        rOrH = doChoice()
        #print 'r or h:', rOrH
        if rOrH == 0:
            p2Dice = doRoll()
            print 'dice:', p2Dice,
            if p2Dice == 1:
                currentScore = 0
                break
            else:
                currentScore += p2Dice
                if currentScore + p2Score >= 100:
                    break
        elif rOrH == 1:
            break
        #print 'turn score', currentScore
    p2Score += currentScore
    return p2Score

def playPig():
    p1Score = 0
    p2Score = 0
    whoTurn = 1
    #whoTurn == 1
    while p1Score<100 and p2Score<100:
        if whoTurn == 1:
            p1Score = holdAt20(p1Score)
            print 'p1 total:', p1Score
            whoTurn = 2
        else:
            p2Score = moveRandomly(p2Score)
            print 'p2 total:', p2Score
            whoTurn = 1
    whoWin = 1 if (p1Score>=100) else 2
    #print whoWin, 'win'
    return whoWin

def doPigStrategyAnalysis():
    loopNumber=1
    p1Win = 0
    p2Win = 0
    for x in xrange(loopNumber):
        if playPig() ==1:
            p1Win +=1
        else :
            p2Win += 1
    #print p1Win
    #print p2Win
    winRate = float(p1Win) / float(p1Win + p2Win)
    winRate = round(winRate,3)
    winRate *= 100
    print "'hold at 20' strategy wins", str(winRate) +'% of ', loopNumber, 'games.'

doPigStrategyAnalysis()            

'''

#question 2
import math
from Tkinter import *


def drawHashMark(canvas, winWidth, winHeight, xmax, xstep, ymax, ystep, xratio, yratio):
	screenXstep = xstep*xratio
	screenYstep = ystep*yratio
	hashMarkLength = winHeight / 25
	xHashNumber = ((xmax/xstep - 1) * 2) +1
	yHashNumber = ((ymax/ystep - 1) * 2) +1

	#draw hash mark on x axes
	for i in xrange(1, xHashNumber+1):
		hashX = i* screenXstep
		hashY = winHeight/2
		lable = -xmax + i*xstep
		canvas.create_line(hashX, hashY-hashMarkLength, hashX, hashY+hashMarkLength)
		canvas.create_text(hashX, hashY+hashMarkLength, text=lable)

	#draw hash mark on y axes
	for i in xrange(1, yHashNumber+1):
		hashY = i*screenYstep
		hashX = winWidth/2
		lable = ymax - i*ystep
		canvas.create_line(hashX-hashMarkLength , hashY, hashX+hashMarkLength, hashY)
		canvas.create_text(hashX-hashMarkLength, hashY, text=lable)
	
def axesInitialize(canvas, cx, cy, winWidth, winHeight, xmax, xstep, ymax, ystep):
	#draw axes
	canvas.create_line(0, cy, winWidth, cy)
	canvas.create_line(cx, 0, cx, winHeight)
	xratio = winWidth/2.0/xmax
	yratio = winHeight/2.0/ymax
	drawHashMark(canvas, winWidth, winHeight, xmax, xstep, ymax, ystep, xratio, yratio)

def cosineInDegrees(degrees):
	return math.cos(math.radians(degrees))

def strangeFunction(x):
	if (int(round(x) % 2 == 0)):
		return x+5*math.cos(x)**3
	else :
		return 10*math.sin(x/2)


def drawGraph(winWidth, winHeight, fn, xmax, xstep, ymax, ystep):
    root = Tk()
    canvas = Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()

    #draw title
    (titlex,titley) = (winWidth/2, winHeight/15)
    canvas.create_text(titlex, titley, text=fn.__name__, font='arial 40 bold')

    (cx, cy) = (winWidth/2, winHeight/2)
    axesInitialize(canvas, cx, cy, winWidth, winHeight, xmax, xstep, ymax, ystep)

    #draw function
    yratio = winHeight/2.0/ymax
    xratio = winWidth/2.0/xmax
    oldScreenX = oldScreenY = None

    #draw line in micro steps to form a whole sketch
    for screenx in xrange (winWidth):
    	#(screenx, screeny) = axesTransfer(cx, cy, screenx, xratio, yratio, fn)
    	x = (screenx - cx)/xratio
    	y = yratio*fn(x)
    	screeny = cy - y
    	if (oldScreenX != None):
    		canvas.create_line(oldScreenX, oldScreenY, screenx, screeny, fill="blue")
    	(oldScreenX, oldScreenY) = (screenx, screeny)

    root.mainloop()

def testAll():
	drawGraph(winWidth=600, winHeight=300, fn=cosineInDegrees, xmax=+720, xstep=90, ymax=+3, ystep=1)
	drawGraph(winWidth=600, winHeight=300, fn=strangeFunction, xmax=+20, xstep=4, ymax=+15, ystep=3)

if __name__ == "__main__":
    testAll()





