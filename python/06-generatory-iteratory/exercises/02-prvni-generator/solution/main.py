def noisy():
    print("start")
    yield 1
    print("mezi")
    yield 2
    print("konec")


# gen = noisy()
# vrati object iterator

# print("vytvořeno")
# print(next(gen))  # dojde k prvnimu vyhodnoceni, proto se vypise start, a potom 1 a nasledne se usne
# print(next(gen))  # mezi 2
# print(list(gen))  # konec, prazdny seznam


def countdown(n):
    for i in range(n, 0, -1):
        yield i


# print(list(countdown(3)))


def evens(limit):
    for i in range(0, limit, 2):
        yield i


print(list(evens(8)))


def repeat(value, times):
    for i in range(times):
        yield value


print(list(repeat(5, 2)))
print(list(repeat("ab", 2)))
