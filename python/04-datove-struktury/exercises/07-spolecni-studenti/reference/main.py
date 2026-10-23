def course_report(a, b):
    print(f"Oba kurzy: {a & b}")
    print(f"Aspoň jeden: {a | b}")
    print(f"Jen první: {a - b}")
    print(f"Jen druhý: {b - a}")
    print(f"Právě jeden: {a ^ b}")
    print(f"Počet studentů: {len(a | b)}")


python_course = {"Anna", "Petr", "Jana", "Tomáš"}
js_course = {"Petr", "Eva", "Tomáš", "Lukáš"}

course_report(python_course, js_course)
print()
course_report(python_course, set())
