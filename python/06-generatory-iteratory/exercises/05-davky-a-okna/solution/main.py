def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


# print(list(chunked([1, 2, 3, 4, 5, 6, 7], 3)))
# print(list(chunked([1, 2, 3, 4], 2)))
# print(list(chunked("abcde", 2)))
# print(list(chunked([], 2)))


def sliding_window(items, size):
    count = len(items)
    idx = 0

    while idx + size <= count:
        yield tuple(items[idx : idx + size])
        idx += 1


# print(list(sliding_window([1, 2, 3, 4], 3)))
# print(list(sliding_window("abcd", 2)))
# print(list(sliding_window([], 2)))
# print(list(sliding_window([1, 2], 3)))


def moving_average(numbers, size):
    windows = sliding_window(numbers, size)

    return [round(sum(window) / len(window), 2) for window in windows]


print(moving_average([10, 20, 30, 40, 50], 3))
print(moving_average([1, 2, 4], 2))
print(moving_average([5], 2))
