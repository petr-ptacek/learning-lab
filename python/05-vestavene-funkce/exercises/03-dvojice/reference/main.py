def pair_up(names, scores):
    return dict(zip(names, scores))


def differences(numbers):
    return [b - a for a, b in zip(numbers, numbers[1:])]


def distance(a, b):
    (x1, y1), (x2, y2) = a, b
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def path_length(points):
    return sum(distance(a, b) for a, b in zip(points, points[1:]))


print(pair_up(["Anna", "Petr", "Eva"], [90, 75, 82]))
print(pair_up(["Anna", "Petr", "Eva"], [90, 75]))
print(pair_up([], []))

for numbers in [[1, 4, 9, 16], [10, 7, 7, 12], [5], []]:
    print(differences(numbers))

for points in [[(0, 0), (3, 4), (3, 0)], [(0, 0), (3, 4), (-1, 2), (5, -2)], [(2, 2)], []]:
    print(round(path_length(points), 2))
