from collections.abc import Iterable, Iterator


def naturals(start: int = 1) -> Iterator[int]:
    while True:
        yield start
        start += 1


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take[T](iterable: Iterable[T], n: int) -> list[T]:
    return [item for _, item in zip(range(n), iterable)]


def first_fib_over(limit: int) -> int:
    return next(f for f in fibonacci() if f > limit)


# list(naturals()) se nikdy nedokončí: generátor nemá konec,
# list by ho četl donekonečna a paměť by rostla, dokud program nespadne.

print(take(naturals(), 5))
print(take(naturals(10), 3))
print(take(fibonacci(), 10))
print(take("python", 3))
print(take([1, 2], 5))
print(take(fibonacci(), 0))

for limit in [100, 1000, 1, 0]:
    print(first_fib_over(limit))
