def normalize(numbers):
    min_value = min(numbers, default=0)
    max_value = max(numbers, default=0)

    return [
        round(
            (n - min_value) / (max_value - min_value)
            if max_value - min_value != 0
            else 0,
            2
        )
        for n in numbers
    ]


print(normalize([10, 15, 20]))


def count_above_average(numbers):
    if len(numbers) == 0:
        return 0

    avg = sum(numbers) / len(numbers)
    return len([i for i in numbers if i > avg])


print(count_above_average([12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]))
