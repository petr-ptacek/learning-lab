import itertools
from collections.abc import Iterable


def chunked_any(iterable: Iterable, size: int) -> Iterable:
    it = iter(iterable)

    while chunk := list(itertools.islice(it, size)):
        yield chunk


# print(list(chunked_any(range(7), 3)))

# print(itertools.batched(range(7), 3))

# klasicke zpracovani dat po bathed
print(list(itertools.batched(range(7), 3)))

# vraci dvojice sousednich prvku, neco jako zip
print(list(itertools.pairwise([1, 2, 3, 4])))
