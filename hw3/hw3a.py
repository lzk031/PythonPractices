# hw3a.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################
def digitCount(n):
    #take in an integer
    #calculate the digit number of this integer
    #return the digit number
    count = 1
    n = abs(n)
    while(n/10 != 0):
        count += 1
        n /= 10
    return count

def kthDigit(n,k):
    n = abs(n)
    result = n / 10**k
    result %= 10
    return result

def fasterIsPrime(n):#frome course notes
    if (n == 2): return True
    if ((n < 2) or (n % 2 == 0)): return False
    for factor in xrange(3,int(round(n**0.5))+1,2):
        if (n % factor == 0): return False
    return True

def largestPrimeSubnumber(n):
    currentLPS = 0 #store largest prime subnumber up to now
    for startDigit in xrange(digitCount(n)): #starDigit is the highest digit of the subnumber
        for endDigit in xrange(startDigit + 1): #endDigit is the lowest digit of the subnumber
            subnumber = n % 10**(startDigit + 1) 
            subnumber /= 10**endDigit
            if (fasterIsPrime(subnumber)) and (subnumber > currentLPS):
                currentLPS = subnumber
    if currentLPS != 0:
        return currentLPS
    else:
        return None

def reverseDigit(n):
    #take an non-negative integer, reverse the integer and return it
    #take each digit of n from low to high one by one
    #every step, move each digit of reversedNumber upward one
    #and put the digit taken from n into ones digit of reversedNumber
    reversedNumber = 0
    for x in xrange(digitCount(n)):
        lowestDigit = n % 10
        n /= 10
        reversedNumber *= 10
        reversedNumber += lowestDigit    
    return reversedNumber

def isPalindromicNumber(n):
    #take a non-negative integer and 
    #check if it is equal to it's reversed number
    if n == reverseDigit(n):
        return True
    else:
        return False

def isLikelyLychrelNumber(n):
    #the function takes a positive integer of at least two digits 
    #and check if it is a likely lychrel number
    count = 0
    numberToBeChecked = n
    for x in xrange(50):
        numberToBeChecked += reverseDigit(numberToBeChecked)
        if ( isPalindromicNumber( numberToBeChecked ) ):
            return False
    return True
    
def nthLikelyLychrelNumber(n):
    count = 0
    #since 196 algorithm apply to positive integer of at least two digits
    #we check numbers start from 10
    #in first loop step, we do the 'guess += 1' before checking guess
    #so we initialize guess as 9
    guess = 9
    while(count<n+1):
        guess += 1
        if (isLikelyLychrelNumber(guess)):
            count += 1
    return guess


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import math
from Tkinter import *

def drawEuFlag(canvas,left,top,width,height):
    #draw a EU flag in the area bounded by top-left 
    #and botom-right(left+width,top+height)
    rhRatio = 20.0
    hRRatio = 0.3
    smallRadius = height / rhRatio #smallRadius is the radius of small yellow circles, 
    bigRadius = height * hRRatio #bigRadius refers to the big circle formed by 13 small circles

    #drwa the frame of flag
    canvas.create_rectangle(left,top,left + width,top + height,
                            fill='blue', outline='black',width=1.5)
    
    #draw the 13 small circles
    for x in xrange(13):
        angle = math.pi/2 - math.pi/6*x
        #angle refers to the angle between the positive vertical axes and 
        #the direction from big circle's center to small circle's center
        centerX = left + width/2.0 + bigRadius*math.cos(angle)
        centerY = top + height/2.0 - bigRadius*math.sin(angle)
        circleLeft = centerX - smallRadius
        circleTop = centerY - smallRadius
        circleRight = centerX + smallRadius
        circleBottom = centerY + smallRadius 
        canvas.create_oval(circleLeft,circleTop,circleRight,circleBottom,
                            fill='yellow',outline='black',width=1)

def drawBahamasFlag(canvas,left,top,width,height):
    #draw a Bahamas flag in the area bounded by top-left 
    #and botom-right(left+width,top+height)

    #draw the light blue background
    canvas.create_rectangle(left,top,left + width,top + height,fill='turquoise1', 
                            outline='black',width=1.5)

    #draw the yellow rectangle
    canvas.create_rectangle(left,top + height*0.33,left + width,top + height*0.67,
                            fill='yellow',outline='black',width=1.5)

    #draw the black triangle
    triangleAxis = left,top,left + 0.45*width,top + height/2.0,left,top + height
    canvas.create_polygon(triangleAxis,fill='black')


def drawTiledFlags(margin, rows, cols, flagWidth, flagHeight):
    root = Tk()
    width = 2*margin + cols*flagWidth
    height = 2*margin + rows*flagHeight
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    for i in xrange(rows):
        for j in xrange(cols):
            rectangleLeft = margin + j*flagWidth
            rectangleTop = margin + i*flagHeight
            if ((i+j)%2 == 0):
                drawEuFlag(canvas,rectangleLeft,
                            rectangleTop,flagWidth,flagHeight)
            else:
                drawBahamasFlag(canvas,rectangleLeft,
                                rectangleTop,flagWidth,flagHeight)
    root.mainloop()

def drawEachRow(canvas,left,top,lineWidth,lineHeight,measuresPerLine):
    #draw a blank sheet music row
    horizontaLinesNumber =5.0
    verticalDistance = lineHeight / (horizontaLinesNumber - 1)
    horizontalDistance = lineWidth / float(measuresPerLine)
    
    #draw horizontal lines
    for x in xrange(5):
        lineLeft = left
        lineTop = top + x*verticalDistance
        lineRight = left +lineWidth
        lineBottom = lineTop
        canvas.create_line(lineLeft,lineTop,lineRight,lineBottom)

    #draw vertical lines
    for x in xrange(measuresPerLine + 1):
        lineLeft =left + x*horizontalDistance
        lineTop = top
        lineRight = lineLeft
        lineBottom = top + lineHeight
        canvas.create_line(lineLeft,lineTop,lineRight,lineBottom)

def drawBlankSheetMusic(title, winWidth, winHeight,
                         lineHeight, lineMargin,
                         measuresPerLine):
    root = Tk()
    canvas = Canvas(root, width = winWidth, height = winHeight)
    canvas.pack()

    #draw title
    textCenterX = winWidth / 2 
    textCenterY = 25
    canvas.create_text(textCenterX, textCenterY, text = title, 
                        fill = 'black', font = 'arial 20 bold')

    #draw blanck sheet music that can fit in the window size
    maxRowsNumber = (winHeight - 50) / (lineHeight + lineMargin)
    #if the margin between window's bottom and the bottom edge of last sheet 
    #is just a little larger than lineHeight, draw a new sheet there
    if ((winHeight - 50) % (lineHeight + lineMargin) >= lineHeight):
       maxRowsNumber += 1 
    for x in xrange(maxRowsNumber):
        left = lineMargin
        top = 50 + x*(lineHeight + lineMargin)
        lineWidth = winWidth - 2*lineMargin
        drawEachRow(canvas,left,top,lineWidth,lineHeight,measuresPerLine)
    root.mainloop()


def testFasterIsPrime():
    print "Testing fasterIsPrime()...",
    assert (type(fasterIsPrime(2)) == bool)
    assert (fasterIsPrime(2) == True)
    assert (fasterIsPrime(191) == True)
    assert (fasterIsPrime(0) == False)
    assert (fasterIsPrime(380) == False)
    print "Passed!"

def testLargestPrimeSubnumber():
    print "Testing largestPrimeSubnumber()...",
    assert (largestPrimeSubnumber(2) == 2)
    assert (largestPrimeSubnumber(8112) == 811)
    assert (largestPrimeSubnumber(37731) == 773)
    print "Passed!"

def testResverseDigit():
    print "Testing reverseDigit()...",
    assert (reverseDigit(1) == 1)
    assert (reverseDigit(13) == 31)
    assert (reverseDigit(485) == 584)
    assert (reverseDigit(2365742365427354823) == 3284537245632475632)
    print "Passed!"

def testIsPalindromicNumber():
    print "Testing isPalindromicNumber...", 
    assert (isPalindromicNumber(4) == True)
    assert (isPalindromicNumber(21) == False)
    assert (isPalindromicNumber(23532) == True)
    assert (isPalindromicNumber(1166996611) == True)
    print "Passed!"

def testIsLikelyLychrelNumber():
    print "Testing isLikelyLychrelNumber...",
    assert (isLikelyLychrelNumber(196) == True)
    assert (isLikelyLychrelNumber(438) == False)
    assert (isLikelyLychrelNumber(2856) == True)
    assert (isLikelyLychrelNumber(3495) == True)
    print "Passed!"

def testNthLikelyLychrelNumber():
    print "Testing nthLikelyLychrelNumber...",
    assert (nthLikelyLychrelNumber(0)==196)
    assert (nthLikelyLychrelNumber(6)==691)
    assert (nthLikelyLychrelNumber(20)==1767)
    assert (nthLikelyLychrelNumber(30)==2674)
    print "Passed!"

def testAll():
    testFasterIsPrime()
    testLargestPrimeSubnumber()
    testResverseDigit()
    testIsPalindromicNumber()
    testIsLikelyLychrelNumber()
    testNthLikelyLychrelNumber()
    drawTiledFlags(margin=10, rows=3, cols=5, flagWidth=100, flagHeight=60)
    drawBlankSheetMusic(title="Blank sheet music", winWidth=800, winHeight=200,
                    lineHeight=50, lineMargin=20, measuresPerLine=5)

if __name__ == "__main__":
    testAll()