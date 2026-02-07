"Multiple inheritance in Python allows to a class to inherit properties and methods of several parents, specified in the brackets"
class Parent1:
    pass
class Parent2:
    pass
class Child(Parent1, Parent2):
    pass
"When a method is called, Python looks for it in the child class, then in the first parent class, then in the second, and so on."