n = int(input("Zadej n: "))
k = int(input("Zadej k (vynechávané číslo): "))
k_2 = int(input("Zadej k2 (vynechávané číslo): "))

summary = 0
skipped = 0

for i in range(1, n + 1):
  if i % k == 0 or i % k_2 == 0:
    skipped += 1
    continue

  summary += i

print(f"Součet {summary}, přskočeno: {skipped} čísel")
