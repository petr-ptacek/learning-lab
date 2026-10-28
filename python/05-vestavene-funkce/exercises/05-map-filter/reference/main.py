def parse_numbers(text):
    return list(map(int, text.split()))


def only_positive(numbers):
    return list(filter(lambda n: n > 0, numbers))


def only_positive_comprehension(numbers):
    return [n for n in numbers if n > 0]


def with_vat(prices, rate=0.21):
    return list(map(lambda price: round(price * (1 + rate), 2), prices))


def with_vat_comprehension(prices, rate=0.21):
    return [round(price * (1 + rate), 2) for price in prices]


for text in ["3 1 4", "  10   -2 0 ", ""]:
    print(parse_numbers(text))

for numbers in [[3, -1, 0, 5], [-1, 0], []]:
    print(only_positive(numbers), only_positive_comprehension(numbers))

print(with_vat([100, 24.9, 0]), with_vat_comprehension([100, 24.9, 0]))
print(with_vat([100, 24.9], 0.1), with_vat_comprehension([100, 24.9], 0.1))

# map vrací iterátor, ne seznam: první list() ho vyčerpá, druhý už dostane [].
numbers = map(int, ["1", "2", "3"])
print(list(numbers))
print(list(numbers))
