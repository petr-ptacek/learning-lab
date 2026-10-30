import itertools
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


# g = naturals()
# print(list(zip(g, range(3))))
# (1,0),(2,1),(3,2)
# print(next(g))
# 5

# g = naturals()
# print(list(zip(range(3), g)))
# (0,1),(1,2),(2,3)
# print(next(g))
#  4
# tato verze je spravna pro take


def take_it(iterable: Iterable, n: int) -> Iterable:
    return list(itertools.islice(iterable, n))


# print(list(take_it(naturals(), 30)))


def fib_below(limit):
    return list(itertools.takewhile(lambda x: x < limit, fibonacci()))


# print(list(fib_below(30)))
print(list(itertools.islice(itertools.count(10, 5), 4)))
