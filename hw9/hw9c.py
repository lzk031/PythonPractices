# hw9c.py
# Zekun Lyu + zlyu + R
# Xinyue Wu + xinyuew + I

######################################################################
# Place your autograded solutions below here
######################################################################
import copy
def sumOfSquaresOfDigits(n):
	# the function take in a number and return the sum of 
	# the squares of its digits

	# base case: when n<10, return the suqare of n
	if n<10: 
		return n*n

	# recursive case: if calculate the one digit's square
	# and add the sum of squares of digits of n/10
	else:
		digit = n%10
		return digit*digit + sumOfSquaresOfDigits(n/10)

def isHappyNumber(n):
	# base case: if n is non-positive, return False
	# if the sum of squares of idgits of n equals to 4, return False
	# if it equals to 1, return True
	if n<=0:
		return False
	tempResult = sumOfSquaresOfDigits(n)
	if tempResult==4:
		return False
	elif tempResult==1:
		return True
	# recursive case: check if the tempResult is a happy number
	else:
		return isHappyNumber(tempResult)

def nthHappyNumber(n, count=-1, found=0):
	# when we firstly call this function,
	# just set count=-1, and found=0 by default
	# in each recursive call of this function
	# we first check if the found is a happy number
	# if so, count+=1, and we also call nthHappyNumber
	# in the body of function in recursive case after adding 1 to found
	# the base case is: if count equals to n, we find nth number and
	# return current found
	if isHappyNumber(found):
		count += 1
	if count==n:
		return found
	else:
		return nthHappyNumber(n, count, found+1)


def fasterIsPrime(n, factor=3):
	# 0, 1 are not prime, 2 is prime
	if (n < 2):
		return False
	if n == 2:
		return True
	# even number are not prime
	if (n % 2 == 0):
		return False

	# base case: if factor arrive max value
	# return True if it can't divide n, otherwise return False
	if factor == int(round(n**0.5)) or factor == int(round(n**0.5))-1:
		return (n % factor!=0)

	# recursive case: if facter doesn't divide n and neither does
	# factors larger than current factor, return True
	# if not, return False
	else:
		return (n % factor!=0) and fasterIsPrime(n, factor+2)

def isHappyPrime(n):
	# return True if n is both happy number and prime
	# if not, return False
	if isHappyNumber(n) and fasterIsPrime(n):
		return True
	else:
		return False

def nthHappyPrime(n, count=-1, found=0):
	# when we firstly call this function,
	# just set count=-1, and found=0 by default
	# in each recursive call of this function
	# we first check if the found is a happy number
	# if so, count+=1, and we also call nthHappyNumber
	# in the body of function in recursive case after adding 1 to found
	# the base case is: if count equals to n, we find nth number and
	# return current found
	if isHappyPrime(found):
		count += 1
	if count==n:
		return found
	else:
		return nthHappyPrime(n, count, found+1)


def isInCatalog(course, courseCatalog):
	# this function take a coruse and check if it is
	# in the courseCatalog also taken by the function
	# base case: courseCatalog is empty, return False
	if len(courseCatalog)==0:
		return False
	# recursive case: if the first element is
	# list, go into it to look for course until there is
	# no element
	elif type(courseCatalog[0])==list:
		return isInCatalog(course, courseCatalog[0]) or\
				 isInCatalog(course, courseCatalog[1:])
	# if the first element is a string, check if it is
	# the course we are looking for and go on to check 
	# the rest of the list
	else:
		return (courseCatalog[0]==course) or \
				isInCatalog(course, courseCatalog[1:])


def getRawCourse(courseCatalog, course):
	# this take course and courseCatalog, return the correct
	# result as expected and return a empty string otherwise

	# base case: if the list is empty, return ""
	if len(courseCatalog)==0:
		return ""
	# if the list contains the course, go to find the course
	# if not, return "" 
	if isInCatalog(course, courseCatalog):
		if type(courseCatalog[0])==str:
			# if we find the course, return it and stop recursion
			if courseCatalog[0] == course:
				return course
			# if the string is not the course we are looking for
			# go on resursion in the rest of the current list
			else:
				return getRawCourse(courseCatalog[1:], course)
		# if the first element is a list, go into it to find the
		# course and go back to recurse in the rest of the basic level list
		else:
			if isInCatalog(course, courseCatalog[0]):
				return courseCatalog[0][0] + '.' + \
						getRawCourse(courseCatalog[0], course) + \
						getRawCourse(courseCatalog[1:], course)
			else:
				return getRawCourse(courseCatalog[1:], course)
	else:
		return ""

def getCourse(courseCatalog, course):
	# this function take in courseCatalog and, if the course is 
	# in the courseCatalog, add the first tittle at the start of the result
	# of getRawCourse. If it is not in courseCatalog, that is to say,
	# when the result of getRawCourse is empty string, return None
	temp = getRawCourse(courseCatalog, course)
	if temp == "":
		return None
	else:
		return courseCatalog[0] + '.' + temp



######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
import random

def swap(a, i, j):
	# from course notes
	# take a list and swap the ith and jth item of it
    (a[i], a[j]) = (a[j], a[i])

def oneStepBubbleSort(a):
	# this function do one step in bubble sort
	# that is to say, it take a list a
	# and check each pair of adjacent numbers
	# and swap them if larger number comes first
	result = copy.copy(a)
	# base case: if length of list is less than or equal 1
	# return the original list
	if len(result)<=1:
		return result
	# each time check the first two elements of 
	# list and sort them by swapping if necessary
	if result[0]>result[1]:
		swap(result, 0, 1)
	# base case: length is 2 and return it after sorting
	if len(result)==2:
		return result
	# recursive case: return the first element and
	# plus the left list after one step bubble sort
	else:
		return result[0:1] + oneStepBubbleSort(result[1:])


def isSorted(a):
	# this function take a list and check
	# if it is well sorted

	# base case: if len(a)<=1, return true
	# because it must be in order with 
	# only one element or nothing
	if len(a)<=1:
		return True
	# base case: if it have 2 element and first one
	# is less than second one, return True.
	if len(a) == 2:
		return a[0]<=a[1]

	# if list length is larger than 2,
	# check the first two elements and go on checking 
	# the rest of the list by recursion
	else:
		return a[0]<=a[1] and isSorted(a[1:])

def bubbleSort(a):
	# this function do oneStepBubbleSort untill it is sorted
	result = copy.copy(a)
	if isSorted(result):
		return result
	else:
		return bubbleSort(oneStepBubbleSort(a))

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

def testBubbleSort():
	print "Testing bubbleSort()...",
	for x in xrange(10):
		a = range(100)
		random.shuffle(a)
		assert(bubbleSort(a)==sorted(a))
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
	testNthHappyNumber()
	testFasterIsPrime()
	testIsHappyPrime()
	testNthHappyPrime()
	testOneStepBubbleSort()
	testIsSorted()
	testBubbleSort()
	testIsInCatalog()
	testGetScore()

if __name__ == "__main__":
    testAll()