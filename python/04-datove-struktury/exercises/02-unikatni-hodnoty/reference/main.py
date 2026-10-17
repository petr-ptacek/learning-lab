def unique(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def reverse(items):
    result = []
    for item in items:
        result.insert(0, item)
    return result


for items in [[1, 2, 2, 3, 1], [], ["a", "A", "a"], [5, 5, 5], [3, 1, 2]]:
    before = items.copy()
    unique_items = unique(items)
    reversed_items = reverse(items)
    print(f"{items} -> unique: {unique_items}, reverse: {reversed_items}")
    print(f"  reverse sedí s [::-1]: {reversed_items == items[::-1]}")
    print(f"  původní beze změny: {items == before}")
