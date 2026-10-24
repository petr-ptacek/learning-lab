def fizzbuzz(n):
    return [
        "FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i
        for i in range(1, n + 1)
    ]


def transpose(matrix):
    if len(matrix) == 0:
        return []
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]


print(fizzbuzz(15))
print(fizzbuzz(0))
print(transpose([[1, 2, 3], [4, 5, 6]]))
print(transpose([[7]]))
