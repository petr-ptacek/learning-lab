python_course = { "Anna", "Petr", "Jana", "Tomáš" }
js_course = { "Petr", "Eva", "Tomáš", "Lukáš" }


def course_report(a: set[str], b: set[str]):
    print(f"oba kurzy {a.intersection(b)}")
    print(f"alespon jeden {a.union(b)}")
    print(f"jen prvni {a.difference(b)}")
    print(f"jen druhy {b.difference(a)}")
    print(f"prave jeden {a.symmetric_difference(b)}")
    print(f"pocet studentu {len(b.union(a))}")


course_report(python_course, js_course)
course_report(python_course, set())
