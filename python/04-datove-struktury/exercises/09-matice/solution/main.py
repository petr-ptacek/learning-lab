def print_matrix(matrix):
    if not matrix:
        print("Empty matrix")
        return

    for row in matrix:
        for col in row:
            print(f"{col:>4}", end="")
        print()


print_matrix([[1, 2, 3], [4, 5, 6]])


def transpose_matrix(matrix):
    if len(matrix) == 0:
        return []

    result = []

    for colIndex in range(len(matrix[0])):
        row = []

        for rowIndex in range(len(matrix)):
            row.append(matrix[rowIndex][colIndex])

        result.append(row)

    return result


print(f"transpose matrix: {transpose_matrix([[1, 2, 3], [4, 5, 6]])}")


def row_sums(matrix):
    result = []

    for rowIdx in range(len(matrix)):
        summary = 0

        for colIdx in range(len(matrix[rowIdx])):
            summary += matrix[rowIdx][colIdx]

        result.append(summary)

    return result


print(f"row_sums: {row_sums([[1, 2, 3], [4, 5, 6]])}")


def column_sums(matrix):
    transposed = transpose_matrix(matrix)
    return row_sums(transposed)


print(f"column sums: {column_sums([[1, 2, 3], [4, 5, 6]])}")
