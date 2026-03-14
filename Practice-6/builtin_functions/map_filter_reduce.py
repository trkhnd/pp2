from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map example
squares = list(map(lambda x: x**2, numbers))
print("Squares:", squares)

# filter example
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce example
total = reduce(lambda a, b: a + b, numbers)
print("Sum:", total)