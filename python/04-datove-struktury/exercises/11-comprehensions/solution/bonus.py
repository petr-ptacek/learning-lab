from typing import Literal


def fizzbuzz(n):
    def checker(n: int) -> Literal["FizzBuzz", "Fizz", "Buzz"] | int:
        if n % 3 == 0 and n % 5 == 0:
            return "FizzBuzz"

        if n % 3 == 0:
            return "Fizz"

        if n % 5 == 0:
            return "Buzz"

        return n

    return [
        "FizzBuzz" if n % 3 == 0 and n % 5 == 0 else
        "Fizz" if n % 3 == 0 else
        "Buzz" if n % 5 == 0 else
        n
        for n in range(1, n + 1)
    ]


print(fizzbuzz(15))
print(fizzbuzz(0))


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if len(matrix) == 0:
        return []

    return [
        [matrix[rowIndex][colIndex] for rowIndex in range(len(matrix))] for colIndex in range(len(matrix[0]))
    ]


print(transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
