# hw6.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################
import time
import copy
import random
def swap(a, i, j):#from course notes
	(a[i], a[j]) = (a[j], a[i])

def instrumentedSelectionSort(a):#the codes about selection sort is based on course notes
	startTime = time.time()
	comparisons = 0
	swaps = 0
	n = len(a)
	for startIndex in xrange(n):
		minIndex = startIndex
		for i in xrange(startIndex, n):
			comparisons += 1
			if (a[i] < a[minIndex]):
				minIndex = i
		swap(a, startIndex, minIndex)
		swaps += 1
	endTime = time.time()
	timeUsed = endTime - startTime
	return (comparisons, swaps, timeUsed)

def instrumentedBubbleSort(a):#codes about bubble sort is based on course notes
	startTime = time.time()
	n = len(a)
	end = n
	swapped = True
	comparisons = 0
	swaps = 0
	while (swapped):
		swapped = False
		for i in xrange(1, end):
			comparisons += 1
			if (a[i-1] > a[i]):
				swap(a, i-1, i)
				swaps += 1
				swapped = True
		end -= 1
	endTime = time.time()
	timeUsed = endTime - startTime
	return (comparisons, swaps, timeUsed)

def largestSumOfPairs(a):
	if len(a) < 2:
		return None
	for i in xrange(len(a)):
		if a[i] > a[-1]:
			swap(a, i, len(a)-1)
	largest = a.pop()
	for i in xrange(len(a)):
		if a[i] > a[-1]:
			swap(a, i, len(a)-1)
	secondLarge = a.pop()
	return secondLarge+largest

def hasBalancedParentheses(s):
	count = 0
	n = len(s)
	for i in xrange(n):
		if s[i] == "(":
			count += 1
		else:
			count -= 1
		if count < 0:
			return False
		if count == 0 and i<n-1:
			return False
	if count != 0:
		return False
	return True

def isInList(sumOfSquare, square):
	#this function take a list sumOfSquare 
	#and a number square, check if square 
	#is in sumOfSquare By using binary search
	start = 0
	end = len(sumOfSquare) - 1
	i = 0
	while start <= end:
		i = i + 1
		mid = (start+end) / 2
		if square == sumOfSquare[mid]:          
			return True
		else:
			if square < sumOfSquare[mid]:
				end = mid -1
			else:
				start = mid + 1       
	return False

def containsPythagoreanTriple(a):
	n = len(a)
	square = [None]*n
	for i in xrange(n):
		square[i] = a[i]*a[i]
	sumOfSquare = []
	for i in xrange (n):
		for j in xrange(i+1,n):
			sumOfSquare += [square[i]+square[j]]
	sumOfSquare.sort()
	for item in square:
		if isInList(sumOfSquare,item):
			return True
	return False

def fasterIsPrime(n):#frome course notes
    if (n == 2): return True
    if ((n < 2) or (n % 2 == 0)): return False
    for factor in xrange(3,int(round(n**0.5))+1,2):
        if (n % factor == 0): return False
    return True

def nthCarolPrime(n):
	count = 0
	k = 1
	while(True):
		carolNumber = (2**k-1)**2-2
		k += 1
		if fasterIsPrime(carolNumber):
			if count == n:
				return carolNumber
			count += 1

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

def isKaprekarNumber(n):
#the function take a non-negative number and
#return True if it is a kaprekar number
#otherwise, return False
	square = n*n
	digits = digitCount(square)
	for x in xrange(1,digits+1):
		left = square/10**x
		right = square%10**x
		if right != 0 and (left+right)==n:
			return True
	return False

def nearestKaprekarNumber(n):
	#we start from the given number n
	#check if the number near it
	#is kaprekar number
	#we first check the number shift less
	#then n, then check the number
	#shift larger than n
	shift = 0
	while(True):
		guess = n - shift
		if isKaprekarNumber(guess):
			return guess
		guess = n + shift
		if isKaprekarNumber(guess):
			return guess
		shift += 1


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import time
import random
import copy

def getRandomList(n):
	#this number generate a random list
	#consists of n numbers
	#the elements is from 0 to n-1 inclusively
	#one number will not appear twice
	randomList = range(n)
	random.shuffle(randomList)
	return randomList

def selectionSortVersusBubbleSort():
	for i in xrange(1,5):
		maxNumber = i*500
		randomList = getRandomList(maxNumber);
		randomListCopy = copy.copy(randomList)
		selectionSort = instrumentedSelectionSort(randomList)
		bubbleSort = instrumentedBubbleSort(randomListCopy)
		print "for the same list of %d random numbers: " % maxNumber
		print "selection sort uses %d comparisons, %d swaps, %f seconds" % selectionSort
		print "bubble sort uses %d comparisons, %d swaps, %f seconds\n" % bubbleSort
	print """based on the results printed above, we can conclude that 
1. when len(randomList) multiply a factor k,
the time used of the same sort methods will multiply k square.
So, both selection sort and bubble sort are quadratic (O(n**2))"""
	print "2.selection sort runs in less time"
	print "3.bubble sort uses fewer comparisons"
	print "4.selection sort uses fewer swaps"

def merge(a, start1, start2, end):
	#from course notes
	index1 = start1
	index2 = start2
	length = end - start1
	aux = [None] * length
	for i in xrange(length):
		if (index1 == start2):
			aux[i] = a[index2]
			index2 += 1
		elif (index2 == end):
			aux[i] = a[index1]
			index1 += 1
		elif (a[index1] < a[index2]):
			aux[i] = a[index1]
			index1 += 1
		else:
			aux[i] = a[index2]
			index2 += 1
	for i in xrange(start1, end):
		a[i] = aux[i - start1]

def mergeSort(a):
	#from course notes
	n = len(a)
	step = 1
	while (step<n):
		for start1 in xrange(0, n, 2*step):
			start2 = min(start1 + step, n)
			end = min(start1 + 2*step, n)
			merge(a, start1, start2, end)
		step *= 2

def mergeWithOneAuxList(aux, a, start1, start2, end):
	index1 = start1
	index2 = start2
	length = end - start1
	for i in xrange(length):
		if (index1 == start2):
			aux[start1+i] = a[index2]
			index2 += 1
		elif (index2 == end):
			aux[start1+i] = a[index1]
			index1 += 1
		elif (a[index1] < a[index2]):
			aux[start1+i] = a[index1]
			index1 += 1
		else:
			aux[start1+i] = a[index2]
			index2 += 1

def mergeSortWithOneAuxList(a):
	#we used the test function below to
	#compare two fuction
	#as a result, the elapesd time of 
	#the two function are similar
	#it is not worthwhile to make the change
	aux = [None]*len(a)
	n = len(a)
	step = 1
	while (step < n):
		for start1 in xrange(0, n, 2*step):
			start2 = min(start1 + step, n)
			end = min(start1 + 2*step, n)
			mergeWithOneAuxList(aux, a, start1, start2, end)
		for i in xrange(len(a)):
			a[i] = aux[i]
		step *= 2

def testSort(sortFn, n, a):#based on course notes
    sortedA = sorted(a)
    startTime = time.time()
    sortFn(a)
    endTime = time.time()
    elapsedTime = endTime - startTime
    assert(a == sortedA)
    print "%20s n=%d  time=%6.3fs" % (sortFn.__name__, n, elapsedTime)

def compareMergeSortWitnOneAuxlistToOriginalOne():
	print "compare mergeSortWithOneAuxList with the original one..."
	for i in xrange(1,5):
		n=2**10*i	
		a = [random.randint(0,2**31) for i in xrange(n)]
		b = copy.copy(a)
		testSort(mergeSortWithOneAuxList, n, a)
		testSort(mergeSort, n, b)



from basicAnimation import BasicAnimationRunner 
from Tkinter import *
def getRandom(n):
	#this number generate a random list
	#consists of n numbers
	#the elements is from 1 to n inclusively
	#one number will not appear twice
	randomList = range(1,n+1)
	random.shuffle(randomList)
	return randomList

def initialBackground(canvas):
	#draw a panel where charts exists
	(left, top, right, bottom) = (20, 20, 476, 320)
	canvas.create_rectangle(left, top, right, bottom, 
							fill="Light Sky Blue", outline="blue")
	(textx,texty) = (20, 380)
	text = "type 's' to step in, type 'r' to restart bubble sort"
	canvas.create_text(textx, texty, text=text, 
						anchor = NW,fill="red", font="arial 16")
	#draw a title "bubble sort"
	(cx,cy)=(570, 70)
	canvas.create_text(cx, cy, text='Bubble sort', font='arial 20 bold')

def drawChart(canvas, randomList, phase, step, finished):
	#draw the chart given the randomlist
	(startX,startY) = (28, 200)
	(xUnit, yUnit, xDistance) = (20, 10, 8)
	maxItem = 16
	upToIndex = maxItem-phase+1#is the minum index of chart that is black
	for i in xrange(len(randomList)):
		(x1,y1) = (startX+i*xUnit+i*xDistance, startY)
		(x2,y2) = (x1+xUnit, y1-yUnit*randomList[i])
		if i < upToIndex:
			color = 'Dark Slate Gray'
		else :
			color = 'black'
		#if finished, all the chart is black
		if finished:
			color = 'black'
		canvas.create_rectangle(x1, y1, x2, y2, fill=color)
		yShift = 10
		(lableX,lableY) = ((x1+x2)/2, startY + yShift)
		text = "%d" % (i+1)
		canvas.create_text(lableX, lableY, text=text, fill='blue', font='axial 12')

def drawComments(canvas, phase, step, listToSort,
					finished,comparisons,copies,swapState):
	#this function draw indicationg comments in the bottom of the window
	comments = "Phase %d: Largest itmes bubbles up to position %d\n" 
	comments = comments % (phase, len(listToSort)-phase+1)
	#if step ==1, don't add comparing comments
	#if step>1, add comparing comments and compare result
	#when drawing comments, also do compare and copy
	#and add 1 to comparisons and copies in some cases
	if step > 1 and not finished:
		comments += "Is item %d bigger than item %d? " % (step-1,step)
		comparisons += 1
		if listToSort[step-2]<=listToSort[step-1]:
			comments += "No, so don't swap them"
			swapState += [False]
		else:
			comments += "Yes, so we swapped them"
			swap(listToSort, step-2, step-1)
			swapState += [True]
			copies += 1
	#in the begining, step = 0, pringt starting comments
	if step==0 and not finished:
		comments = "Press 's' to start sort"
	#if finished, print finishing comments
	if finished:
		comments = "The sort is finished "
	(commentsLeft, commentsTop) = (20, 340)
	canvas.create_text(commentsLeft, commentsTop, text=comments, anchor = NW,
						fill="Light Sea Green", font="arial 16")
	return (comparisons, copies)

def drawCompareFrame(canvas, index):
	#when swapping two items, draw red frame around 
	#the grey chart
	(startX,startY) = (28, 200)
	(xUnit, yUnit, xDistance) = (20, 10, 8)
	i = index
	yHeight = 180
	outlineWidth = 2
	(x1,y1) = (startX+i*xUnit+i*xDistance-outlineWidth, startY+outlineWidth)
	(x2,y2) = (x1+xUnit+2*outlineWidth, y1-yHeight)
	canvas.create_line(x1, y1, x1, y2, fill='red')
	canvas.create_line(x1, y2, x2, y2, fill='red')
	canvas.create_line(x2, y2, x2, y1, fill='red')
	canvas.create_line(x2, y1, x1, y1, fill='red')


def doBubbleSort(canvas,listToSort,step,finished,comparisons,copies,swapState):
	#this fucntion take in step and make the change of
	#listTosort, comparisons, copies and finished

	#given the steps now, we should
	#calculate which step and which phase
	#we are in
	#in each phase, the first step just tell us
	#entering a new phase, not do compare and copy
	phaseStep = len(listToSort)
	phase = 1
	while step > phaseStep and phase<=15:
		step -= phaseStep
		phaseStep -= 1
		phase += 1
	#in some extreme case, if phase goes to 16, 
	#the sort will be finished
	if phase >= 16: finished = True

	#in the first step of each phase,
	#update swapState
	if step == 1:
		swapState = []

	#draw indicating comments in the window
	(comparisons, copies) = drawComments(canvas, phase, step, listToSort,
										finished,comparisons,copies,swapState)
	#if the current list is well sorted, the sort is finished
	if step == phaseStep and swapState.count(True)==0:
		finished = True
	#in comparing steps, draw swap frame
	if not finished and step>1:
		drawCompareFrame(canvas,step-2)
		drawCompareFrame(canvas,step-1)
	return (phase,finished,comparisons,copies,swapState)

def drawCompareCopy(canvas, comparisons, copies):
	#take in comparisons and copies
	#show them in the window

	#first, create a panel
	(left, top, width, height)=(490, 120, 160, 200)
	canvas.create_rectangle(left, top, left+width, top+height, 
							fill='Light Steel Blue')
	#show comparisons
	offsetY = 30
	(comX, comY) = (left+width/2, top+offsetY)
	canvas.create_text(comX, comY, text="Comparisons:", font='arial 20')
	(comNumX, comNumY) = (left+width/2, top+height/2-offsetY)
	comNum = "%d" % comparisons
	canvas.create_text(comNumX, comNumY, text=comNum, font='arial 16')
	#show copies
	(copX, copY) = (left+width/2, top+height/2+offsetY)
	canvas.create_text(copX, copY, text="Copies:", font='arial 20')
	(copNumX, copNumY) = (left+width/2, top+height-offsetY)
	copNum = "%d" % copies
	canvas.create_text(copNumX, copNumY, text=copNum, font='arial 16')

def bubblesortSimulator(app, canvas):
	(comparisons, copies, step, phase) = (0,0,0,1)
	#step and phase indicate which step
	#in which phase we are in
	listToSort = getRandom(16)
	swapState = []
	#in each phase, we will have a swapState
	#which indicate if there is a swap in each step
	#if there is, the element in swapState will be True
	#False otherwise

	finished = False #if the sort is finished, it will turn True

	while app.isRunning():
		(eventType, event) = app.getEvent()
		if (eventType == "keyPressed"):
			if (event.char == 's')and not finished:
				step += 1
			elif (event.char == 'r'):
				(step, phase) = (0, 1)
				listToSort = getRandom(16)
				finished = False
				(comparisons,copies) = (0, 0)
		canvas.delete(ALL)
		initialBackground(canvas)
		#when the sort is finished
		#we use the comTemp to store curren comparisons
		#so that comparisons will not change any more
		comTemp = comparisons
		(phase,finished,comparisons,copies,swapState) = doBubbleSort(canvas,listToSort,step,
															finished,comparisons,copies,swapState)
		if finished: 
			comparisons = comTemp
		drawChart(canvas, listToSort, phase, step, finished)
		if finished: drawCompareCopy(canvas, comparisons+1, copies)
		else: drawCompareCopy(canvas, comparisons, copies)


def testInstrumentedSelectionSort():
	print "Testing instrumentedSelectionSort()...",
	assert (instrumentedSelectionSort([3,2,1])[0:2] == (6,3))
	assert (instrumentedSelectionSort([23,52,5,7,2])[0:2] == (15,5))
	assert (instrumentedSelectionSort([6,5,4,3,2,1])[0:2] == (21,6))
	print "Passed!"

def testInstrumentedBubbleSort():
	print "Testing instrumentedBubbleSort()...",
	assert (instrumentedBubbleSort([3,2,1])[0:2] == (3,3))
	assert (instrumentedBubbleSort([23,52,5,7,2])[0:2] == (10,8))
	assert (instrumentedBubbleSort([6,5,4,3,2,1])[0:2] == (15,15))
	print "Passed!"

def testLargestSumOfPairs():
	print "Testing largestSumOfPairs()...",
	assert (largestSumOfPairs([3,4,5,6,2,6]) == 12)
	assert (largestSumOfPairs([3]) == None)
	assert (largestSumOfPairs([]) == None)
	assert (largestSumOfPairs([233544563,239423472,345435895,234323,435432]) == 584859367)
	print "Passed!"

def testContainsPythagoreanTriple():
	print "Testing containsPythagoreanTriple()...",
	assert (containsPythagoreanTriple([3,4,5,6,3,7,2]) == True)
	assert (containsPythagoreanTriple([1,2,3,4,6]) == False)
	assert (containsPythagoreanTriple([354234,232,345,1,6]) == False)
	assert (containsPythagoreanTriple([3,5,6,72,8,34,10,9,52,52,974,256,37294]) == True)
	print "Passed!"

def testHasBalancedParentheses():
	print "Testing hasBalancedParentheses()...",
	assert (hasBalancedParentheses("())") == False)
	assert (hasBalancedParentheses("()(") == False)
	assert (hasBalancedParentheses(")(") == False)
	assert (hasBalancedParentheses("(()())") == True)
	assert (hasBalancedParentheses("(())()") == False)
	print "Passed!"

def testDigitCount():
    print "Testing digitCount()...",
    assert (digitCount(23)==2)
    assert (digitCount(0)==1)
    assert (digitCount(23479845)==8)
    print "Passed!"

def testIsKaprekarNumber():
	print "Testing isKaprekarNumber()...",
	assert (isKaprekarNumber(1)==True)
	assert (isKaprekarNumber(2728)==True)
	assert (isKaprekarNumber(45)==True)
	assert (isKaprekarNumber(458)==False)
	print "Passed!"

def testNearestKaprekarNumber():
	print "Testing nearestKaprekarNumber()...",
	assert (nearestKaprekarNumber(3)==1)
	assert (nearestKaprekarNumber(50)==45)
	assert (nearestKaprekarNumber(554)==703)
	assert (nearestKaprekarNumber(302)==297)
	print "Passed!"

def testFasterIsPrime():
    print "Testing fasterIsPrime()...",
    assert (fasterIsPrime(2) == True)
    assert (fasterIsPrime(191) == True)
    assert (fasterIsPrime(0) == False)
    assert (fasterIsPrime(380) == False)
    print "Passed!"

def testNthCarolPrime():
	print "Testing nthCarolPrime()...",
	assert (nthCarolPrime(0) == 7)
	assert (nthCarolPrime(3) == 3967)
	assert (nthCarolPrime(5) == 1046527)
	assert (nthCarolPrime(9) == 274876858367)
	print "Passed!"

 
def testAll():
	testInstrumentedSelectionSort()
	testInstrumentedBubbleSort()
	selectionSortVersusBubbleSort()
	compareMergeSortWitnOneAuxlistToOriginalOne()
	testLargestSumOfPairs()
	testContainsPythagoreanTriple()
	testHasBalancedParentheses()
 	testDigitCount()
 	testIsKaprekarNumber()
 	testNearestKaprekarNumber()
 	testFasterIsPrime()
 	testNthCarolPrime()
 	BasicAnimationRunner(bubblesortSimulator, width=650, height=400)

if __name__ == "__main__":
    testAll()


