def sum_all(*numbers):
    total = 0
    for number in numbers:
        total += number
    return total


def average(*numbers):
    sum = sum_all(*numbers)

    return sum / (len(numbers) or 1)


print(f"{average(2, 3, 5):.2f}")
print(f"{average(1, 1, 1):.2f}")
print(f"{average():.2f}")
