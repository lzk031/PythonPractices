# hw5.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################

import copy
def nondestructiveRotateList(a,n):
	#result is the copy of a, so the a outside will not change
	result = copy.copy(a)
	#if result is a empty list, do nothing and return it back
	if result != []:
		#as n goes larger, output of the function will change periodicly
		#so we change n in to the minimal range to consider the problem
		n = n%len(a)

		#if n is positive, we move each elment of the list right n times 
		if n > 0:
			for x in xrange(n):
				temp = result.pop(len(result)-1)
				result.insert(0,temp)
		#if n is negative, we move each elment of the list left n times 
		#if n = 0, we do nothing and return the oringinal list
		elif n < 0:
			for x in xrange(-n):
				temp = result.pop(0)
				result.insert(len(result)-2,temp)	
	return result


def destructiveRotateList(a,n):
	#the following codes are similar to codes of the first question
	#to do in a destructive way, we do not copy original list
	if a != []:
		n = n%len(a)
		if n > 0:
			for x in xrange(n):
				temp = a.pop(len(a)-1)
				a.insert(0,temp)
		elif n < 0:
			for x in xrange(-n):
				temp = a.pop(0)
				a.insert(len(a)-2,temp)


def getHistogram(a, rangeList):
	#this function take the score list and 
	#a list of score range. in range list,
	#each element stand for the start point of range,
	#for example: 60 stand for '60-69' 
	strOutput = ''

	#create a list called count which store the number
	#of scores in a certain range
	count = [0]*len(rangeList)

	#check how many score score list have in each range
	for score in a:
		#in most cases except when score=100, rang is 
		#the start of the range the score belongs to
		rang = score / 10 * 10 #a score's rang is the range where the score lies in

		#rang==100 means the score is 100
		#in this case, '90++' must relate to the last element of count
		if rang == 100:
			count[-1] += 1

		#in other cases, we first find the index of rang in rangeList
		#then add the number stored in the same index of count list
		else:
			count[rangeList.index(rang)] += 1

	#according to the count list we get above
	#create the output string
	for i in xrange(len(rangeList)):
		start = rangeList[i]
		if start != 90:
			end = start + 9
			if start != 0: strOutput += '%d-%d:'%(start, end)
			else : strOutput += '00-09:'
		else :
			strOutput += '90++ :'
		if count[i] != 0: strOutput += ' '
		strOutput = strOutput + '*'*count[i] + '\n'
	return strOutput


def histogram(a):
	a = copy.copy(a)
	#find the highest and lowest range
	#we assume start number of the range
	#stand for this range, we store these 
	#elements in rangeList
	lowestRange = min(a)/10*10
	highestRange = max(a)/10*10
	if lowestRange == 100:
		lowestRange = 90
	if highestRange == 100:
		highestRange = 90
	rangeList = list()
	#generate rangeList
	for x in xrange(lowestRange,highestRange+1,10):
		rangeList.append(x)
	return getHistogram(a,rangeList)


def lookAndSay(a):
	if a == []:
		return []
	result = list()
	count = 0 #count the number of the current consecutive row
	digitNow = None #the number counted now
	for number in a:
		if digitNow == None: #we find a number in the first time
			digitNow = number
			count += 1
		elif number == digitNow: #each time that digitNow doesn't change, add the count number
			count += 1

		#each time we come to a new number, store the number and it's frequence
		else:
			numberTuple = (count, digitNow) 
			result.append(numberTuple)
			digitNow = number
			count = 1

	#for the last number, we didn't store it's information in the loop
	#so do it here
	numberTuple = (count, digitNow)
	result.append(numberTuple)
	return result

def inverseLookAndSay(a):
	result = []
	for tupl in a:
		count = tupl[0]
		digit = tupl[1]
		result += [digit]*count
	return result

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
from Tkinter import *
from basicAnimation import BasicAnimationRunner
import string

def displayTittle(canvas, width):
	#this function display the title for superSimpleCalculator
	(titleX, titleY) = (width/2, 10)
	canvas.create_text(titleX, titleY, text='superSimpleCalculator', font='Arial 12 bold')
	subTitle = """Enter Simple arithmetic expression.
Such as: 123+45=
Illegal chars --> red output.
Correct typos with BackSpace"""
	startY = 25
	yUnit = 16
	i = 0
	for line in subTitle.splitlines():
		(lineX,lineY) = (width/2, startY + i*yUnit)
		canvas.create_text(lineX, lineY, text=line, font='Arial 15')
		i += 1

def doType(char, equation, color, calculateState):
	#this function take in the current equation and input character in each loop
	#and return color, updated equation and updated calculateState
	#legal = string.digits + string.punctuation + string.whitespace
	legal = "0123456789()+-*/% \n\t"
	if legal.find(char) != -1: #means that the char is legal
		color = 'blue'
		#if the equation hasn't been calculated, add char to it
		if not calculateState: 
			equation += char

		#if the current current equation has been calculated
		#update equation with char, update calculatestate
		else:
			equation = char
			calculateState = False
	#when char equal '=' calculate it if it hasn't been done
	elif char == '=':
		if not calculateState:
			color = 'blue'
			#if there is a error, the equation equal to 'error'
			try:
				result = str(eval(equation))
			except:
				result = 'error'
			equation = equation + " = " + result
			calculateState = True

	#illegal input change color to red
	else: color = 'red'
	return (equation, color, calculateState)

def superSimpleCalculator(app, canvas):
	color = 'blue'
	equation = ''
	calculateState = False#indicate if the equation now has been calculated
	while app.isRunning():
		(eventType, event) = app.getEvent()
		if (eventType == "keyPressed"):
			if event.keysym == "BackSpace":
				if not calculateState:
					equation = equation[0:len(equation)-1]
					color = 'blue'
				else:
					equation=''
					calculateState = False
			else:
				char = event.char
				(equation,color,calculateState) = doType(char,equation,color,calculateState)
		canvas.delete(ALL)
		displayTittle(canvas, app.width)
		(equationX,equationY) = (app.width/2,125)
		canvas.create_text(equationX, equationY, text=equation, font='Arial 20', fill=color)


BasicAnimationRunner(superSimpleCalculator, width=400, height=150)


def drawPolygon(canvas, points, currentIndex):
	radius = 5
	leftIndexBound = -1
	if len(points)!=0 and currentIndex > leftIndexBound:
		points = points[0:currentIndex+1]
		for axis in points:
			x = axis[0]
			y = axis[1]
			canvas.create_oval(x-radius, y-radius, x+radius, 
								y+radius, fill='orange', outline='black')
		for i in xrange(len(points)-1):
			canvas.create_line(points[i],points[i+1])
		canvas.create_line(points[-1],points[0])


def visualizeTittle(canvas, width):
	#diplay tittle
	(titleX, titleY) = (width/2, 15)
	canvas.create_text(titleX, titleY, text='drawPolygonPointsWithUndoRedo', font='Arial 12 bold')
	subTitle = """Click mouse to add a point.
u = Undo move(s)  r = Redo move(s)"""
	(startY,yUnit,i) = (30,16,0)
	for line in subTitle.splitlines():
		(lineX,lineY) = (width/2, startY + i*yUnit)
		canvas.create_text(lineX, lineY, text=line, font='Arial 15')
		i += 1


def drawPolygonPointsWithUndoRedo(app, canvas):
	points = [] #store tops of the polygon(the number may be larger than those will be displayed)
	currentIndex = -1 #this index relate to the last point of polygon displayed, start count from 0
	while app.isRunning():
		(eventType, event) = app.getEvent()
		#each time click mouse, add a new point and make currentindex plus 1
		if (eventType == "mousePressed"):
			(x,y) = (event.x, event.y)
			points = points[0:currentIndex+1]
			points.append((x,y))
			currentIndex += 1

		elif (eventType == "keyPressed"):
			#input r, if currentindex is the last index, do nothing
			#if not, plus 1
			if (event.char == 'r') and (currentIndex < len(points)-1):
				currentIndex += 1

			#input u, if currentindex is the first index, do nothing
			#if not, minus 1
			if (event.char == 'u') and (currentIndex > -1):
				currentIndex -= 1
		canvas.delete(ALL)
		visualizeTittle(canvas, app.width)
		drawPolygon(canvas, points, currentIndex)

BasicAnimationRunner(drawPolygonPointsWithUndoRedo, width=300, height=320)

def testNondestructiveRotateList():
	print "Testing nondestructiveRotateList()...",
	assert (nondestructiveRotateList([1,2,3,4], 1)==[4,1,2,3])
	assert (nondestructiveRotateList([4,3,2,6,5], 2)==[6,5,4,3,2])
	assert (nondestructiveRotateList([1,2,3], 0)==[1,2,3])
	assert (nondestructiveRotateList([1, 2, 3], -1)==[2,3,1])
	print "Passed!"

def testDestructiveRotateList():
	print "Testing destructiveRotateList()...",
	a=[1,2,3,4]
	destructiveRotateList(a, 1)
	assert (a==[4,1,2,3])
	a=[4,3,2,6,5]
	destructiveRotateList(a,2)
	assert(a==[6,5,4,3,2])
	a=[1,2,3]
	destructiveRotateList(a,0)
	assert (a==[1,2,3])
	a=[1,2,3]
	destructiveRotateList(a, -1)
	assert (a==[2,3,1])
	print "Passed!"

def testGetHistogram():
	print "Testing getHistogram()...",
	assert (getHistogram([45,60,70],[40,50,60,70]) == """40-49: *
50-59:
60-69: *
70-79: *
""")
	assert (getHistogram([45,57,64,44],[40,50,60,70]) == """40-49: **
50-59: *
60-69: *
70-79:
""")
	print "Passed!"

def testHistogram():
	print "Testing histogram()...",
	assert (histogram([100],) == """90++ : *
""")
	assert (histogram([73, 62, 91, 74, 100, 77])=="""\
60-69: *
70-79: ***
80-89:
90++ : **
""")
	assert (histogram([45,60,70]) == """40-49: *
50-59:
60-69: *
70-79: *
""")
	print "Passed!"	

def testLookAndSay():
	print "Testing lookAndSay()...",
	assert (lookAndSay([]) == [])
	assert (lookAndSay([1,1,1]) == [(3,1)])
	assert (lookAndSay([-1,2,7]) == [(1,-1),(1,2),(1,7)])
	assert (lookAndSay([3,3,8,-10,-10,-10]) == [(2,3),(1,8),(3,-10)])
	print "Passed!"

def testInverseLookAndSay():
	print "Testing inverseLookAndSay()...",
	assert (inverseLookAndSay([]) == [])
	assert (inverseLookAndSay([(3,1)]) == [1,1,1])
	assert (inverseLookAndSay([(1,-1),(1,2),(1,7)]) == [-1,2,7])
	assert (inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
	print "Passed!"

def testAll():
	testDestructiveRotateList()
	testNondestructiveRotateList()
	testGetHistogram()
	testHistogram()
	testLookAndSay()
	testInverseLookAndSay()

if __name__ == "__main__":
    testAll()

