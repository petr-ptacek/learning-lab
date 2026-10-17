def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    if n == 0 or n == 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def main1():
    cases = [
        5, 0, 6, 1
    ]

    print(f"{"Case":^12}|{"factorial":^12}|{"fibonacci":^12}")
    print("-" * (12 * 3))

    for case in cases:
        fac = factorial(case)
        fib = fibonacci(case)

        print(f"{f"{case}":^12}|{f"{fac}":^12}|{f"{fib}":^12}")


def main():
    n = int(input("Type a number: "))
    fac = factorial(n)
    fib = fibonacci(n)

    print(f"{n}! = {fac}, fibonacci({n}) = {fib}")


main()
