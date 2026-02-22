#1 square numbers up to N
def square_gen(n):
    for i in range(1, n+1):
        yield i**2
        i += 1

N = int(input())
for i in square_gen(N):
    print(i)

#2 even numbers between 0 and n
def evens(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

n = int(input())
print(*evens(n), sep = ",")

#3 numbers divisible by 3 and 4
def div_3_4(n):
    for i in range(1, n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
print(*div_3_4(n))

#4 square from a to b
def squares(a, b):
    for i in range(a, b+1):
        yield i**2
        i += 1

a = int(input())
b = int(input())
for i in squares(a, b):
    print(i, end = " ")

#5 all numbers from n down to 0
def decr_gen(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())
print(*decr_gen(n))