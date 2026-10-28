results = [
    ("Anna", 87),
    ("Petr", 92),
    ("Eva", 87),
    ("Jana", 75),
    ("Tomáš", 92),
    ("Lukáš", 60),
]


def get_top_scorers(results):
    ordered = get_leaderboard(results)

    top_score = max([p[1] for p in ordered], default=0)
    top_scorers = filter(lambda x: x[1] == top_score, ordered)
    return [p[0] for p in top_scorers]


def get_average(results):
    if len(results) == 0:
        return 0

    total = sum(score for name, score in results)
    return round(total / len(results), 1)


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def get_leaderboard(results):
    return sorted(results, key=lambda x: (-x[1], x[0].lower()))


def print_leaderboard(results):
    if not results:
        print("No results")
        return

    ordered = get_leaderboard(results)
    for nth, p in enumerate(ordered, 1):
        g = get_grade(p[1])
        name = p[0]
        score = p[1]

        print(f"{f'{nth}.':3}{name:<20}{score:4} {g}")


def print_leaderboard2(results):
    if not results:
        print("No results")
        return

    ordered = get_leaderboard(results)
    nth_real = 1
    previous_result = None
    for nth, p in enumerate(ordered, 1):
        g = get_grade(p[1])
        name = p[0]
        score = p[1]

        if not previous_result:
            previous_result = p

        if previous_result[1] != score:
            nth_real = nth
            previous_result = p

        print(f"{f'{nth_real}.':3}{name:<20}{score:4} {g}")


def grade_counts(results):
    results_counts_by_grade = dict()

    for name, score in results:
        grade = get_grade(score)
        count = results_counts_by_grade.get(grade, 0)
        results_counts_by_grade[grade] = count + 1

    return results_counts_by_grade


print(grade_counts(results))
print_leaderboard2(results)
