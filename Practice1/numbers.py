x = 7     # int
y = 9.3   # float
z = 4j    # complex
print(type(x))
print(type(y))
print(type(z))
#------------------------------
x = 42e2
y = 7E5
z = -12.4e50

print(type(x))
print(type(y))
print(type(z))
#-----------------------------
x = 8+2j
y = 9j
z = -3j

print(type(x))
print(type(y))
print(type(z))
#-----------------------------
x = 6     # int
y = 5.9   # float
z = 2j    # complex

# convert from int to float:
a = float(x)

# convert from float to int:
b = int(y)

# convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))
#--------------------------------
import random

print(random.randrange(10, 50))
