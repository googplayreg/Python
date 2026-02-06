"""
To create a class, use the keyword class.
Create a class named MyClass, with a property named x:
"""
class MyClass:
  x = 5

"""
Now we can use the class named MyClass to create objects:
Example
Create an object named p1, and print the value of x:
"""
p1 = MyClass()
print(p1.x)

"You can delete objects by using the del keyword:"
del p1

"You can create multiple objects from the same class:"
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)