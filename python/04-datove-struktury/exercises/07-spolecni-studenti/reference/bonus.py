def course_report(a, b):
    print(f"Oba kurzy: {a & b}")
    print(f"Aspoň jeden: {a | b}")
    print(f"Jen první: {a - b}")
    print(f"Jen druhý: {b - a}")
    print(f"Právě jeden: {a ^ b}")
    print(f"Počet studentů: {len(a | b)}")


def group_by_course(registrations):
    courses = {}
    for student, course in registrations:
        if course not in courses:
            courses[course] = set()
        courses[course].add(student)
    return courses


registrations = [
    ("Anna", "python"),
    ("Petr", "js"),
    ("Anna", "python"),
    ("Petr", "python"),
    ("Eva", "js"),
]

courses = group_by_course(registrations)
print(courses)
course_report(courses["python"], courses["js"])
