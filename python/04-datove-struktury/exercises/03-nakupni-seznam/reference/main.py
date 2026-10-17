items = []

while True:
    choice = input("Volba (p/o/v/k): ")

    if choice == "k":
        break
    elif choice == "p":
        item = input("Položka: ")
        if item in items:
            print("Už v seznamu")
        else:
            items.append(item)
    elif choice == "o":
        item = input("Položka: ")
        if item in items:
            items.remove(item)
        else:
            print("Není v seznamu")
    elif choice == "v":
        if len(items) == 0:
            print("Seznam je prázdný")
        for i in range(len(items)):
            print(f"{i + 1}. {items[i]}")
    else:
        print("Neznámá volba")
