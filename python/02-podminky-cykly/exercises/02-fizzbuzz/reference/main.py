n = int(input("Zadej horní hranici: "))

for number in range(1, n + 1):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)

print(f"\n{'BONUS':-^30}\n")

divisor1 = int(input("Zadej první dělitel: "))
word1 = input("Zadej slovo pro první dělitel: ")

divisor2 = int(input("Zadej druhý dělitel: "))
word2 = input("Zadej slovo pro druhý dělitel: ")

for number in range(1, n + 1):
    if number % divisor1 == 0 and number % divisor2 == 0:
        print(word1 + word2)
    elif number % divisor1 == 0:
        print(word1)
    elif number % divisor2 == 0:
        print(word2)
    else:
        print(number)
