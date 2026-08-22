upper_bound = int(input("Zadej cislo: "))
prime_numbers_str = ""

for idx, num in enumerate(range(2, upper_bound + 1)):

  is_prime_number = True

  for divisor in range(2, num):
    if num % divisor == 0:
      is_prime_number = False
      break

  if is_prime_number:
    if idx > 0:
      prime_numbers_str += f", {num}"
    else:
      prime_numbers_str += f"{num}"

print(f"{upper_bound}: {prime_numbers_str}")
