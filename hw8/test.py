class Dog(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return (self.name == other.name) and (self.age == other.age)

    def __repr__(self):
        return "Dog(%r, %r)" % (self.name, self.age)

pet1 = Dog("marceau", 10)
print pet1   # prints Dog(marceau, 10)
print [pet1] # prints [Dog(marceau, 10)]  (huzzah!)

print "That's great, but what about this (it is preferred"
print "for eval(repr(x)) to return an object equal to x):"
pet2 = eval(repr(pet1))  # NameError: name 'marceau' is not defined
print pet2 == pet1
print [pet1]
