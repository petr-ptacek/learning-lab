balance = 0


def deposit(amount):
    global balance
    balance += amount


def withdraw(amount):
    global balance
    balance -= amount


def get_user_amount():
    return float(input("Zadej castku: "))


while True:
    choice = input("Zadej volbu (p/o/k): ")

    if choice == "p":
        amount = get_user_amount()
        deposit(amount)
        print(f"Zustatek: {balance}")
    elif choice == "o":
        amount = get_user_amount()
        withdraw(amount)
        print(f"Zustatek: {balance}")
    elif choice == "k":
        print(f"Konec, zustatek: {balance}")
        break
