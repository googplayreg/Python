"""
When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.

Note: The child's __init__() function overrides the inheritance of the parent's __init__() function.
"""

class Student(Person):
  def __init__(self, fname, lname):
    self.age = 21

"""
To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:

Example
"""
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)


"""
Example
Add a method called welcome to the Student class:
"""
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)
    
# If you add a method in the child class with the same name as a function in the parent class, the inheritance of the parent method will be overridden.

