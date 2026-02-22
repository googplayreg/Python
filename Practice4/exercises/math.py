import math

#1 convert degree to radian
deg = int(input("Input degree: "))
rad = math.radians(deg)
print(f"Output radians: {rad}")

#2 trapezoid area
h = int(input("Height: "))
b1 = int(input("Base, first value: "))
b2 = int(input("Base, second value: "))
trapezoid_area = float(((b1+b2)/2)*h)
print(trapezoid_area)

#3 regular polygon area
n = int(input("Input number of sides: "))
l = int(input("Input the length of a side: "))
r_polygon_area = n * l * l / (4 * math.tan(math.pi/n))
# if r_polygon_area.is_integer():
#     result = int(r_polygon_area)
# else:
#     result = r_polygon_area
print(f"The area of a polygon is: {r_polygon_area}")

#4 parallelogram area
l = int(input("Length of base: "))
h = int(input("Heigth of parallelogram: "))
parallelogram_area = float(l * h)
print(parallelogram_area)