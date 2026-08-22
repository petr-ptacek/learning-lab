n = int(input("Zadej číslo: "))

is_prime = n >= 2

for divisor in range(2, n):
    if n % divisor == 0:
        is_prime = False
        break

print(f"{n} {'je' if is_prime else 'není'} prvočíslo")
