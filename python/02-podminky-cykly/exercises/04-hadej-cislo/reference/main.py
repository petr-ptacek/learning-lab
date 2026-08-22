MAGIC_NUMBER = 50
MAX_ATTEMPTS = 7

attempt = 0

while attempt < MAX_ATTEMPTS:
    guess = int(input("Hádej číslo (1-100): "))
    attempt += 1

    if guess == MAGIC_NUMBER:
        print(f"Uhodl jsi! Počet pokusů: {attempt}")
        break

    print("Míň" if guess > MAGIC_NUMBER else "Víc")
else:
    print(f"Prohra, číslo bylo {MAGIC_NUMBER}.")
