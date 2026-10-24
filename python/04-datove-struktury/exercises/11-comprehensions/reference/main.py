def squares(n):
    return [x ** 2 for x in range(1, n + 1)]


def squares_loop(n):
    result = []
    for x in range(1, n + 1):
        result.append(x ** 2)
    return result


def evens(n):
    return [x for x in range(1, n + 1) if x % 2 == 0]


def word_lengths(words):
    return {word: len(word) for word in words}


def first_letters(words):
    return {word[0] for word in words}


def long_upper(words, min_len):
    return [word.upper() for word in words if len(word) > min_len]


def flatten(matrix):
    return [value for row in matrix for value in row]


def invert(d):
    return {value: key for key, value in d.items()}


print(squares(5), squares_loop(5), squares(0))
print(evens(10), evens(1))
print(word_lengths(["pes", "kocka", "slon", "pes"]))
print(first_letters(["pes", "papoušek", "kocka", "koza"]), first_letters([]))
print(long_upper(["pes", "kocka", "slon"], 3), long_upper(["pes"], 5))
print(flatten([[1, 2], [3], [4, 5, 6]]), flatten([[], []]))
print(invert({"a": 1, "b": 2, "c": 3}))
# duplicitní hodnota 1 se stane dvakrát klíčem, pozdější "b" přepíše "a"
print(invert({"a": 1, "b": 1}))
