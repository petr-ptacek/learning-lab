# A
a = [1, 2, 3]
b = a
b.append(4)
print(a)
# 1,2,3,4

# B
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)
# 1,2,3

# C
grid = [[0, 0], [0, 0]]
copy = grid.copy()
copy[0][0] = 9
print(grid)
# [[9,0][0,0]]


# D
row = [0] * 3
grid = [row] * 2
grid[0][0] = 1
print(grid)


# [[1,0,0],[1,0,0]]

# E
def add_item(item, items=[]):
    items.append(item)
    return items


print(add_item("a"))
# [a]
print(add_item("b"))


# [a,b]

# E1
def add_item_correct(item, items=None):
    return [*(items or []), item]


print(add_item_correct("a"))
print(add_item_correct("b"))


# F
def double_all(numbers):
    for i in range(len(numbers)):
        numbers[i] *= 2


values = [1, 2, 3]
double_all(values)
print(values)


# [2,4,6]


def remove_negatives(numbers):
    return [n for n in numbers if n >= 0]
