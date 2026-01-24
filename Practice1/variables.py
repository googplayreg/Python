# creating variables
x = 5
y = "John"

# no need to declare the type; moreover, type can be changed by simple rewriting
x = 4       # x is of type int
x = "Sally" # x is now of type str

# specifying the datatype by your own
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

# checking the datatype of the variable
x = 5
y = "John"
print(type(x))
print(type(y))

# single and double quotes are the same:
x = "John"
x = 'John'

# case-sensitive; e.g. a and A are NOT the same:
a = 4
A = "Sally"

# --------------------------------------------------

# Legal variable names:
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

# Illegal variable names:
# 2myvar = "John"
# my-var = "John"
# my var = "John"

# --------------------------------------------------

# creating global variable (outside the functions if any)
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

# it's also possible to create a global and local (inside the function) variables with the same name (but they may store different values)
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)