num = int(input("Zadej cislo: "))

# liche
is_odd = bool(num % 2)

message = ""

if is_odd:
  message = f"{num} je liche."
else:
  message = f"{num} je sude."

if num > 0:
  message += f" {num} je kladne."
elif num < 0:
  message += f" {num} je zaporne."
else:
  message += f" {num} je nula."

print(message)