def get_rectangle_area(a, b):
    return a * b


side_a = float(input("Type side a: "))
side_b = float(input("Type side b: "))

rectangle_area = get_rectangle_area(side_a, side_b)

print(f"Rectangle area: {rectangle_area:0.2f}")

