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
