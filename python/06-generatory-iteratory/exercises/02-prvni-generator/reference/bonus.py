from collections.abc import Iterable, Iterator


def running_total(numbers: Iterable[int]) -> Iterator[int]:
    total = 0
    for number in numbers:
        total += number
        yield total


def with_index[T](items: Iterable[T], start: int = 0) -> Iterator[tuple[int, T]]:
    index = start
    for item in items:
        yield index, item
        index += 1


for numbers in [[1, 2, 3, 4], [5, -5, 2], []]:
    print(list(running_total(numbers)))

print(list(with_index("abc")))
print(list(with_index(["x", "y"], 1)))
print(list(with_index([])))
print(list(with_index("abc", 5)) == list(enumerate("abc", 5)))
