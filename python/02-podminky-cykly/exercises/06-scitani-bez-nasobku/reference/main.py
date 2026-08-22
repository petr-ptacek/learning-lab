n = int(input("Zadej n: "))
k = int(input("Zadej k (vynechávané číslo): "))

total = 0
skipped = 0

for number in range(1, n + 1):
    if number % k == 0:
        skipped += 1
        continue

    total += number

print(f"Součet: {total}, přeskočeno: {skipped} čísel")
