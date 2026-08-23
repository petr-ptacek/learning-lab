add = lambda x, y: x + y
subtract = lambda x, y: x - y
multiply = lambda x, y: x * y
divide = lambda x, y: x / y

print_result = lambda x: print(f"Vysledek: {x}")


def get_numbers():
    num_a = float(input("Zadej cislo (A): "))
    num_b = float(input("Zadej cislo (B): "))

    return num_a, num_b


while True:
    op = input("Zadej operaci (+,-,*,/,k): ")

    match op:
        case "+":
            print_result(add(*get_numbers()))
        case "-":
            print_result(subtract(*get_numbers()))
        case "*":
            print_result(multiply(*get_numbers()))
        case "/":
            num_a, num_b = get_numbers()
            if num_b == float(0):
                print("Nelze dělit nulou")
            else:
                print_result(divide(num_a, num_b))
        case "k":
            break
