def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def most_common(counts):
    best = None
    for word, count in counts.items():
        if best is None or count > best[1]:
            best = (word, count)
    return best


counts = count_words(input("Text: "))
for word, count in counts.items():
    print(f"{word}: {count}")

best = most_common(counts)
if best is None:
    print("Žádná slova")
else:
    word, count = best
    print(f"Nejčastější: {word} ({count}×)")
