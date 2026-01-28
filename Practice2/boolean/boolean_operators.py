# functions can return a boolean
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

# Built-in function isinstance() function checks the type of an object:
x = 200
print(isinstance(x, int))