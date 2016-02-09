
class C(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		if isinstance(self, D):
			return "<Just %d>" % self.x
		return "<%d and %d>" % (self.x, self.y)

	def __eq__(self, other):
		if self.x==other.x and self.y == other.y:
			return True
		else :
			return False
	def __repr__(self):
		return "C(%r, %r)" % (self.x, self.y)

	def __add__(self, other):
		if not isinstance(other,c): return 42
		return C(self.x+other.x, self.y+other.y)

	def reversed(self):
		return C(self.y, self.x)

	def reverse(self):
		return (self.x, self.y) = (self.y, self.x)



class D(C):
	def __init__(self, x):
		super(D, self).__init__(x,x)


class rectangle(object):
	def __init__(self):
'''

class H(object):
	def __init__(self, age):
		self.age = age
	def __hash__(self):
		return hash(self.age)
	def __str__(self):
		return '42'
	def __repr__(self):
		return "lvpa"

h1 = H('15')
h2 = H('14')
h3 = H('15')


print repr(h1)
print [h1]

class Dog(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return (self.name == other.name) and (self.age == other.age)

    def __repr__(self):
        return "Dog('%s', %d)" % (self.name, self.age)

    def __str__(self):
        return "Dog(%s, %s)" % (self.name, self.age)


pet1 = Dog("marceau", 10)
print pet1   # prints Dog(marceau, 10)
print [pet1] # prints [Dog(marceau, 10)]  (huzzah!)

print "That's great, but what about this (it is preferred"
print "for eval(repr(x)) to return an object equal to x):"
pet2 = eval(repr(pet1))  # NameError: name 'marceau' is not defined
print pet2 == pet1
