#--------------------------------------------
def add(a, b):
    return a + b

result = add(3, 5)
print(result)

#--------------------------------------------
def greet(name):
    return "Hello " + name

message = greet("Dani")
print(message)

#--------------------------------------------
def is_even(n):
    return n % 2 == 0

print(is_even(6))

#--------------------------------------------
def min_max(numbers):
    return min(numbers), max(numbers)

a, b = min_max([3, 7, 1, 9])
print(a, b)