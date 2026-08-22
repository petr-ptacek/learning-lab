def get_rectangle_area(a, b):
    return a * b


def get_rectangle_perimeter(side_a, side_b):
    return 2 * (side_a + side_b)


side_a = float(input("Type side a: "))
side_b = float(input("Type side b: "))

rectangle_area = get_rectangle_area(side_a, side_b)
rectangle_perimeter = get_rectangle_perimeter(side_a, side_b)

print(f"Rectangle area: {rectangle_area:.>20.2f}")
print(f"Rectangle perimeter: {rectangle_perimeter:.>20.2f}")
