def group_by_length(text):
    result = dict()

    for word in text.lower().split():
        t = result.get(len(word), [])

        if not word in t:
            result[len(word)] = [*t, word]

    return result


text = input("Zadej text: ")
print(group_by_length(text))
