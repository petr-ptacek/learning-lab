n = int(input("Zadej číslo: "))

primes_str = ""

for candidate in range(2, n + 1):
    is_prime = True

    for divisor in range(2, candidate):
        if candidate % divisor == 0:
            is_prime = False
            break

    if not is_prime:
        continue

    if primes_str:
        primes_str += ", "
    primes_str += str(candidate)

print(primes_str)
