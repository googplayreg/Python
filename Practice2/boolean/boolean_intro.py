# The bool() function allows you to evaluate any value, and give you True or False in return,
# Evaluate a string and a number:
print(bool("Hello"))
print(bool(15))

# Evaluate two variables:
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

# Most Values are True
# Almost any value is evaluated to True if it has some sort of content.
# Any string is True, except empty strings.
# Any number is True, except 0.
# Any list, tuple, set, and dictionary are True, except empty ones.

# The following will return True:
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# Some Values are False
# In fact, there are not many values that evaluate to False, except empty values.

# The following will return False:
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# functions can return a boolean
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")