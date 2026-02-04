"""
Information can be passed into functions as arguments.
Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma.
The following example has a function with one argument (fname). 
When the function is called, we pass along a first name, which is used inside the function to print the full name:
"""
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")

#####################################################################################################################################################

"""
PARAMETERS vs ARGUMENTS
From a function's perspective:
- A parameter is the variable listed inside the parentheses in the function definition.
- An argument is the actual value that is sent to the function when it is called.
"""
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

"You can assign default values to parameters. If the function is called without an argument, it uses the default value:"
def my_function(name = "friend"):
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#####################################################################################################################################################

"KEYWORD ARGUMENTS"
"You can send arguments with the key = value syntax."
"This way, with keyword arguments, the order of the arguments does not matter."
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy")

"When you call a function with arguments without using keywords, they are called positional arguments."
"Positional arguments MUST BE IN THE CORRET ORDER:"
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy")

"The order matters with positional arguments:"
"Switching the order changes the result:"
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("Buddy", "dog")


"""
You can mix positional and keyword arguments in a function call.
However, positional arguments must come before keyword arguments:
"""
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)
my_function("dog", name = "Buddy", age = 5)

#####################################################################################################################################################

"""
You can send any data type as an argument to a function (string, number, list, dictionary, etc.).
The data type will be preserved inside the function:
Example
Sending a list as an argument:
"""
def my_function(fruits):
  for fruit in fruits:
    print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

"Sending a dictionary as an argument:"
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)