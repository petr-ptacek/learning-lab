def stats(numbers):
    if not numbers:
        return None

    maximum = max(numbers)
    minimum = min(numbers)
    summary = sum(numbers)
    avg = round(summary / len(numbers), 2)
    span = maximum - minimum

    return minimum, maximum, summary, avg, span


print(stats([12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]))


def closest_to_zero(numbers):
    return min(numbers, key=lambda n: abs(n), default=None)


for data in [[5, -2, 3, 2], [], [0, 7], [-4, 4]]:
    print(closest_to_zero(data))
