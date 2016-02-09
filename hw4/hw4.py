# hw4.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################
import string
def isVowel(s):
	if s=='a' or s=='e' or s=='i' or s=='o' or s=='u':
		return True
	elif s=='A' or s=='E' or s=='I' or s=='O' or s=='U':
		return True
	else:
		return False

def vowelCount(s):
	#take a string and calculate how much vowels it includes
	count = 0
	for i in s:
		if isVowel(i):
			count +=1
	return count

def sortByalpha(s):
	#take a string in which the same letter occurs no more than once
	#sort all the character in alphabetic order
	result = ''
	for i in xrange(len(s)):
		currentLetter = s[0]
		#find least letter in the current string
		for letter in s:
			currentLetter = min(letter, currentLetter)
		result += currentLetter
		#replace the least letter in current string and go to next loop
		s=s.replace(currentLetter,'') 
	return result


def leastFrequentLetters(s):
	#find the least frequent letter in s
	frequence = None
	currentFrequence = 0
	result=""
	s=s.lower() #transfer to lower cases
	#check alphabic letters in s one by one
	for letter in s:
		if(letter.isalpha()):
			currentFrequence = s.count(letter)
			#in the first time to enter here,
			#assign initial value to frequence
			if frequence == None:
				frequence =currentFrequence
				result = letter
			#if current frequence is less than frequence
			#update result and frequence
			elif currentFrequence < frequence:
				frequence = currentFrequence
				result = letter
			#if the current letter which is new
			#have the same frequence with letters we have found
			#add current letter to result
			elif currentFrequence == frequence and result.count(letter)==0:
				result += letter
	#sort the result and output
	result = sortByalpha(result)
	return result


def isPalindrome(s):
	#from course notes
	reverse = ""
	for c in s:
		reverse = c + reverse
	return (reverse == s)



def longestSubpalindrome(s):
	substring = ""
	longest = ""
	for i in xrange(len(s),0,-1):
	#check if all the substring consists of i characters are palindrome
		for j in xrange(len(s)-i+1):
			#substring = findSubstring(s,j+1,j+i)
			substring = s[j:j+i]
			if isPalindrome(substring):
				longest = max(substring,longest)
		if longest != "":
		#if we have found a palindrome, stop to check substring with less characters
			break
	return longest


#Question 6

def nextOperator(expr):
	#this function take in the current expresion, find the next operator and return
	operator = ""
	#check if there is a ** operator in expression
	#if so, just return it and stop
	for i in xrange(len(expr)):
		if expr[i]=="*" and expr[i+1]=="*":
			operator = "**"
			return operator
	#from left to right, check if there is a *, / or %
	#if so, return it and stop
	for i in xrange(len(expr)):
		if expr[i]=="*" or expr[i]=="/" or expr[i]=="%":
			operator = expr[i]
			return operator  #find the first operator in same precedence and stop
	#similarly, check the + and - operator
	for i in xrange(len(expr)):
		if expr[i]=="+" or expr[i]=="-":
			operator = expr[i]
			return expr[i]

def reverse(s):
	#take in a string and reverse it
	reverse = ""
	for c in s:
		reverse = c + reverse
	return reverse

def calculate(leftThing, rightThing, operator):
	#take in a expression with two operand and a operator, 
	#calculate result and return.
	leftThing = int(leftThing)
	rightThing = int(rightThing)
	#judge the type of operator and do calculation
	if operator == "+":
		result = leftThing + rightThing
	elif operator == "-":
		result = leftThing - rightThing
	elif operator == "*":
		result = leftThing * rightThing
	elif operator == "/":
		result = leftThing / rightThing
	elif operator == "%":
		result = leftThing % rightThing
	elif operator == "**":
		result = leftThing ** rightThing
	result = str(result)
	return result

def doOneStep(expr,operator):
	#take in the current expression and the operator fond in this step
	#find the part to be operated in this part including right thing ang left thing 
	#and the operator we have found

	#if we don't go to the code that assign value for left and right
	#that means one operand is in the start or the end of expr, 
	#we assign initial value for them in this condition
	(left,right) = (-1,len(expr)) 
	leftThing = rightThing = ""
	index = expr.find(operator)
	#find the thing left to operatior
	for i in xrange(index-1,-1,-1):
		if expr[i].isdigit(): 
			leftThing += expr[i]
		else: 
			left = i #store the index our operand in the original expression
			break
	leftThing=reverse(leftThing)

	#find the thing right to the operator
	#digit number of ** and other operator are different
	#the variable add is set to help find where right thing start
	add = 2 if operator == "**" else 1
	for i in xrange(index+add,len(expr)):
		if expr[i].isdigit(): 
			rightThing += expr[i]
		else : 
			right = i #store the index our operand in the original expression
			break
	#get calculate result of this step
	result = calculate(leftThing, rightThing, operator)
	expr = expr[0:left+1] + result + expr[right:]
	return expr

def getEvalSteps(expr):
	currentExpr = expr
	#make a white space string for indentation
	spaceLine = " " * len(expr) + " "
	outputString = expr + " "
	operator = ""
	step = 1 #in while loop, if step = 1, don't need a white space this step
	while(not currentExpr.isdigit()):
		operator = nextOperator(currentExpr)
		currentExpr=doOneStep(currentExpr,operator)
		if step==1:
			outputString += "= " + currentExpr
		else:
			outputString += "\n" + spaceLine + "= " + currentExpr
		step += 1
	#step=1 means that the expr is just a number
	#in this situation, output itself
	if step == 1:
		outputString += "= " + expr
	return outputString


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from Tkinter import *
import math

#Question 4
def countCharacter(text):
	#take in a text and count vowels,
	#consonants and other ono-space characterss
	vowels = 0
	consonants = 0
	others = 0
	for letter in text:
		if letter.isspace(): #if it is space, don't count
			continue
		letter = letter.lower() #ignore case
		if letter >= "a" and letter<="z":
			if isVowel(letter):
				vowels += 1
			else:
				consonants += 1
		else:
			others += 1
	return (vowels,consonants,others)

def drawWedge(canvas,letterType,(x0,y0,x1,y1),radius,cx,cy,
				number,total,start,extent,color,width,height):
		#draw a singe pipe wedge

		#if there is only one type, draw a circle. 
		#if not draw several pipe wedge to form a circle
		if number != total:
			canvas.create_arc((x0,y0,x1,y1), start=start, 
								extent=extent, fill=color)
		else:
			canvas.create_oval((x0,y0,x1,y1),fill=color)
		#find the center of the lable
		radius = radius*0.5
		angle = start + extent*0.5
		angle = math.radians(angle)
		#if we should draw a whole circle instead of some pipe wedge
		#the center will be different. next part consider this situation
		if number == total:
			(xLable,yLable) = (width/2,height/2)
		else:
			(xLable,yLable) = (cx+radius*math.cos(angle), cy-radius*math.sin(angle))

		#draw a lable in the region we have found above after string formatting
		percentRate = 100
		ratio = float(number)/float(total)*percentRate
		ratio = int(round(ratio))
		text = letterType
		text += " (%d of %d, %d%%)"%(number,total,ratio)
		canvas.create_text(xLable,yLable,text=text, font="Arial 12 bold")

def calculateWedgeData(vowels,consonants,others):
	#calculate data that used to draw pie charts
	total = vowels + consonants + others
	circleDegree = 360.0
	angleUnit = circleDegree/total if total !=0 else 0 
	startDegree = 90
	(vStart,vExtent) = (startDegree, vowels * angleUnit)
	(cStart,cExtent) = (vStart+vExtent, consonants * angleUnit)
	(oStart,oExtent) = (cStart + cExtent, others * angleUnit)
	return (vStart,vExtent,cStart,cExtent,oStart,oExtent)

def makeLetterTypePieChart(text, winWidth=500, winHeight=500):
	(vowels, consonants, others)=countCharacter(text) #get count results
	root = Tk()
	canvas = Canvas(root, width=winWidth, height=winHeight)
	canvas.pack()

	#calculate data for drawing
	(cx,cy) = (winWidth/2, winHeight/2)#get center of piechart
	radiusRatio = 0.9
	circleRadius = radiusRatio*min(winWidth,winHeight)/2
	#calculate boundary of arc
	boundary = (cx-circleRadius ,cy-circleRadius, cx+circleRadius, cy+circleRadius)
	total = vowels + consonants + others
	#in case of crash, when total =0, don't do deviding
	(vStart,vExtent,cStart,cExtent,oStart,oExtent) = calculateWedgeData(vowels,
														consonants,others)
	if vowels != 0:
		drawWedge(canvas,"vowels",boundary,circleRadius,cx,cy,vowels,total,
					vStart,vExtent,"pink",winWidth,winHeight)
	if consonants != 0:
		drawWedge(canvas,"consonants",boundary,circleRadius,cx,cy,consonants,total,
					cStart,cExtent,"cyan",winWidth,winHeight)
	if others != 0:
		drawWedge(canvas,"others",boundary,circleRadius,cx,cy,others,total,
					oStart,oExtent,"lightGreen",winWidth,winHeight)
	#don't draw anything if total is 0
	if total == 0:
		canvas.create_text(cx,cy,text="No data to display",font="Arial 20 bold")
	root.mainloop()


#question 5

def move(canvas,n,angle,color,cx,cy,drawWidth):
	angle = math.radians(angle)

	#calculate the x and y in the end of this step
	newx = cx + n*math.cos(angle)
	newy = cy - n*math.sin(angle)
	if color == "none":
		pass
	else:	
	#calculate the axes of two tops for the rectangle
		r=drawWidth/2.0
		canvas.create_line(cx,cy,newx,newy,fill=color,width=4)
	return (newx,newy)


def turnLeft(change,angle):
	return angle + change

def turnRight(change,angle):
	return angle - change

def runSimpleTortoiseProgram(program,winWidth=500,winHeight=500):
	root = Tk()
	canvas = Canvas(root, width=winWidth, height=winHeight)
	canvas.pack()
	color = None
	(angle,i) = (0,2)
	currentX = winWidth/2.0
	currentY = winHeight/2.0
	drawWidth = 4
	for line in program.splitlines():
		(textx,texty) = (10,10*i)
		i += 1
		line = line.strip() #delete white space in the begin and the end of this line
		canvas.create_text(textx,texty,text=line,anchor=SW,fill="gray",font="mono 10")
		if line.startswith("#"):
			continue
		elif line.startswith("color"):
			color = line.split(" ")[1]
		elif line.startswith("move"):
			(currentX,currentY) = move(canvas,int(line.split(" ")[1]),
										angle,color,currentX,currentY,drawWidth)
		elif line.startswith("left"):
			angle = turnLeft(int(line.split(" ")[1]), angle)
		elif line.startswith("right"):
			angle = turnRight(int(line.split(" ")[1]), angle)
	root.mainloop()


def testVowelCount():
	print "Testing vowelCount()...",
	assert (vowelCount('abedo')==3)
	assert (vowelCount('eUfdaC')==3)
	assert (vowelCount('lasdfkjoeweu')==5)
	print "Passed!"

def testSortByalpha():
	print "Testing sortByalpha()...",
	assert (sortByalpha('aewojf')=='aefjow')
	assert (sortByalpha('e')=='e')
	assert (sortByalpha('werldfs')=='deflrsw')
	print 'Passed!'

def testLeastFrequentLetters():
	print "Testing leastFrequentLetters()...",
	assert (leastFrequentLetters(" sfdeBBF!#89\n\\?;")=="des")
	assert (leastFrequentLetters('')=='')
	assert (leastFrequentLetters('abdewbBAeawdE')=='dw')
	assert (leastFrequentLetters("aDq efQ? FB'daf!!!")=="be")
	print "Passed!"

def testReverse():
	print "Testing reverse()...",
	assert (reverse("aba")=="aba")
	assert (reverse("?34")=="43?")
	assert (reverse("")=="")
	print "Passed!"

def testCalculate():
	print "Testing calculate()...",
	assert (calculate("3","2","**")=="9")
	assert (calculate("1","67","+")=="68")
	assert (calculate("3","2","/")=="1")
	assert (calculate("238765","2","%")=="1")
	print "Passed!"

def testLongestSubpalindrome():
	print "Testing longestSubpalindrome()...",
	assert (longestSubpalindrome("ab-4-be!!!")=="b-4-b")
	assert (longestSubpalindrome("abcbce")=="cbc")
	assert (longestSubpalindrome("abc")=="c")
	assert (longestSubpalindrome("\n")=="\n")
	print "Passed!"

def testDoOneStep():
	print "Testing doOneStep()...",
	assert (doOneStep("2234*938+34*3","*")=="2095492+34*3")
	assert (doOneStep("2234*34*3+5**4","**")=="2234*34*3+625")
	assert (doOneStep("123-23+982/50+37","/")=="123-23+19+37")
	print "Passed!"

def testGetEvalSteps():
	print "Testing getEvalSteps()...",
	assert (getEvalSteps("2+3*4-8**3%3")=="""2+3*4-8**3%3 = 2+3*4-512%3
             = 2+12-512%3
             = 2+12-2
             = 14-2
             = 12""")
	assert (getEvalSteps("34/3%34+2**3+1")=="""34/3%34+2**3+1 = 34/3%34+8+1
               = 11%34+8+1
               = 11+8+1
               = 19+1
               = 20""")
	assert (getEvalSteps("34")=="34 = 34")
	print "Passed!"


def testAll():
	makeLetterTypePieChart("ab,c de!?!")
	makeLetterTypePieChart("AB e") 
	makeLetterTypePieChart("A") 
	makeLetterTypePieChart("BKHKSdsf")
	testVowelCount()
	testSortByalpha()
	testLeastFrequentLetters()
	testReverse()
	testLongestSubpalindrome()
	testDoOneStep()
	testCalculate()
	testGetEvalSteps()
	runSimpleTortoiseProgram("""
	# This is a simple tortoise program
	color blue
	move 50

	left 90

	color red
	move 100

	color none # turns off drawing
	move 50

	right 45

	color green # drawing is on again
	move 50

	right 45

	color orange
	move 50

	right 90

	color purple
	move 100
	""", 300, 400)
	runSimpleTortoiseProgram("""
	# Y
	color red
	right 45
	move 50
	right 45
	move 50
	right 180
	move 50
	right 45
	move 50
	color none # space
	right 45
	move 25

	# E
	color green
	right 90
	move 85
	left 90
	move 50
	right 180
	move 50
	right 90
	move 42
	right 90
	move 50
	right 180
	move 50
	right 90
	move 43
	right 90
	move 50  # space
	color none
	move 25

	# S
	color blue
	move 50
	left 180
	move 50
	left 90
	move 43
	left 90
	move 50
	right 90
	move 42
	right 90
	move 50
	""")

if __name__ == "__main__":
    testAll()
