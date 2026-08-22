MAGIC_NUMBER = 50
MAX_ATTEMPTS = 7

current_attempt = 0

while True:
  user_number = int(input("Hádej číslo (1 - 100): "))
  current_attempt += 1

  if user_number > MAGIC_NUMBER:
    print("Míň")
  elif user_number < MAGIC_NUMBER:
    print("Víc")
  else:
    print(f"Uhodl jsi! Počet pokusů: {current_attempt}")
    break

  if current_attempt >= MAX_ATTEMPTS:
    print(f"Hra ukončena, počet pokusů překročen {current_attempt}.\nSprávné číslo: {MAGIC_NUMBER}")
    break
