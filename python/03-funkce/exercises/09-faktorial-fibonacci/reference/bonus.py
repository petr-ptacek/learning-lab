calls = 0


def factorial(n):
    global calls
    calls += 1
    if n <= 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


n = int(input("Zadej n: "))
print(f"{n}! = {factorial(n)}")
print(f"fibonacci({n}) = {fibonacci(n)}")
print(f"Počet volání: {calls}")
