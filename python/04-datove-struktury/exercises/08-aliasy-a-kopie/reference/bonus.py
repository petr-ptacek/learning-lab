def copy_matrix(matrix):
    result = []
    for row in matrix:
        result.append(row.copy())
    return result


def create_grid(rows, cols, value=0):
    grid = []
    for _ in range(rows):
        grid.append([value] * cols)
    return grid


m = [[1, 2], [3, 4]]
c = copy_matrix(m)
c[0][0] = 9
print(m, c)
print(copy_matrix([]))

g = create_grid(2, 3)
g[0][0] = 1
print(g)
print(create_grid(1, 2, "-"))
print(create_grid(0, 3))
