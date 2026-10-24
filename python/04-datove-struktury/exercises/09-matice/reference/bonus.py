def multiply(a, b):
    if len(a) == 0 or len(b) == 0 or len(a[0]) != len(b):
        return None

    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            total = 0
            for k in range(len(b)):
                total += a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result


for a, b in [
    ([[1, 2], [3, 4]], [[5, 6], [7, 8]]),
    ([[1, 0], [0, 1]], [[4, 5], [6, 7]]),
    ([[1, 2, 3]], [[1], [2], [3]]),
    ([[1, 2]], [[1, 2]]),
    ([], [[1]]),
]:
    print(multiply(a, b))
