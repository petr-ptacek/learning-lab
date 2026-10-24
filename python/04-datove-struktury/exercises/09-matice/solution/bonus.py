def multiply(A: list[list[int]], B: list[list[int]]) -> list[list[int]] | None:
    if len(A) == 0 or len(B) == 0:
        return None

    if len(A[0]) != len(B):
        return None

    rows = len(A)
    cols = len(B[0])
    inner = len(B)


    result = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            for k in range(inner):
                result[i][j] += A[i][k] * B[k][j]

    return result


print(multiply([[1, 2], [3, 4]], [[1, 2], [3, 4]]))
