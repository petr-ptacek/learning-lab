from collections.abc import Iterator, Sequence


def chunked[T](items: Sequence[T], size: int) -> Iterator[Sequence[T]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def sliding_window[T](items: Sequence[T], size: int) -> Iterator[tuple[T, ...]]:
    for start in range(len(items) - size + 1):
        yield tuple(items[start : start + size])


def moving_average(numbers: Sequence[float], size: int) -> list[float]:
    return [round(sum(window) / size, 2) for window in sliding_window(numbers, size)]


print(list(chunked([1, 2, 3, 4, 5, 6, 7], 3)))
print(list(chunked([1, 2, 3, 4], 2)))
print(list(chunked([1, 2], 5)))
print(list(chunked("abcde", 2)))
print(list(chunked([], 3)))

print(list(sliding_window([1, 2, 3, 4], 3)))
print(list(sliding_window("abcd", 2)))
print(list(sliding_window([1, 2, 3], 1)))
print(list(sliding_window([1, 2], 3)))
print(list(sliding_window([], 2)))

print(moving_average([10, 20, 30, 40, 50], 3))
print(moving_average([1, 2, 4], 2))
print(moving_average([5], 2))
