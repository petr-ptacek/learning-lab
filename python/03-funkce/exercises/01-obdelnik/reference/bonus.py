def rectangle_area(a, b):
    return a * b


def rectangle_perimeter(a, b):
    return 2 * (a + b)


a = float(input("Zadej stranu a: "))
b = float(input("Zadej stranu b: "))

print(f"Obsah: {rectangle_area(a, b)}, obvod: {rectangle_perimeter(a, b)}")
