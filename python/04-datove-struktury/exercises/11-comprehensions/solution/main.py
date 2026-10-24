def squares(n: int) -> list:
    return [i ** 2 for i in range(1, n + 1)]


def evens(n: int) -> list:
    return [i for i in range(1, n + 1) if i % 2 == 0]


def odds(n: int) -> list:
    return [i for i in range(n) if i % 2 != 0]


def word_lengths(words: list[str]) -> dict[str, int]:
    return {
        w: len(w) for w in words
    }


def first_letters(words: list[str]):
    return { w[0].lower() for w in words }


def long_upper(words: list[str], min_len: int):
    return [w.upper() for w in words if len(w) > min_len]


def flatten(matrix: list[list[int]]) -> list:
    # result = []

    # for row in matrix:
    #     for col in row:
    #         result.append(col)

    return [
        col for row in matrix for col in row
    ]

    return result


def invert(d):
    return { v: k for k, v in d.items() }


print(word_lengths(["pes", "kocka", "mys"]))
print(flatten([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
print(invert({ "a": 1, "b": 2, "c": 3 }))
