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
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

    # use pass when you don't want any other properties or methods
    #pass

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of",
              self.graduationyear)

# Use the student 'child' class to create an object,
# and then execute the printname method.
x = Student("Mike", "Olsen", 2019)
x.printname()
x.welcome()
