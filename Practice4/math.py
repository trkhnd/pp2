import math

#-----------------------------------
# Convert Degree to Radian
#-----------------------------------

degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", round(radian, 6))


#-----------------------------------
# Area of a Trapezoid
#-----------------------------------

height = float(input("\nHeight: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

trapezoid_area = (base1 + base2) / 2 * height
print("Expected Output:", trapezoid_area)


#-----------------------------------
# Area of Regular Polygon
#-----------------------------------

n = int(input("\nInput number of sides: "))
s = float(input("Input the length of a side: "))

polygon_area = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(polygon_area))


#-----------------------------------
# Area of a Parallelogram
#-----------------------------------

base = float(input("\nLength of base: "))
height_para = float(input("Height of parallelogram: "))

parallelogram_area = base * height_para
print("Expected Output:", parallelogram_area)

#-----------------------------------