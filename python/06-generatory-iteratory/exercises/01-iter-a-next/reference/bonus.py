def manual_sum(iterable):
    # None ani 0 jako zarážka nefungují, mohou být přímo v datech.
    # Nový object() se s ničím jiným nerovná a "is" ho pozná jednoznačně.
    done = object()
    iterator = iter(iterable)
    total = 0
    while (value := next(iterator, done)) is not done:
        total += value
    return total


for numbers in [[1, 2, 3], [0, 0, 7], range(5), map(int, ["4", "5"]), []]:
    print(manual_sum(numbers))
