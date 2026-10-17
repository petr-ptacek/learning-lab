def duplicates(items):
    result = []
    for item in items:
        if items.count(item) > 1 and item not in result:
            result.append(item)
    return result


for items in [[1, 2, 2, 3, 1], [3, 1, 2], ["a", "A", "a"], [5, 5, 5], []]:
    print(f"{items} -> duplicates: {duplicates(items)}")
