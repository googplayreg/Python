# A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).
# With the for loop we can execute a set of statements, once for each item in a list, tuple, set etc.

# Example
# Print each fruit in a fruit list:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

# Even strings are iterable objects, they contain a sequence of characters
for x in "banana":
  print(x)