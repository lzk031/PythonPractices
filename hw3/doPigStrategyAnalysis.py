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
    print 'p1'
    currentScore = 0
    while currentScore < 20:
        p1Dice = doRoll()
        print 'dice:', p1Dice,
        if p1Dice == 1:
            currentScore = 0
            break
        else:
            currentScore += p1Dice
        if currentScore + p1Score >= 100:
            break
        print 'turn score', currentScore
    p1Score += currentScore
    return p1Score

def moveRandomly(p2Score):
    print 'p2'
    currentScore = 0
    while True:
    #determin Roll or Hold
        rOrH = doChoice()
        print 'r or h:', rOrH
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
        print 'turn score', currentScore
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
    print whoWin, 'win'
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
            
    
    
            
