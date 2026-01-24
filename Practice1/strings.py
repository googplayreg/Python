# strings in Python are arrays of unicode characters
a = "Hello, World!"
print(a[1])
# since strings are arrays, we can loop through the characters in a string, with a for loop:
for x in "banana":
    print(x)
# to get the length of a string, use the len() function:
a = "Hello, World!"
print(len(a))
# to check if a certain phrase or character is present in a string, we can use the keyword in:
txt = "The best things in life are free!"
print("free" in txt)
# to check if a certain phrase or character is NOT present in a string, we can use the keyword not in:
txt = "The best things in life are free!"
print("expensive" not in txt)

# --------------------------------------------------------

# specify the start index and the end index, separated by a colon, to return a part of the string:
b = "Hello, World!"
print(b[2:5])

# by leaving out the start index, the range will start at the first character:
b = "Hello, World!"
print(b[:5])

# by leaving out the end index, the range will go to the end:
b = "Hello, World!"
print(b[2:])

# use negative indexes to start the slice from the end of the string:
b = "Hello, World!"
print(b[-5:-2])

#*IMPORTANT! THE LAST INDEX IS NOT INCLUDED IN ALL OF THE CASES!

# --------------------------------------------------------

# The upper() method returns the string in upper case:
a = "Hello, World!"
print(a.upper())
# the lower() method returns the string in lower case:
a = "Hello, World!"
print(a.lower())
# the strip() method removes any whitespace from the beginning or the end:

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

# the replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J")) # returns "Jello, World!"

# the split() method splits the string into substrings if it finds instances of the separator:
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

# --------------------------------------------------------

# we can concatenate (add to each other) strings:
a = "Hello"
b = "World"
c = a + b
print(c)
# we can also add a space:
a = "Hello"
b = "World"
c = a + " " + b
print(c)

# --------------------------------------------------------

# to specify a string as an f-string, simply put an f in front of the string literal, and add curly brackets {} as placeholders for variables and other operations:
age = 36
txt = f"My name is John, I am {age}"
print(txt)
# it's also possible to perform mathematical operations in the placeholders:
txt = f"The price is {20 * 59} dollars"
print(txt)

# --------------------------------------------------------

# you will get an error if you use double quotes inside a string that is surrounded by double quotes:
# txt = "We are the so-called "Vikings" from the north." 

# to fix this problem, use the escape character \":
# the escape character allows you to use double quotes when you normally would not be allowed:
txt = "We are the so-called \"Vikings\" from the north."