it = iter([10, 20, 30])
print(next(it))           # 10
print(next(it))           # 20
print(next(it))           # 30
print(next(it, "konec"))  # konec — bez defaultu by next vyhodil StopIteration


def first(iterable, default=None):
    return next(iter(iterable), default)


def first_match(items, predicate, default=None):
    return next((item for item in items if predicate(item)), default)


for iterable in [[5, 6], "abc", range(3, 10), {"a": 1, "b": 2}, map(str.upper, ["x", "y"]), [], {}]:
    print(first(iterable))
print(first([], "nic"))

print(first_match([1, 4, 7, 10], lambda n: n > 5))
print(first_match([1, 2], lambda n: n > 5))
print(first_match(["kocka", "Pes", "Zebra"], str.istitle))
print(first_match([], bool, "nic"))

# first si z iterátoru vezme jen jednu hodnotu, zbytek v něm zůstane.
m = map(int, ["1", "2", "3"])
print(first(m))   # 1
print(list(m))    # [2, 3]
