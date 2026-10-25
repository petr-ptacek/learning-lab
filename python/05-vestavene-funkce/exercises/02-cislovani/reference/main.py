def print_numbered(items, start=1):
    if not items:
        print("Seznam je prázdný")
        return
    for number, item in enumerate(items, start=start):
        print(f"{number}. {item}")


def indexes_of(items, value):
    return [index for index, item in enumerate(items) if item == value]


print_numbered(["mléko", "chleba"])
print_numbered(["mléko", "chleba"], start=0)
print_numbered([])

for items, value in [(["a", "b", "a", "c", "a"], "a"), ([1, 2, 1], 1), (["a", "b"], "z"), ([], "a")]:
    print(indexes_of(items, value))
