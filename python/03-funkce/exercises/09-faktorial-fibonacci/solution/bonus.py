calls_factorial = 0
calls_fibonacci = 0


def factorial(n):
    global calls_factorial
    calls_factorial += 1

    if n <= 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    global calls_fibonacci
    calls_fibonacci += 1

    if n == 0 or n == 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    n = int(input("Type a number: "))
    fac = factorial(n)
    fib = fibonacci(n)

    print(f"{n}! = {fac} (pocet volani {calls_factorial}), fibonacci({n}) = {fib} (pocet volani {calls_fibonacci})")


main()
