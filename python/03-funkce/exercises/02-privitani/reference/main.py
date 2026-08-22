def greet(name, greeting="Ahoj"):
    return f"{greeting}, {name}!"


name = input("Zadej jméno: ")
greeting = input("Zadej pozdrav (nebo nic pro výchozí): ")

if greeting:
    print(greet(name, greeting))
else:
    print(greet(name))
