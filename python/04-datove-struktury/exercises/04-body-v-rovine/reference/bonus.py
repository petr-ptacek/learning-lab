def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def closest_pair(points):
    best = None
    best_distance = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = distance(points[i], points[j])
            if best is None or d < best_distance:
                best = (points[i], points[j])
                best_distance = d
    return best


for case in [[(0, 0), (3, 4), (3, 0)], [(0, 0), (3, 4), (-1, 2), (5, -2)], [(2, 2)], []]:
    print(closest_pair(case))
