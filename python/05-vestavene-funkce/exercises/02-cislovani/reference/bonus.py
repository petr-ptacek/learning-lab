def index_of_max(numbers):
    index, _ = max(enumerate(numbers), key=lambda pair: pair[1], default=(None, None))
    return index


for numbers in [[3, 9, 2, 9], [5], [-1, -5], []]:
    print(index_of_max(numbers))
