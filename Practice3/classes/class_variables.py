"""
Properties are variables that belong to a class. They store data for each object created from the class.

Example
Create a class with properties:
"""
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)


"You can access object properties using dot notation:"
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

car1 = Car("Toyota", "Corolla")

print(car1.brand)
print(car1.model)


"You can modify the value of properties on objects:"
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Tobias", 25)
print(p1.age)

p1.age = 26
print(p1.age)


"""
Class Properties vs Object Properties

Properties defined inside __init__() belong to each object (instance properties).
Properties defined outside methods belong to the class itself (class properties) and are shared by all objects:

Example
Class property vs instance property:
"""
class Person:
  species = "Human" # Class property

  def __init__(self, name):
    self.name = name # Instance property

p1 = Person("Emil")
p2 = Person("Tobias")

print(p1.name)
print(p2.name)
print(p1.species)
print(p2.species)


"""
When you modify a class property, it affects all objects:

Example
Change a class property:
"""
class Person:
  lastname = ""

  def __init__(self, name):
    self.name = name

p1 = Person("Linus")
p2 = Person("Emil")

Person.lastname = "Refsnes"

print(p1.lastname)
print(p2.lastname)


"""
You can add new properties to existing objects:

Example
Add a new property to an object:
"""
class Person:
  def __init__(self, name):
    self.name = name

p1 = Person("Tobias")

p1.age = 25
p1.city = "Oslo"

print(p1.name)
print(p1.age)
print(p1.city)

# Note: Adding properties this way only adds them to that specific object, not to all objects of the class.