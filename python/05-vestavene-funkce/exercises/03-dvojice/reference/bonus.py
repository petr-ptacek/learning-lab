def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


for matrix in [[[1, 2, 3], [4, 5, 6]], [[7]], []]:
    print(transpose(matrix))

try:
    pairs = list(zip(["Anna", "Petr", "Eva"], [90, 75], strict=True))
except ValueError as error:
    print(error)
