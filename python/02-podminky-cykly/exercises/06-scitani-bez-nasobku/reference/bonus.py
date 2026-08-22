n = int(input("Zadej n: "))
k1 = int(input("Zadej k1 (vynechávané číslo): "))
k2 = int(input("Zadej k2 (vynechávané číslo): "))

total = 0
skipped = 0

for number in range(1, n + 1):
    if number % k1 == 0 or number % k2 == 0:
        skipped += 1
        continue

    total += number

print(f"Součet: {total}, přeskočeno: {skipped} čísel")
