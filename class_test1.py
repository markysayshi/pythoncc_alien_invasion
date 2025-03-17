# simple class refresh
# https://www.w3schools.com/python/python_inheritance.asp

class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)

# Use the person 'parent' class to create an object,
# and then execute the printname method.
#x = Person("John", "Doe")
#x.printname()

class Student(Person):
    # use pass when you don't want any other properties or methods
    pass

# Use the student 'child' class to create an object,
# and then execute the printname method.
x = Student("Mike", "Olsen")
x.printname()
