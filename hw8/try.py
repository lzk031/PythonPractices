class Dog(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return (self.name == other.name) and (self.age == other.age)

pet1 = Dog("marceau", 10)
s = set()
s.add(pet1)

pet2 = Dog("marceau", 10)
print pet2 == pet1 # prints True
print pet1 in s    # prints True
print pet2 in s    # prints False (should be True!)