import math
from collections.abc import Iterable


class Employee:
    role = "employee"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def monthly_cost(self):
        return round(self.salary * 1.338)

    def describe(self):
        return f"{self.name} - {self.role}"

    def __str__(self):
        return f"{self.name} ({type(self).__name__})"


class Developer(Employee):
    role = "developer"

    def __init__(self, name, salary, languages: Iterable | None = None):
        super().__init__(name, salary)
        self.languages = list(languages or [])


class Manager(Employee):
    role = "manager"

    def __init__(
        self,
        name,
        salary,
        reports: Iterable | None = None,
    ):
        super().__init__(name, salary)
        self.reports = list(reports or [])

    def add_report(self, report: Employee):
        self.reports.append(report)

    def monthly_cost(self):
        per_reports = sum(5_000 for _ in self.reports)

        return round(super().monthly_cost() + per_reports)


if False:
    dev = Developer("Petr", 60000, ["Python", "SQL"])
    print(isinstance(dev, Employee), isinstance(Employee("A", 1), Developer))
    # true, false
    print(type(dev) is Employee, issubclass(Manager, Employee))
    # false, true
    print("role" in vars(dev), "describe" in vars(Developer))
    # false, false
    print(dev.describe())
    # "Petr developer"

anna = Employee("Anna", 40000)
dev = Developer("Petr", 60000, ["Python", "SQL"])
boss = Manager("Eva", 80000)

print(anna.monthly_cost())
print(str(anna), anna.describe())
print(dev.languages)


class Intern(Employee):
    def __init__(self, name, school, salary=15_000):
        super().__init__(name, salary)
        self.school = school


intern = Intern("Ota", "CVUT")
print(vars(intern))
# { school: "CVUT" }
print(intern.describe())
# nenajde se name

print(Developer.__mro__)
# Developer -> Employee -> object

staff = [
    Employee("Anna", 40000),
    Developer("Petr", 60000, ["Python"]),
    Manager("Eva", 80000),
]

staff[2].add_report(staff[0])

print([e.monthly_cost() for e in staff])
print(sum(e.monthly_cost() for e in staff))
