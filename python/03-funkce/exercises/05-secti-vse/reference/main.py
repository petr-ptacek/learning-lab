def sum_all(*numbers):
    total = 0

    for number in numbers:
        total += number

    return total


a = int(input("Zadej a: "))
b = int(input("Zadej b: "))
c = int(input("Zadej c: "))

print(f"sum_all(a) = {sum_all(a)}")
print(f"sum_all(a, b) = {sum_all(a, b)}")
print(f"sum_all(a, b, c) = {sum_all(a, b, c)}")
