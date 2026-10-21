def group_by_length(text):
    groups = {}
    for word in text.lower().split():
        length = len(word)
        if length not in groups:
            groups[length] = []
        if word not in groups[length]:
            groups[length].append(word)
    return groups


for text in ["a b a", "Pes pes PES kocka", "jedna dva tri dva jedna jedna", "kolo auto kolo vlak auto", ""]:
    print(f"{text!r}: {group_by_length(text)}")
