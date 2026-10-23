def copy_matrix(matrix):
    result = []

    for row in matrix:
        result.append(row.copy())

    return result


m = [[1, 2], [3, 4]]
c = copy_matrix(m)
c[0][0] = 9
print(m)


def create_grid(rows: int, cols: int, value: str | int = 0):
    # grid = [[value] * cols for _ in range(rows)]
    grid = []

    return [[value for _ in range(cols)] for _ in range(rows)]

    # for i in range(rows):
    #     row = []
    #     for j in range(cols):
    #         row.append(value)
    #
    # return grid


print(create_grid(3, 2, "X"))
