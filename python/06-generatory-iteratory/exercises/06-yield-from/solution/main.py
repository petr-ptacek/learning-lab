from collections.abc import Iterable, Iterator


def chain[T](*iterables: Iterable[T]) -> Iterator[T]:
    for iterable in iterables:
        yield from iterable


print(list(chain([1, 2], "ab", range(2))))
print(list(chain([], range(2))))


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print(list(flatten([1, [2, [3, [4]]], 5])))
