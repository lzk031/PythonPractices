# hw9c.py
# Zekun Lyu + zlyu + R
# Xinyue Wu + xinyuew + I

######################################################################
# Place your autograded solutions below here
######################################################################
import copy
def sumOfSquaresOfDigits(n):
	if n<10: 
		return n*n
	else:
		digit = n%10
		return digit*digit + sumOfSquaresOfDigits(n/10)

def isHappyNumber(n):
	if n<=0:
		return False
	tempResult = sumOfSquaresOfDigits(n)
	if tempResult==4:
		return False
	elif tempResult==1:
		return True
	else:
		return isHappyNumber(tempResult)

def distanceToNextHappyNumber(n):
	if isHappyNumber(n):
		return 0
	else:
		return 1 + distanceToNextHappyNumber(n+1)

def nthHappyNumber(n):
	if n==0:
		return 1
	else:
		return nthHappyNumber(n-1) + \
				distanceToNextHappyNumber(nthHappyNumber(n-1)+1) + 1

def fasterIsPrime(n):
	# from course note
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = int(round(n**0.5))
    for factor in xrange(3,maxFactor+1,2):
        if (n % factor == 0):
            return False
    return True

def isHappyPrime(n):
	if isHappyNumber(n) and fasterIsPrime(n):
		return True
	else:
		return False

def distanceToNextHappyPrime(n):
	if isHappyPrime(n):
		return 0
	else:
		return 1 + distanceToNextHappyPrime(n+1)

def nthHappyPrime(n):
	if n == 0:
		return 7
	else:
		return nthHappyPrime(n-1) + \
				distanceToNextHappyPrime(nthHappyPrime(n-1)+1) + 1

def swap(a, i, j):
	# from course notes
	# take a list and swap the ith and jth item of it
    (a[i], a[j]) = (a[j], a[i])

def oneStepBubbleSort(a):
	result = copy.copy(a)
	if len(result)<=1:
		return result
	if result[0]>result[1]:
		swap(result, 0, 1)
	if len(result)==2:
		return result
	else:
		return result[0:1] + oneStepBubbleSort(result[1:])


def isSorted(a):
	if len(a)<=1:
		return True
	if len(a) == 2 and a[0]<=a[1]:
		return True
	else:
		return a[0]<=a[1] and isSorted(a[1:])

def bubbleSort(a):
	result = copy.copy(a)
	if isSorted(result):
		return result
	else:
		return bubbleSort(oneStepBubbleSort(a))

def isInCatalog(course, courseCatalog):
	if len(courseCatalog)==0:
		return False
	elif type(courseCatalog[0])==list:
		return isInCatalog(course, courseCatalog[0]) or\
				 isInCatalog(course, courseCatalog[1:])
	else:
		return (courseCatalog[0]==course) or \
				isInCatalog(course, courseCatalog[1:])


def getRawCourse(courseCatalog, course):
	if isInCatalog(course, courseCatalog):
		if course in courseCatalog:
			return "%s.%s" % (courseCatalog[0], course)
		else:
			if type(courseCatalog[0])==str:
				if len(courseCatalog[0])<3 or type(courseCatalog[0][2]!='-'): 
					return courseCatalog[0] + '.' + \
							getRawCourse(courseCatalog[1:], course)
				else:
					return ''
			else: 
				return getRawCourse(courseCatalog[0], course) + \
							getRawCourse(courseCatalog[1:], course)
	else: return ''
	"""if len(courseCatalog)==0:
		return "" 
	if isInCatalog(course, courseCatalog):
		if type(courseCatalog[0])==str:
			if len(courseCatalog[0])<3 or courseCatalog[0][2]!='-':
				return courseCatalog[0] + "." + \
						getRawCourse(courseCatalog[1:],course)
			elif courseCatalog[0] == course:
				return course
			else:
				return "" + getRawCourse(courseCatalog[1:], course)
		else:	
			return getRawCourse(courseCatalog[0], course) + \
					getRawCourse(courseCatalog[1:], course)
	else:
		return """""


def getCourse(courseCatalog, course):
	temp = getRawCourse(courseCatalog, course)
	if temp == "":
		return None
	else:
		return temp
	







######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testSumOfSquaresOfDigits():
	print "Testing sumOfSquaresOfDigits()...",
	assert(sumOfSquaresOfDigits(5) == 25)   # 5**2 = 25
	assert(sumOfSquaresOfDigits(12) == 5)   # 1**2 + 2**2 = 1+4 = 5
	assert(sumOfSquaresOfDigits(234) == 29) # 2**2 + 3**2 + 4**2 = 4 + 9 + 16 = 29
	print "Passed!"

def testIsHappyNumber():
	print "Testing isHappyNumber()...",
	assert(isHappyNumber(-7) == False)
	assert(isHappyNumber(1) == True)
	assert(isHappyNumber(2) == False)
	assert(isHappyNumber(97) == True)
	assert(isHappyNumber(98) == False)
	assert(isHappyNumber(404) == True)
	assert(isHappyNumber(405) == False)
	print "Passed!"

def testDistanceToNextHappyNumber():
	print "Testing distanceToNextHappyNumber()...",
	assert(distanceToNextHappyNumber(2)==5)
	assert(distanceToNextHappyNumber(10)==0)
	assert(distanceToNextHappyNumber(24)==4)
	print "Passed!"

def testNthHappyNumber():
	print "Testing nthHappyNumber()...",
	assert(nthHappyNumber(0) == 1)
	assert(nthHappyNumber(1) == 7)
	assert(nthHappyNumber(2) == 10)
	assert(nthHappyNumber(3) == 13)
	assert(nthHappyNumber(4) == 19)
	assert(nthHappyNumber(5) == 23)
	assert(nthHappyNumber(6) == 28)
	assert(nthHappyNumber(7) == 31)
	print "Passed!"

def testIsHappyPrime():
	print "Testing IsHappyPrime()...",
	assert(isHappyPrime(7) == True)
	assert(isHappyPrime(19) == True)
	assert(isHappyPrime(0) == False)
	assert(isHappyPrime(31) == True)
	assert(isHappyPrime(100234234231240) == False)
	print "Passed!"

def testFasterIsPrime():
	print "Testing fasterIsPrime()...",
	assert(fasterIsPrime(0)==False)
	assert(fasterIsPrime(1)==False)
	assert(fasterIsPrime(2)==True)
	assert(fasterIsPrime(97)==True)
	print "Passed!"

def testDistanceToNextHappyPrime():
	print "Testing distanceToNextHappyPrime()...",
	assert(distanceToNextHappyPrime(0)==7)
	assert(distanceToNextHappyPrime(13)==0)
	assert(distanceToNextHappyPrime(28)==3)
	print "Passed!"

def testNthHappyPrime():
	print "Testing nthHappyPrime()...",
	assert(nthHappyPrime(0) == 7)
	assert(nthHappyPrime(1) == 13)
	assert(nthHappyPrime(2) == 19)
	assert(nthHappyPrime(3) == 23)
	assert(nthHappyPrime(4) == 31)
	assert(nthHappyPrime(5) == 79)
	assert(nthHappyPrime(6) == 97)
	assert(nthHappyPrime(7) == 103)
	print "Passed!"

def testOneStepBubbleSort():
	print "Testing oneStepBubbleSort()...",
	assert(oneStepBubbleSort([5,4,3,2,1])==[4,3,2,1,5])
	assert(oneStepBubbleSort([5,23,6,8,2])==[5,6,8,2,23])
	assert(oneStepBubbleSort([1])==[1])
	assert(oneStepBubbleSort([2,1])==[1,2])
	print "Passed!"

def testIsSorted():
	print "Testing isSorted()...",
	assert(isSorted([])==True)
	assert(isSorted([42])==True)
	assert(isSorted([1,2,5,7,9,23,456])==True)
	assert(isSorted([1,2,3,4,5,6,3])==False)
	assert(isSorted([2,3,3,4,5,5,6])==True)
	print "Passed!"

def loadCatalog():
	courseCatalog = ["CMU",
						["CIT",
							[ "ECE", "18-100", "18-202", "18-213" ],
							[ "BME", "42-101", "42-201" ],
						],
						["SCS",
							[ "CS", 
								["Intro", "15-110", "15-112" ],
								"15-122", "15-150", "15-213"
							],
						],
						"99-307", "99-308"
					]
	return courseCatalog

def testIsInCatalog():
	courseCatalog = loadCatalog()
	print "Testing isInCatalog()...",
	assert(isInCatalog('15-112',courseCatalog)==True)
	assert(isInCatalog('99-307',courseCatalog)==True)
	assert(isInCatalog('18-100',courseCatalog)==True)
	assert(isInCatalog('15-251',courseCatalog)==False)
	print "Passed!"

def testGetScore():
	courseCatalog = loadCatalog()
	print "Testing getCourse()...",
	assert(getCourse(courseCatalog, "18-100") == "CMU.CIT.ECE.18-100")
	assert(getCourse(courseCatalog, "15-112") == "CMU.SCS.CS.Intro.15-112")
	assert(getCourse(courseCatalog, "15-213") == "CMU.SCS.CS.15-213")
	assert(getCourse(courseCatalog, "99-307") == "CMU.99-307")
	assert(getCourse(courseCatalog, "15-251") == None)
	print "Passed!"

def testAll():
	testSumOfSquaresOfDigits()
	testIsHappyNumber()
	testDistanceToNextHappyNumber()
	testNthHappyNumber()
	testFasterIsPrime()
	testIsHappyPrime()
	testDistanceToNextHappyPrime()
	testNthHappyPrime()
	testOneStepBubbleSort()
	testIsSorted()
	testIsInCatalog()
	testGetScore()

if __name__ == "__main__":
    testAll()