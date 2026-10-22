running = True
phone_dict = dict()

while running:
    choice = input("Volba (p/h/s/v/k/c/r): ")

    if choice == "p":
        name = input("Jmeno: ")
        phone = input("cislo: ").strip() or None

        if not phone:
            print("Nebylo zadano telefonni cislo")
        else:
            if name in phone_dict:
                print("Aktualizovano")
            else:
                print("Pridano")

            phone_dict[name] = phone

    elif choice == "r":
        p = input("cislo: ")
        founded = None

        for name, phone in phone_dict.items():
            if p == phone:
                founded = (name, phone)
                break

        if founded:
            print(f"{founded[0]}")
        else:
            print("Nenalezeno")

    elif choice == "c":
        n = input("Jmeno: ").strip().lower()
        founded = False

        for name, phone in phone_dict.items():
            if n in name.lower():
                print(f"{name}: {phone}")
                founded = True

        if not founded:
            print("Nenalezeno")

    elif choice == "h":
        name = input("Jmeno: ")
        phone = phone_dict.get(name, None)

        if not phone:
            print("Nenalezeno")
        else:
            print(phone)

    elif choice == "s":
        name = input("Jmeno: ")
        phone = phone_dict.get(name, None)

        if phone:
            phone_dict.pop(name)
            print("Smazano")
        else:
            print("Nenalezeno")

    elif choice == "v":
        if len(phone_dict) == 0:
            print("Seznam je prazdny")
        else:
            for name, phone in phone_dict.items():
                print(f"{name}: {phone}")

    elif choice == "k":
        running = False
