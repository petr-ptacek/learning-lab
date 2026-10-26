words = ["kocka", "Pes", "slon", "auto", "Zebra", "mys"]
scores = {"Anna": 87, "Petr": 92, "Eva": 87, "Jana": 75}


def sort_alpha(words: list) -> list:
    return sorted(words, key=str.lower)


print(sort_alpha(words))


def sort_by_length(words: list) -> list:
    return sorted(words, key=lambda w: (len(w), w.lower()))


print(sort_by_length(words))


def top_n(scores: dict, n: int) -> list:
    return sorted(scores.items(), key=lambda pair: (pair[1] * -1, pair[0].lower()))[:n]


print(top_n(scores, 10))


# seradi slova prodle asci znaku, tedy podle asci hodnot
print(sorted(words))

words_copy = words.copy()
print(sorted(words))
print(words_copy == words)
