items = []

while True:
    choice = input("Volba (p/o/n/x/v/k): ")

    if choice == "k":
        break
    elif choice in ("p", "n"):
        item = input("Položka: ")
        if item in items:
            print("Už v seznamu")
        elif choice == "p":
            items.append(item)
        else:
            position = int(input("Pozice: "))
            if position < 1:
                position = 1
            items.insert(position - 1, item)
    elif choice == "o":
        item = input("Položka: ")
        if item in items:
            items.remove(item)
        else:
            print("Není v seznamu")
    elif choice == "x":
        items.clear()
    elif choice == "v":
        if len(items) == 0:
            print("Seznam je prázdný")
        for i in range(len(items)):
            print(f"{i + 1}. {items[i]}")
    else:
        print("Neznámá volba")
