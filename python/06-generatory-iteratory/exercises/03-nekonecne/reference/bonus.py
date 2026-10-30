from collections.abc import Iterable, Iterator
from itertools import count, islice, takewhile


def naturals(start: int = 1) -> Iterator[int]:
    while True:
        yield start
        start += 1


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# zip bere v každém kole nejdřív z prvního vstupu.
# zip(g, range(3)): ve 4. kole vytáhne z g číslo 4, pak zjistí,
# že range došel, a 4 zahodí -> next(g) vrátí 5.
# zip(range(3), g): ve 4. kole skončí už na range, do g nesáhne
# -> next(g) vrátí 4. Pro take je správně tohle pořadí.
g = naturals()
print(list(zip(g, range(3))), next(g))
g = naturals()
print(list(zip(range(3), g)), next(g))


def take_it[T](iterable: Iterable[T], n: int) -> list[T]:
    return list(islice(iterable, n))


def fib_below(limit: int) -> list[int]:
    return list(takewhile(lambda f: f < limit, fibonacci()))


print(take_it(naturals(), 5))
print(take_it([1, 2], 5))

for limit in [50, 1, 0]:
    print(fib_below(limit))

print(list(islice(count(10, 5), 4)))
