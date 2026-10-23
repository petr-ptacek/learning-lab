registrations = [
    ("Anna", "python"),
    ("Petr", "js"),
    ("Anna", "python"),
    ("Petr", "python"),
    ("Eva", "js"),
]


def group_by_course(registrations):
    result = dict()
    for name, course in registrations:
        students = result.get(course, set())
        students.add(name)
        result[course] = students

    return result


for course, students in group_by_course(registrations).items():
    print(f"{course}: {students}")
