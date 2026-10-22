contacts = {}

while True:
    choice = input("Volba (p/h/s/v/c/r/k): ")

    if choice == "k":
        break
    elif choice == "p":
        name = input("Jméno: ")
        phone = input("Číslo: ")
        print("Aktualizováno" if name in contacts else "Přidáno")
        contacts[name] = phone
    elif choice == "h":
        print(contacts.get(input("Jméno: "), "Nenalezeno"))
    elif choice == "s":
        name = input("Jméno: ")
        if contacts.pop(name, None) is None:
            print("Nenalezeno")
        else:
            print("Smazáno")
    elif choice == "v":
        if len(contacts) == 0:
            print("Seznam je prázdný")
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    elif choice == "c":
        query = input("Část jména: ").lower()
        found = False
        for name, phone in contacts.items():
            if query in name.lower():
                print(f"{name}: {phone}")
                found = True
        if not found:
            print("Nenalezeno")
    elif choice == "r":
        number = input("Číslo: ")
        for name, phone in contacts.items():
            if phone == number:
                print(name)
                break
        else:
            print("Nenalezeno")
