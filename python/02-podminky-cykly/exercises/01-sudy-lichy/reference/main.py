num = int(input("Zadej číslo: "))

parity = "liché" if num % 2 else "sudé"

if num > 0:
    sign = "kladné"
elif num < 0:
    sign = "záporné"
else:
    sign = "nula"

print(f"{num} je {parity}. {num} je {sign}.")
