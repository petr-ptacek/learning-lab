def noisy():
    print("start")
    yield 1
    print("mezi")
    yield 2
    print("konec")


gen = noisy()
print("vytvořeno")  # vytvořeno — tělo funkce zatím neběželo
print(next(gen))  # start, 1
print(next(gen))  # mezi, 2
print(list(gen))  # konec, []
print(type(noisy()))  # <class 'generator'>


def countdown(n):
    while n > 0:
        yield n
        n -= 1


def evens(limit):
    yield from range(0, limit, 2)


def repeat(value, times):
    for _ in range(times):
        yield value


for n in [3, 1, 0, -2]:
    print(list(countdown(n)))

for limit in [7, 8, 1, 0]:
    print(list(evens(limit)))

print(list(repeat("ab", 3)))
print(list(repeat("x", 0)))
