# A — b je alias, ne kopie: [1, 2, 3, 4]
a = [1, 2, 3]
b = a
b.append(4)
print(a)

# B — copy() vytvoří nový seznam: [1, 2, 3]
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)

# C — mělká kopie sdílí vnitřní seznamy: [[9, 0], [0, 0]]
grid = [[0, 0], [0, 0]]
copy = grid.copy()
copy[0][0] = 9
print(grid)

# D — oba řádky jsou tentýž seznam row: [[1, 0, 0], [1, 0, 0]]
row = [0] * 3
grid = [row] * 2
grid[0][0] = 1
print(grid)


# E — původní items=[] vznikne jednou při definici funkce, takže vypíše
# ['a'] a pak ['a', 'b']; opravená verze vytvoří nový seznam při každém volání
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item("a"))
print(add_item("b"))
print(add_item("c", ["x"]))


# F — funkce mění seznam volajícího: [2, 4, 6]
def double_all(numbers):
    for i in range(len(numbers)):
        numbers[i] *= 2


values = [1, 2, 3]
double_all(values)
print(values)


def remove_negatives(numbers):
    result = []
    for number in numbers:
        if number >= 0:
            result.append(number)
    return result


def remove_negatives_broken(numbers):
    for number in numbers:
        if number < 0:
            numbers.remove(number)
    return numbers


for numbers in [[1, -2, -3, 4], [-1, -2, 3], [0, 5], []]:
    print(numbers, "->", remove_negatives(numbers), "| původní:", numbers)

# remove() posune zbytek doleva, takže cyklus další prvek přeskočí: [-2, 3]
print(remove_negatives_broken([-1, -2, 3]))
