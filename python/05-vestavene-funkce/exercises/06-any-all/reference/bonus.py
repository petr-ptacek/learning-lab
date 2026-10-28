def is_sorted(numbers):
    return all(a <= b for a, b in zip(numbers, numbers[1:]))


def has_duplicates(numbers):
    return len(set(numbers)) < len(numbers)


for numbers in [[1, 2, 2, 3], [1, 3, 2], [3, 1], [5], []]:
    print(numbers, is_sorted(numbers), has_duplicates(numbers))
