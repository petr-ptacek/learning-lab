from collections.abc import Iterable, Iterator


def chain[T](*iterables: Iterable[T]) -> Iterator[T]:
    for iterable in iterables:
        yield from iterable


def flatten(nested: list) -> Iterator:
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


# Základní případ: prvek, který není seznam, se vydá a rekurze dál nejde.
# Prázdný seznam rekurzi zastaví taky, cyklus se neprovede ani jednou.

print(list(chain([1, 2], "ab", range(2))))
print(list(chain([], [3])))
print(list(chain()))

print(list(flatten([1, [2, [3, [4]]], 5])))
print(list(flatten([1, 2, 3])))
print(list(flatten(["ab", ["cd"]])))
print(list(flatten([[], [[]]])))
print(list(flatten([])))
