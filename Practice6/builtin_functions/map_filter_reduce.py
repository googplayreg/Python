# map and filter functions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

print(squared)
print(evens)

# reduce function
"""reduce function takes two first elements and applies the function to them, 
then takes the result and the next element and applies function to them and so on"""
from functools import reduce

product = reduce(lambda x, y: x * y, numbers)
print(product)

# When using the reduce() function, we need to import it from the functools library
# In the example above, our function multiplies all elements, so that we get the factorial of 10 in our case. 