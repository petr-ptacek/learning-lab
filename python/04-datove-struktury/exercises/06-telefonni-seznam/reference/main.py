contacts = {}

while True:
    choice = input("Volba (p/h/s/v/k): ")

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
