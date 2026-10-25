def print_numbered(items, start=1):
    if not items:
        print("No items to print")
        return

    for index, item in enumerate(items, start=start):
        print(f"{index} - {item}")


print_numbered(["Mleko", "Kafe", "Mouka"], 1)


def indexes_of(items, value):
    return [index for index, item in enumerate(items) if item == value]


print(indexes_of([1, 2, 3, 4, 1, 0, 10, 1], 1))


def index_of_max(numbers):
    index, _ = max(enumerate(numbers), key=lambda x: x[1], default=(None, None))
    return index


print(index_of_max([3, 9, 2, 9]))
