from collections.abc import Iterable


def manual_sum(iterable: Iterable[int]) -> int:
    it = iter(iterable)
    summary = 0
    default_value = object()

    while True:
        value = next(it, default_value)
        if value is default_value:
            break

        summary += value

    return summary


print(manual_sum(range(10)))
print(manual_sum([1, 2, 3]))
print(manual_sum(i for i in range(10) if i % 2 == 0))
