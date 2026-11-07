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
    cost_per_report = 5000

    def __init__(self, name: str, salary: int) -> None:
        super().__init__(name, salary)
        self.reports: list[Employee] = []

    def add_report(self, employee: Employee) -> None:
        self.reports.append(employee)

    def monthly_cost(self) -> int:
        return super().monthly_cost() + self.cost_per_report * len(self.reports)


dev = Developer("Petr", 60000, ["Python", "SQL"])
print(isinstance(dev, Employee), isinstance(Employee("A", 1), Developer))  # True False
print(type(dev) is Employee, issubclass(Manager, Employee))  # False True
# dev.role: instance (není) → Developer (najde "vývojář").
# dev.describe: instance → Developer (není) → Employee (najde).
# isinstance počítá i s podtřídami, type(x) is ne → skoro vždy chceš isinstance.
print("role" in vars(dev), "describe" in vars(Developer))  # False False
print(dev.describe())  # Petr – vývojář

anna = Employee("Anna", 40000)
boss = Manager("Eva", 80000)
boss.add_report(anna)
boss.add_report(dev)
print(anna.monthly_cost(), dev.monthly_cost(), boss.monthly_cost())  # 53520 80280 117040
print(str(boss), boss.describe())  # Eva (Manager) Eva – manažer
