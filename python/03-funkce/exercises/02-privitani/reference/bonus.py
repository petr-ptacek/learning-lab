def greet(name, greeting="Ahoj", exclamation_count=1):
    return f"{greeting}, {name}{'!' * exclamation_count}"


name = input("Zadej jméno: ")
greeting = input("Zadej pozdrav (nebo nic pro výchozí): ")
exclamation_count = int(input("Zadej počet vykřičníků (nebo nic pro výchozí): ") or "1")

if greeting:
    print(greet(name, greeting, exclamation_count=exclamation_count))
else:
    print(greet(name, exclamation_count=exclamation_count))
