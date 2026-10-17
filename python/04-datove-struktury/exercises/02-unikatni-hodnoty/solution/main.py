def unique(items: list) -> list:
    result = list()

    for item in items:
        if item not in result:
            result.append(item)

    return result


def reverse(items: list) -> list:
    result = []

    for idx in range(-1, -(len(items) + 1), -1):
        result.append(items[idx])

    return result


def duplicities(items: list) -> list:
    result = list()

    for item in items:
        if items.count(item) > 1 and item not in result:
            result.append(item)

    return result


for t in [
    [1, 2, 2, 3, 1],
    ["a", "A", "a"],
    [],
    [5, 5, 5],
    [3, 2, 1]
]:
    u = unique(t[:])
    r = reverse(t[:])
    d = duplicities(t[:])

    reversed_ok = t[::-1] == r

    print(
        f"original: {t}, unique: {u}, reverse: {r}, duplicities: {d}, reversed_ok: {reversed_ok}"
    )
