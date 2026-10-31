from collections.abc import Iterable, Iterator
from itertools import batched, islice, pairwise


def naturals(start: int = 1) -> Iterator[int]:
    while True:
        yield start
        start += 1


def chunked_any[T](iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk


print(list(chunked_any(range(7), 3)))
print(list(chunked_any(iter([]), 2)))
print(list(islice(chunked_any(naturals(), 2), 3)))

# batched = chunked_any, pairwise = sliding_window(..., 2); obě vydávají tuply
print(list(batched(range(7), 3)))
print(list(pairwise([1, 2, 3, 4])))
