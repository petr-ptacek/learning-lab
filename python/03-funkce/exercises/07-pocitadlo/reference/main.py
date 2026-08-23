balance = 0


def deposit(amount):
    global balance
    balance += amount


def withdraw(amount):
    global balance
    balance -= amount


while True:
    choice = input("Zadej volbu (p/o/k): ")

    if choice == "p":
        deposit(float(input("Zadej částku: ")))
        print(f"Zůstatek: {balance}")
    elif choice == "o":
        withdraw(float(input("Zadej částku: ")))
        print(f"Zůstatek: {balance}")
    elif choice == "k":
        print(f"Konec, zůstatek: {balance}")
        break
