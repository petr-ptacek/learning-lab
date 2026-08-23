add = lambda a, b: a + b
subtract = lambda a, b: a - b
multiply = lambda a, b: a * b
divide = lambda a, b: a / b

while True:
    op = input("Zadej operaci (+ - * / k): ")

    if op == "k":
        break

    a = float(input("Zadej a: "))
    b = float(input("Zadej b: "))

    if op == "+":
        print(f"Výsledek: {add(a, b)}")
    elif op == "-":
        print(f"Výsledek: {subtract(a, b)}")
    elif op == "*":
        print(f"Výsledek: {multiply(a, b)}")
    elif op == "/":
        if b == 0:
            print("Nelze dělit nulou")
        else:
            print(f"Výsledek: {divide(a, b)}")
