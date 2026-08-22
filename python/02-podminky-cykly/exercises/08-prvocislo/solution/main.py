num = int(input("Enter a number: "))

is_prime_number = True

if num < 2:
  print(f"{num} neni prvočíslo")
else:
  for divisor in range(2, num):
    if num % divisor == 0:
      is_prime_number = False
      break

  print(f"{num} {'je prvočíslo' if is_prime_number else 'není prvočíslo'}")