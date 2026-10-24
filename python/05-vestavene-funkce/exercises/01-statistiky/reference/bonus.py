def normalize(numbers):
    if not numbers:
        return []
    low, high = min(numbers), max(numbers)
    if low == high:
        return [0.0 for _ in numbers]
    return [round((n - low) / (high - low), 2) for n in numbers]


def count_above_average(numbers):
    if not numbers:
        return 0
    average = sum(numbers) / len(numbers)
    return sum(n > average for n in numbers)


for numbers in [[10, 15, 20], [-5, 0, 5, 10], [3, 3, 3], []]:
    print(normalize(numbers))

for numbers in [[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5], [5.0], []]:
    print(count_above_average(numbers))
