def stats(numbers):
    if not numbers:
        return None
    low, high, total = min(numbers), max(numbers), sum(numbers)
    return low, high, total, round(total / len(numbers), 2), high - low


def closest_to_zero(numbers):
    return min(numbers, key=abs, default=None)


for numbers in [[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5], [5.0], [-3.0, -1.5, -7.0], []]:
    print(stats(numbers))

for numbers in [[5, -2, 3, 2], [-4, 4], [0, 7], []]:
    print(closest_to_zero(numbers))
