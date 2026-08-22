number = int(input("Zadej číslo: "))

for multiplier in range(1, 11):
    result = number * multiplier
    print(f"{number:>2} x {multiplier:>2} = {result:>2}")

print(f"\n{'BONUS':-^20}\n")

for number in range(1, 11):
    for multiplier in range(1, 11):
        result = number * multiplier
        print(f"{number:>2} x {multiplier:>2} = {result:>2}")
    print("-" * 20)
