def count_words(text: str):
    state = dict()

    words = text.split()

    for word in words:
        w = word.lower()

        count = state.get(w, 0)
        state[w] = count + 1

    return state


def most_common(counts: dict):
    most = None

    for key, count in counts.items():
        if most is None or most[1] < count:
            most = (key, count)

    return most


text = input("Napis text: ")
counts = count_words(text)
most = most_common(counts)

for key, count in counts.items():
    print(f"{key}: {count}")

if most:
    print(f"Nejcastejsi {most[0]} ({most[1]}x)")
else:
    print("Zadna slova")
