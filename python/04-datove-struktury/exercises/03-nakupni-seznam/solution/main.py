running = True
shopping_list = list()

while running:
    selection = input("Volba (p/o/v/k/n/x): ")

    if selection == "p":
        item = input("Polozka: ")

        if item in shopping_list:
            print("Uz v seznamu")
        else:
            shopping_list.append(item)

    elif selection == "o":
        item = input("Polozka: ")

        if item not in shopping_list:
            print("Neni v seznamu")
        else:
            shopping_list.remove(item)

    elif selection == "n":
        item = input("Polozka: ")
        index = int(input("Pozice: ")) - 1

        if item in shopping_list:
            print("Uz v seznamu")
        else:
            shopping_list.insert(index, item)


    elif selection == "x":
        shopping_list.clear()
        print("Seznam smazan")

    elif selection == "v":
        if len(shopping_list) == 0:
            print("Seznam je prazdny")
        else:
            for idx in range(len(shopping_list)):
                print(f"{idx + 1}. {shopping_list[idx]}")

    elif selection == "k":
        running = False

    else:
        print("Neznama volba")
