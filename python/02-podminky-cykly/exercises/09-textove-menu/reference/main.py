while True:
    print("1 - spočítej samohlásky ve slově")
    print("2 - obrať pořadí znaků slova")
    print("0 - konec")

    choice = input("Zadej volbu: ")

    if choice == "1":
        word = input("Zadej slovo: ").lower()
        vowels = 0

        for letter in word:
            if letter in "aeiouy":
                vowels += 1

        print(f"Počet samohlásek: {vowels}")

    elif choice == "2":
        word = input("Zadej slovo: ")
        reversed_word = ""

        for letter in word:
            reversed_word = letter + reversed_word

        print(reversed_word)

    elif choice == "0":
        print("Konec, ahoj!")
        break

    else:
        print("Neznámá volba")
