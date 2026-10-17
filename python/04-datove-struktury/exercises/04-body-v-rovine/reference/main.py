def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def path_length(points):
    total = 0
    for i in range(len(points) - 1):
        total += distance(points[i], points[i + 1])
    return total


def bounding_box(points):
    if len(points) == 0:
        return None

    min_x, min_y = points[0]
    max_x, max_y = points[0]
    for x, y in points:
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    return min_x, min_y, max_x, max_y


points = [(0, 0), (3, 4), (-1, 2), (5, -2)]
# points[0] = (1, 1)     # funguje — list jde měnit
# points[0][0] = 1       # TypeError: 'tuple' object does not support item assignment

print(f"{distance((0, 0), (3, 4)):.2f}")
print(f"{distance((0, 0), (1, 1)):.2f}")
for case in [[(0, 0), (3, 4), (3, 0)], points, [(2, 2)], []]:
    print(f"{path_length(case):.2f}", bounding_box(case))
