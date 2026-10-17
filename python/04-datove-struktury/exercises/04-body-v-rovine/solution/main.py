def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    x1, y1 = a
    x2, y2 = b

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def path_length(points: list[tuple[float, float]]) -> float:
    length = 0
    for idx in range(len(points)):
        if idx + 1 >= len(points):
            break

        a = points[idx]
        b = points[idx + 1]

        length += distance(a, b)

    return length


def bounding_box(points: list[tuple[float, float]]):
    if len(points) == 0:
        return None

    x, y = points[0]

    max_x = x
    max_y = y
    min_x = x
    min_y = y

    for (x, y) in points:

        if x > max_x:
            max_x = x

        if x < min_x:
            min_x = x

        if y > max_y:
            max_y = y

        if y < min_y:
            min_y = y

    return (
        min_x,
        min_y,
        max_x,
        max_y,
    )


def closest_pair(points: list[tuple[float, float]]):
    if len(points) < 2:
        return None

    p1 = points[0]
    p2 = points[1]
    length = distance(p1, p2)

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            l = distance(points[i], points[j])
            if l < length:
                length = l
                p1 = points[i]
                p2 = points[j]

    return p1, p2


# for t in [
#     [(0, 0), (3, 4), (3, 0)],
#     [],
#     [(2, 2)],
#     [(0, 0), (3, 4), (-1, 2), (5, -2)]
# ]:
#     length = path_length(t)
#     print(f"{length:.2f}")


# print(bounding_box([(0, 0), (3, 4), (-1, 2), (5, -2)]))
# print(bounding_box([(2, 2)]))
# print(bounding_box([]))
print(closest_pair([(0, 0), (3, 4), (3, 0)]))
print(closest_pair([(0, 0), (3, 4), (-1, 2), (5, -2)]))
print(closest_pair([]))
print(closest_pair([(2, 2)]))
