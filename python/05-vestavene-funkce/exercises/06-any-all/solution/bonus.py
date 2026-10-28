def is_sorted(numbers):
    return all(b >= a for a, b in zip(numbers, numbers[1:]))


print(is_sorted([1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(is_sorted([1, 2, 3, 4, 0, 6, 7, 8, 9]))


def has_duplicates(numbers):
    return len(set(numbers)) != len(numbers)


print(has_duplicates([1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(has_duplicates([1, 2, 3, 4, 5, 6, 7, 8, 9, 9]))
