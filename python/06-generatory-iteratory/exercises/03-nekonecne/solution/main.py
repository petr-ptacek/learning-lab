from collections.abc import Iterable


def naturals(start=1) -> Iterable[int]:
    while True:
        yield start
        start += 1


def fibonacci() -> Iterable[int]:
    a, b = 0, 1

    while True:
        yield a
        a, b = b, a + b


def first_fib_over(limit):
    return next(f for f in fibonacci() if f > limit)


def take(iterable: Iterable, n: int) -> Iterable:
    return [entry[1] for entry in zip(range(n), iterable)]


print(take(naturals(10), 5))
print(take(fibonacci(), 10))
print(take("python", 3))
