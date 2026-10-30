# vrati iterator
it = iter([10, 20, 30])
# 10
print(next(it))
# 20
print(next(it))
# 30
print(next(it))
# konec, bez konec hodi chybu neosetrena vyjimka StopIteration
print(next(it, "konec"))

print("\n" * 2)


def first(iterable, default=None):
    return next(iter(iterable), default)


print(first(range(50, 101, 50)))
print(first([50, 100]))
print(first({50, 100}))
print(first((50, 100)))
print(first({"a": "a", "b": "b"}))
print(first("abcdefg"))
print(first(map(str.upper, ["x", "y"])))
print(first([]))


def first_match(items, predicate, default=None):
    return next((i for i in items if predicate(i)), default)


print(first_match([10, 20, 30], lambda x: x == 50))
print(first_match(["kocka", "Pes", "Zebra"], str.istitle))


m = map(int, ["1", "2", "3"])
print(first(m))
# tohle uz nic [2,3]
print(list(m))
