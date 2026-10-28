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
    rank, previous_score = 0, None
    for position, (name, score) in enumerate(leaderboard(results), start=1):
        if score != previous_score:
            rank, previous_score = position, score
        print(f"{rank:>2}. {name:<8}{score:>3}  {grade(score)}")


def grade_counts(results):
    counts = {}
    for _, score in results:
        letter = grade(score)
        counts[letter] = counts.get(letter, 0) + 1
    return counts


print_leaderboard(results)
print_leaderboard([("A", 5), ("B", 5), ("C", 5)])
print(grade_counts(results))
print(grade_counts([]))
