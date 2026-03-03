import re

print("--- REGEX RESULTS ---")

# 1. 'a' followed by zero or more 'b's
s1 = 'abbbb asda ab hfhadh abbbbbbbbbb'
res1 = re.findall(r"ab*", s1)
print(f"Task 1: '{s1}' -> {res1}")
# Task 1: 'abbbb asda ab hfhadh abbbbbbbbbb' -> ['abbbb', 'a', 'a', 'ab', 'a', 'abbbbbbbbbb']

# 2. 'a' followed by two to three 'b'
s2 = 'abb abbb' # for fullmatch it's better to use clean string
res2 = re.findall(r"ab{2,3}", 'abb abbb aasdada sdabdbas') # findall suits better here
print(f"Task 2: 'abb abbb aasdada...' -> {res2}")
# Task 2: 'abb abbb aasdada sdabdbas' -> ['abb', 'abbb']

# 3. Lowercase letters joined with underscore
s3 = 'string_intance hello_again notreally'
res3 = re.findall(r"[a-z]+_[a-z]+", s3)
print(f"Task 3: '{s3}' -> {res3}")
# Task 3: 'string_intance hello_again notreally' -> ['string_intance', 'hello_again']

# 4. Uppercase followed by lowercase
s4 = 'Apple Pen Bread Village'
res4 = re.findall(r"[A-Z][a-z]+", s4)
print(f"Task 4: '{s4}' -> {res4}")
# Task 4: 'Apple Pen Bread Village' -> ['Apple', 'Pen', 'Bread', 'Village']

# 5. 'a' anything in between 'b'
s5 = 'aANYTHINGLITERALLYb'
res5 = re.fullmatch(r"a.*b", s5).group() if re.fullmatch(r"a.*b", s5) else None
print(f"Task 5: '{s5}' -> {res5}")
# Task 5: 'aANYTHINGLITERALLYb' -> aANYTHINGLITERALLYb

# 6. Replace space, comma, dot with colon
s6 = 'hello, world. test'
res6 = re.sub(r"[ ,.]", ":", s6)
print(f"Task 6: '{s6}' -> '{res6}'")
# Task 6: 'hello, world. test' -> 'hello::world::test'

# 7. Snake to Camel
s7 = 'instance_of_snake'
def snake_to_camel(s):
    return ''.join(word.capitalize() for word in s.split('_'))
print(f"Task 7: '{s7}' -> '{snake_to_camel(s7)}'")
# Task 7: 'instance_of_snake' -> 'InstanceOfSnake'

# 8. Split at uppercase
s8 = 'SplitThisString'
res8 = re.split(r"(?=[A-Z])", s8)
print(f"Task 8: '{s8}' -> {res8}")
# Task 8: 'SplitThisString' -> ['', 'Split', 'This', 'String']

# 9. Insert spaces before capitals
s9 = 'InsertSpacesHere'
res9 = re.sub(r"(\w)([A-Z])", r"\1 \2", s9)
print(f"Task 9: '{s9}' -> '{res9}'")
# Task 9: 'InsertSpacesHere' -> 'Insert Spaces Here'

# 10. Camel to Snake
s10 = 'TypicalCamelCase'
def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
print(f"Task 10: '{s10}' -> '{camel_to_snake(s10)}'")
# Task 10: 'TypicalCamelCase' -> 'typical_camel_case'