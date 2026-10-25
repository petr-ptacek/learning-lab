def pair_up(names, scores):
    return dict(zip(names, scores))


print(pair_up(["Anna", "Petr"], [10, 30]))
print(pair_up(["Anna", "Petr"], [30]))
print(pair_up(["Anna"], [10, 30]))


def differences(numbers):
    return [y - x for x, y in zip(numbers, numbers[1:])]


print(differences([1, 4, 9, 16]))
print(differences([]))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    x1, y1 = a
    x2, y2 = b

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def path_length(points):
    length = sum(distance(a, b) for a, b in zip(points, points[1:]))
    return round(length, 2)


print(path_length([(0, 0), (3, 4), (3, 0)]))
print(path_length([(0, 0), (3, 4), (-1, 2), (5, -2)]))
