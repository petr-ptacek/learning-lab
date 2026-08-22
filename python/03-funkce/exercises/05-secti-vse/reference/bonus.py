def sum_all(*numbers):
    total = 0

    for number in numbers:
        total += number

    return total


def average(*numbers):
    if not numbers:
        return 0

    return sum_all(*numbers) / len(numbers)


print(average(2, 3, 5))
print(average(1, 1, 1))
print(average())
