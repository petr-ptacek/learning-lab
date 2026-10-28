def parse_numbers(text):
    chunks = text.split()
    return list(map(int, chunks))


print(parse_numbers("1 2 3 4 5"))


def only_positive(numbers):
    return list(filter(lambda x: x > 0, numbers))


print(only_positive([1, 2, 3, 4, 5]))


def only_positive_comprehension(numbers):
    return [n for n in numbers if n > 0]


print(only_positive_comprehension([1, 2, 3, 4, 5]))


def with_vat(prices, rate=0.21):
    return list(map(lambda price: round(price * (1 + rate), 2), prices))


print(with_vat([100, 24.9], 0.1))


def with_vat_comprehension(prices, rate=0.21):
    return [round(price * (1 + rate), 2) for price in prices]


print(with_vat_comprehension([100, 24.9], 0.1))

# truthy values, like js [].filter(Boolean)
print(list(filter(None, ["", "a", 0, 1, None, [], [0]])))
