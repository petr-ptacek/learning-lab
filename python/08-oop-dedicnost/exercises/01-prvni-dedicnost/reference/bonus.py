from collections.abc import Iterable


class Employee:
    role = "zaměstnanec"

    def __init__(self, name: str, salary: int) -> None:
        self.name = name
        self.salary = salary

    def monthly_cost(self) -> int:
        return round(self.salary * 1.338)

    def describe(self) -> str:
        return f"{self.name} – {self.role}"

    def __str__(self) -> str:
        return f"{self.name} ({type(self).__name__})"


class Developer(Employee):
    role = "vývojář"

    def __init__(self, name: str, salary: int, languages: Iterable[str] = ()) -> None:
        super().__init__(name, salary)
        self.languages = list(languages)


class Manager(Employee):
    role = "manažer"

    def __init__(self, name: str, salary: int) -> None:
        super().__init__(name, salary)
        self.reports: list[Employee] = []

    def add_report(self, employee: Employee) -> None:
        self.reports.append(employee)

    def monthly_cost(self) -> int:
        return super().monthly_cost() + 5000 * len(self.reports)


class BrokenIntern(Employee):
    def __init__(self, name: str, school: str) -> None:
        self.school = school  # rodičův __init__ se nezavolá → name a salary chybí


broken = BrokenIntern("Ota", "ČVUT")
print(vars(broken))  # {'school': 'ČVUT'}
# broken.describe() → AttributeError: 'BrokenIntern' object has no attribute 'name'


class Intern(Employee):
    def __init__(self, name: str, school: str, salary: int = 15000) -> None:
        super().__init__(name, salary)
        self.school = school


print(Intern("Ota", "ČVUT").monthly_cost())  # 20070
print([cls.__name__ for cls in Developer.__mro__])  # ['Developer', 'Employee', 'object']

staff = [Employee("Anna", 40000), Developer("Petr", 60000, ["Python"]), Manager("Eva", 80000)]
staff[2].add_report(staff[0])
# Každý objekt si zavolá svou verzi monthly_cost, žádné if na typ.
print([e.monthly_cost() for e in staff])  # [53520, 80280, 112040]
print(sum(e.monthly_cost() for e in staff))  # 245840
