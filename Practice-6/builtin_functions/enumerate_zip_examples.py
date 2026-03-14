# enumerate example
names = ["Alice", "Bob", "Charlie"]

print("Enumerate example:")
for index, name in enumerate(names):
    print(index, name)

print()

# zip example
scores = [90, 85, 88]

print("Zip example:")
for name, score in zip(names, scores):
    print(name, score)

# Type checking and conversions

print("\nType checking and conversions:")

value = "123"  # this is a string
print("Original value:", value)
print("Type before conversion:", type(value))

# convert string to integer
number = int(value)

print("Converted value:", number)
print("Type after conversion:", type(number))

# check if variable is integer
if isinstance(number, int):
    print("The variable 'number' is an integer")