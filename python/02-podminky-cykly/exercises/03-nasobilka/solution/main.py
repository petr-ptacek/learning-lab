number = int(input("Zadej číslo: "))

for multiplier in range(1, 11):
  result = number * multiplier

  number_str = f"{number:>2}"
  multiplier_str = f"{multiplier:>2}"
  result_str = f"{result:>2}"

  message = "{number} x {multiplier} = {result}".format(
      number=number_str,
      multiplier=multiplier_str,
      result=result_str
  )

  print(message)

print(f"\n{'BONUS':x^20}\n")

for number in range(1, 11):

  for multiplier in range(1, 11):
    result = number * multiplier

    number_str = f"{number:>2}"
    multiplier_str = f"{multiplier:>2}"
    result_str = f"{result:>2}"

    message = "{number} x {multiplier} = {result}".format(
        number=number_str,
        multiplier=multiplier_str,
        result=result_str
    )

    print(message)

  print("-" * 20)
