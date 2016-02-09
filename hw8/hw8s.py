# hw8.py
# Zekun Lyu + zlyu + R

######################################################################
# Place your autograded solutions below here
######################################################################
class Polynomial(object):
	def __init__(self, *coeffs):
		# if there is no arguments, construct the object as Polynomial([0])
		if len(coeffs)==0: coeffs=[0]
		# if a list or a tuple is given assign the list or tuple to coeffs
		if type(coeffs[0])==list or type(coeffs[0])==tuple:
			coeffs = coeffs[0]
		# if several integers is given
		# delete leading zeros
		index = 0
		while (index<len(coeffs) and coeffs[index]==0):
			index += 1
		# cast the tuple to list and assign it to coeffs
		coeffs = list(coeffs[index:])
		if coeffs == []:
			coeffs = [0]
		self.coeffs = coeffs


	
	def degree(self):
		# The degree is power of the largest exponent, and since
		# we start at x**0, this is one less than the number of coefficients.
		return len(self.coeffs)-1
	
	def coeff(self, power):
		# This returns the coefficient corresponding to the given power.
		# Note that these are stored in reverse, in that the coefficient
		# for x**0 is not stored in coeffs[0] but rather coeffs[-1].
		return self.coeffs[self.degree()-power]
	
	def evalAt(self, x):
		# Evaluate this polynomial at the given value of x.
		return sum([self.coeff(power)*x**power
					for power in xrange(self.degree()+1)])

	def __add__(self, other):
		# Add this polynomial to another polynomial, producing a third
		# polyonial as the result.  This makes the + operator work right.
		# First, make both coefficent lists the same length by nondestructively
		# adding 0's to the front of the shorter one
		(coeffs1, coeffs2) = (self.coeffs, other.coeffs)
		if (len(coeffs1) > len(coeffs2)):
			(coeffs1, coeffs2) = (coeffs2, coeffs1)
		# Now, coeffs1 is shorter, so add 0's to its front
		coeffs1 = [0]*(len(coeffs2)-len(coeffs1)) + coeffs1
		# Now they are the same length, so add them to get the new coefficients
		coeffs = [coeffs1[i] + coeffs2[i] for i in xrange(len(coeffs1))]
		# And create the new Polynomial instance with these new coefficients
		return Polynomial(coeffs)

	def derivative(self):
		# Take the first derivative of this polynomial, returning the result
		# as a new polynomial.  For example:
		# f(x)  = A*x**3 + B*x**2 + C*x**1 + D
		# f'(x) = 3*A*x**2 + 2*B*x**1 + 1*C   [ 3*A, 2*B, 1*C ]
		coeffs = [ power*self.coeff(power)
				   for power in xrange(self.degree(), 0, -1)]
		return Polynomial(coeffs)

	def __str__(self):
		# Convert this polynomial into a human-readable string.
		# This is not a very good string implementation. Ugly, but functional.
		result = ""
		for power in xrange(self.degree(), -1, -1):
			if (result != ""): 
				# result!=""means this is not he first item of the expression
				# add'+' or '-' in front of the non-leading item
				if self.coeff(power)>0: result += "+"
				elif self.coeff(power)<0: result += "-"

				# if the coefficient is 0, don't add sign symbol
				else : continue
			coeff = self.coeff(power)
			# convert each coefficient to its absolute value
			# except the largest power's coeff, because we want to
			# preserve it's sign.
			if power != self.degree(): coeff = abs(coeff)
			item = " %dx^%d " % (coeff, power)
			# remove all the '1' from items except the constant item
			if '1' in item and power!=0: item = item.replace('1','')
			# remove the symbol '^' for power 1 item
			if power==1: item = item[:-2] + item[-1]
			if power==0: item = item[:-4]
			result += item
		result = result.strip()#remove white space in the start and end
		return result


	def __eq__(self, other):
		if (not isinstance(other, Polynomial)):
			# firstly, consider situaion where other is not a Polynomial

			# A polynomial of degree 0 has to equal the same non-Polynomial 
			# numeric!
			if (len(self.coeffs)==1 and type(other)==int 
				and self.coeffs[0]==other):
				return True
			# Apolynamial equalt to the list consists of same elements
			# with those of its coeffs
			if type(other)==list and other==self.coeffs: return True
			# in other cases, return False
			return False
		# two Polynomials are equal when their coeffs are the same
		for power in xrange(self.degree()+1):
			if self.coeff(power)!=other.coeff(power):
				return False
		return True

	def __repr__(self):
		# return the result of it's coeffs casted to a str
		return str(self.coeffs)

	def __hash__(self):
		# let each value in coeffs mapped to a unique result in hash table
		result = 0
		for value in self.coeffs:
			result += hash(value)+hash(':)')
		return hash(result)

	def __mul__(self, other):
		# when multiplyed by a integer
		# let each element multiplyed by the integer
		# for example: Polynomial([1,2])*10 = Polynomial([10,20])
		if isinstance(other, int):
			coeffs = self.coeffs
			return Polynomial([other*coeff for coeff in coeffs])
		# Polynomial times another Polynomial
		if isinstance(other, Polynomial):
			result = Polynomial()#store the result
			degree = other.degree()
			for power in xrange(degree+1):
				# split operation into multiple steps
				# each step, let a coefficient of others multiply 
				# this Polynomial. 
				multiplier = other.coeff(power)
				newCoeffs = [multiplier*coeff for coeff in self.coeffs]
				# add endding zeros
				newCoeffs += [0]*power
				# add the paritial result to total result
				result += Polynomial(newCoeffs)
		return result

	def __rmul__(self, other): return self.__mul__(other)

	def __pow__(self, power):
		if power==0: return 1
		result = Polynomial(self.coeffs)
		for x in xrange(power-1):
			result = result*Polynomial(self.coeffs)
		return result

class Quadratic(Polynomial):
	def __init__(self, *coeffs):
		if len(coeffs)==3 or len(coeffs[0])==3:
			super(Quadratic, self).__init__(coeffs)
		else:
			raise Exception("Invalid quadratic representation")

	def determinant(self):
		# calculate determinant based on the equation:b882-4*a*c and return
		coeffs = self.coeffs
		(a, b, c) = (coeffs[0], coeffs[1], coeffs[2])
		return b*b-4.0*a*c

	def numberOfRealRoots(self):
		# judge the number of roots given value of determinant
		if self.determinant()>0:
			return 2
		elif self.determinant()==0:
			return 1
		else:
			return 0

	def getRealRoots(self):
		# calculate all the roots and form a list to return
		coeffs = self.coeffs
		(a, b, c) = (coeffs[0], coeffs[1], coeffs[2])
		if self.numberOfRealRoots()==0:
			return []
		if self.numberOfRealRoots()==1:
			return [(-1.0)*b/2/a]
		if self.numberOfRealRoots()==2:
			determinant = self.determinant()
			root1 = ((-1.0)*b-determinant**0.5)/2/a
			root2 = ((-1.0)*b+determinant**0.5)/2/a
			return [root1, root2]





######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
def testPolynomialAndQuadraticClasses():
	print "Testing Polynomial and Quadratic classes..."
	for testFn in [testPolynomialBasicsFromClassNotes,
				   testPolynomialEq,
				   testPolynomialStr,
				   testPolynomialRepr,
				   testPolynomialConstructor,
				   testPolynomialInSets,
				   testPolynomialTimesOperator,
				   testPolynomialExponentiationOperator,
				   testQuadraticClass
				  ]:
		print "  Running %s..." % testFn.__name__,
		testFn()
		print "Passed!"
	print "Passed all Polynomial and Quadratic Class tests!"

def almostEqual(d1, d2):
	epsilon = 0.000001
	return abs(d1 - d2) < epsilon

def testPolynomialBasicsFromClassNotes():
	# Commented out the string assertions since we actually
	# changed/improved those as part of this hw
	p1 = Polynomial([2, -3, 5])  # 2x**2 -3x + 5
	#assert(str(p1) == "2*x**2+-3*x**1+5*x**0") # ugly, but functional
	assert(type(p1) == Polynomial)
	assert(p1.degree() == 2)
	assert(p1.coeff(0) == 5)
	assert(p1.coeff(1) == -3)
	assert(p1.coeff(2) == 2)
	assert(p1.evalAt(0) == 5)
	assert(p1.evalAt(2) == 7)
	# Now test the derivative method
	p2 = p1.derivative() # 4x - 3
	#assert(str(p2) == "4*x**1+-3*x**0")
	assert(type(p2) == Polynomial)
	assert(p2.evalAt(2) == 5)
	assert(p2.evalAt(5) == 17)
	# Now test the + operator
	p3 = p1 + p2 # (2x**2 -3x + 5) + (4x - 3) == (2x**2 + x + 2)
	#assert(str(p3) == "2*x**2+1*x**1+2*x**0")
	assert(type(p3) == Polynomial)
	assert(p3.evalAt(2) == 12)
	assert(p3.evalAt(5) == 57)

def testPolynomialEq():
	assert(Polynomial([1,2,3]) == Polynomial([1,2,3]))
	assert(Polynomial([1,2,3]) != Polynomial([1,2,3,0]))
	assert(Polynomial([1,2,3]) != Polynomial([1,2,0,3]))
	assert(Polynomial([1,2,3]) != Polynomial([1,-2,3]))
	assert(Polynomial([1,2,3]) != 42)
	assert(Polynomial([1,2,3]) != "Wahoo!")
	# A polynomial of degree 0 has to equal the same non-Polynomial numeric!
	assert(Polynomial([42]) == 42)

def testPolynomialStr():
	assert(str(Polynomial([1,2,3])) == "x^2 + 2x + 3")
	assert(str(Polynomial([-1,-2,-3])) == "-x^2 - 2x - 3")
	assert(str(Polynomial([42])) == "42")
	assert(str(Polynomial([-42])) == "-42")
	assert(str(Polynomial([0])) == "0")
	assert(str(Polynomial([1,0,-3, 0, 1])) == "x^4 - 3x^2 + 1")
	assert(str(Polynomial([1,0,-3, 0, 1])) == "x^4 - 3x^2 + 1")
	assert(str(Polynomial([-1,0,3, 0, -1])) == "-x^4 + 3x^2 - 1")

def testPolynomialRepr():
	for coeffs in [ [1,2,3], [0], [-1,0,2,0,-3] ]:
		assert(eval(repr(Polynomial(coeffs))) == Polynomial(coeffs))

def testPolynomialConstructor():
	# If the list is empty, treat it the same as [0]
	assert(Polynomial([]) == Polynomial([0]))
	assert(Polynomial([]) != Polynomial([1]))
	# Remove leading 0's
	assert(Polynomial([0,0,0,1,2]) == Polynomial([1,2]))
	assert(Polynomial([0,0,0,1,2]).degree() == 1)
	# Require that the constructor be non-destructive
	coeffs = [0,0,0,1,2]
	assert(Polynomial(coeffs) == Polynomial([1,2]))
	assert(coeffs == [0,0,0,1,2])
	# Require that the constructor also accept tuples of coefficients
	coeffs = (0, 0, 0, 1, 2)
	assert(Polynomial(coeffs) == Polynomial([1,2]))
	# Allow for variable-length arguments.  That is, if the arguments
	# are not a list, then put them in a list
	assert(Polynomial(1,2,3) == Polynomial([1,2,3]))
	# And thus if no values are supplied, this is also the same as [0]:
	assert(Polynomial() == Polynomial([0]))

def testPolynomialInSets():
	s = set()
	assert(Polynomial(1,2,3) not in s)
	s.add(Polynomial(1,2,3))
	assert(Polynomial(1,2,3) in s)
	assert(Polynomial([1,2,3]) in s)
	assert(Polynomial(1,2) not in s)

def testPolynomialTimesOperator():
	# (x**2 + 2)(x**4 + 3x**2) == (x**6 + 5x**4 + 6x**2)
	assert(Polynomial([1,0,2]) * Polynomial([1,0,3,0,0]) ==
		   Polynomial([1,0,5,0,6,0,0]))
	# (x**3 - 3x + 5) * 10 == (10x**3 - 30x + 50)
	assert(Polynomial(1,0,-3,5) * 10 == Polynomial(10,0,-30,50))
	# Hint: to do multiplication this way, you have to use __rmul__,
	# which should just call __mul__ (yes, really)
	assert(10 * Polynomial(1,0,-3,5) == Polynomial(10,0,-30,50))

def testPolynomialExponentiationOperator():
	assert(Polynomial(1,2,3)**0 == 1)
	assert(Polynomial(1,2,3)**1 == Polynomial(1,2,3))
	assert(Polynomial(1,2,3)**2 == Polynomial(1,2,3) * Polynomial(1,2,3))
	assert(Polynomial(1,2,3)**3 == Polynomial(1,2,3) * Polynomial(1,2,3) * Polynomial(1,2,3))

def testQuadraticClass():
	q1 = Quadratic(3,2,1)  # 3x^2 + 2x + 1
	assert(type(q1) == Quadratic)
	assert(q1.evalAt(10) == 321)
	assert(isinstance(q1, Quadratic) == isinstance(q1, Polynomial) == True)
	# the determinant is b**2 - 4ac
	assert(q1.determinant() == -8)
	# use the determinant to determine how many real roots (zeroes) exist
	assert(q1.numberOfRealRoots() == 0)
	assert(q1.getRealRoots() == [ ])
	# Once again, with a double root
	q2 = Quadratic(1,-6,9)
	assert(q2.determinant() == 0)
	assert(q2.numberOfRealRoots() == 1)
	[root] = q2.getRealRoots()
	assert(almostEqual(root, 3))
	# And again with two roots
	q3 = Quadratic(1,1,-6)
	assert(q3.determinant() == 25)
	assert(q3.numberOfRealRoots() == 2)
	[root1, root2] = q3.getRealRoots() # smaller one first
	assert(almostEqual(root1, -3) and almostEqual(root2, 2))
	# Now, creating a non-quadratic "Quadratic" is an error
	ok = False # the exception turns this to True!
	try: q = Quadratic(1,2,3,4) # this is cubic, should fail!
	except: ok = True
	assert(ok)
	# one more time, with a line, which is sub-quadratic, so also fails
	ok = False
	try: q = Quadratic([2,3])
	except: ok = True
	assert(ok)
	# And make sure that these methods were defined in the Quadratic class
	# and not in the Polynomial class (we'll just check a couple of them...)
	assert('evalAt' in Polynomial.__dict__)
	assert('evalAt' not in Quadratic.__dict__)
	assert('determinant' in Quadratic.__dict__)
	assert('determinant' not in Polynomial.__dict__)

testPolynomialAndQuadraticClasses()