a = float(input("Zadej stranu a: "))
b = float(input("Zadej stranu b: "))
c = float(input("Zadej stranu c: "))

if not (a + b > c and a + c > b and b + c > a):
    print("Trojúhelník nelze sestavit")
    exit()

if a == b == c:
    triangle_type = "rovnostranný"
elif a == b or b == c or a == c:
    triangle_type = "rovnoramenný"
else:
    triangle_type = "obecný"

if c >= a and c >= b:
    is_right = c ** 2 == a ** 2 + b ** 2
elif a >= b and a >= c:
    is_right = a ** 2 == b ** 2 + c ** 2
else:
    is_right = b ** 2 == a ** 2 + c ** 2

is_right = is_right and triangle_type == "obecný"

print(f"Trojúhelník: {triangle_type}{', pravoúhlý' if is_right else ''}")
