"""
All classes have a built-in method called __init__(), which is always executed when the class is being initiated.
The __init__() method is used to assign values to object properties, or to perform operations that are necessary when the object is being created.

Example
Create a class named Person, use the __init__() method to assign values for name and age:
"""
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)


"The __init__() method can have as many parameters as you need:"
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Linus", 30, "Oslo", "Norway")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)