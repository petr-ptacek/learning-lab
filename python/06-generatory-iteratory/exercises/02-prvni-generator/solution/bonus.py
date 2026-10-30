from collections.abc import Iterable


def running_total(numbers: Iterable) -> Iterable[int]:
    total = 0
    for number in numbers:
        total += number
        yield total


for sequence in [[1, 2, 3, 4], [5, -5, 2], []]:
    print(list(running_total(sequence)))


def with_index(items: Iterable, start=0):
    index = start
    value = None
    iterator = iter(items)
    default_value = object()

    while (value := next(iterator, default_value)) is not default_value:
        yield index, value
        index += 1


for sequence, start in [(["x", "y"], 1), ("abc", 1)]:
    print(list(with_index(sequence, start)))
