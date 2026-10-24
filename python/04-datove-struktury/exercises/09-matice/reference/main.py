def print_matrix(matrix):
    if len(matrix) == 0:
        print("(prázdná)")
    for row in matrix:
        for value in row:
            print(f"{value:>4}", end="")
        print()


def transpose(matrix):
    if len(matrix) == 0:
        return []

    result = []
    for col in range(len(matrix[0])):
        new_row = []
        for row in matrix:
            new_row.append(row[col])
        result.append(new_row)
    return result


def row_sums(matrix):
    sums = []
    for row in matrix:
        total = 0
        for value in row:
            total += value
        sums.append(total)
    return sums


def col_sums(matrix):
    return row_sums(transpose(matrix))


for matrix in [[[1, 2, 3], [4, 5, 6]], [[1, 2], [3, 4]], [[7]], []]:
    print_matrix(matrix)
    print(f"transpose: {transpose(matrix)}, row_sums: {row_sums(matrix)}, col_sums: {col_sums(matrix)}")
    print()
