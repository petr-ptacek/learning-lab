words = ["kocka", "Pes", "slon", "auto", "Zebra", "mys"]


def sort_alpha(words):
    return sorted(words, key=str.lower)


def sort_by_length(words):
    return sorted(words, key=lambda word: (len(word), word.lower()))


def top_n(scores, n):
    return sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


# Velká písmena mají v Unicode nižší kódy než malá ('P' = 80, 'a' = 97),
# takže sorted() bez key dá slova s velkým písmenem dopředu.
print(sorted(words))
print(sort_alpha(words))
print(sort_by_length(words))
print(sort_alpha([]))

scores = {"Anna": 87, "Petr": 92, "Eva": 87, "Jana": 75}
for n in [2, 3, 10, 0]:
    print(top_n(scores, n))
print(top_n({}, 3))

result = sorted(words)
print(words is not result, words)
print(words.sort(), words)
