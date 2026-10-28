results = [
    ("Anna", 87), ("Petr", 92), ("Eva", 87),
    ("Jana", 75), ("Tomáš", 92), ("Lukáš", 60),
]


def leaderboard(results):
    return sorted(results, key=lambda pair: (-pair[1], pair[0]))


def grade(score):
    for limit, letter in [(90, "A"), (80, "B"), (70, "C"), (60, "D")]:
        if score >= limit:
            return letter
    return "F"


def print_leaderboard(results):
    if not results:
        print("Žádné výsledky")
        return
    for position, (name, score) in enumerate(leaderboard(results), start=1):
        print(f"{position:>2}. {name:<8}{score:>3}  {grade(score)}")


def average(results):
    if not results:
        return 0
    return round(sum(score for _, score in results) / len(results), 1)


def top_scorers(results):
    best = max((score for _, score in results), default=None)
    return sorted(name for name, score in results if score == best)


print(leaderboard(results))
print(leaderboard([]))
print_leaderboard(results)
print_leaderboard([])
print(average(results), average([]))
print(top_scorers(results), top_scorers([]))
print([grade(score) for score in [100, 90, 89, 60, 59, 0]])
