# The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".
# The elif keyword allows you to check multiple expressions for True and execute a block of code as soon as one of the conditions evaluates to True.
# You can have as many elif statements as you need.
# When you use elif, Python evaluates the conditions from top to bottom. 
# As soon as it finds a condition that is true, it executes that block and skips all remaining conditions.

temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")