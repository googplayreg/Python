"""
Python Inheritance
Inheritance allows us to define a class that inherits all the methods and properties from another class.
Parent class is the class being inherited from, also called base class.
Child class is the class that inherits from another class, also called derived class.
#############################################################################################################
Any class can be a parent class, so the syntax is the same as creating any other class:

Example
Create a class named Person, with firstname and lastname properties, and a printname method:
"""
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()


"To create a class that inherits the functionality from another class, send the parent class as a parameter when creating the child class:"
class Student(Person):
  pass


"Add the __init__() function to the Student class:"

class Student(Person):
  def __init__(self, fname, lname):
    self.age = 21

"When you add the __init__() function, the child class will no longer inherit the parent's __init__() function."