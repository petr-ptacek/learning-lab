# 01 — První dědičnost

Podtřída převezme všechno od rodiče a přidá nebo změní jen to, co
potřebuje. Každý Django model začíná `class Book(models.Model):`, každé
view `class BookList(ListView):`. Tady si vyzkoušíš, odkud se zděděné
atributy a metody berou.

Teorie: [`docs/INHERITANCE_AND_SUPER.md`](../../../docs/INHERITANCE_AND_SUPER.md).

## Požadavky

- `Employee(name, salary)`:
  - atribut **třídy** `role = "zaměstnanec"`,
  - `monthly_cost()` → náklady firmy: `salary × 1.338`, zaokrouhlené
    na celé koruny (`round`),
  - `describe()` → `"Anna – zaměstnanec"` (bere `self.role`),
  - `__str__` → `"Anna (Employee)"`. Jméno třídy **nepiš natvrdo**,
    zjisti ho z objektu (`type(self).__name__`), ať podtřídy vypíšou
    svoje jméno bez přepisování.
- `Developer(Employee)`:
  - `__init__(self, name, salary, languages=())` — jméno a plat nastaví
    rodič přes `super().__init__(...)`, `languages` si uloží jako
    **vlastní nový** seznam (může přijít libovolný iterable),
  - `role = "vývojář"`.
- `Manager(Employee)`:
  - `role = "manažer"`, `reports` — seznam podřízených (každý manažer
    vlastní), `add_report(employee)`,
  - přepíše `monthly_cost()`: náklady rodiče (zavolej přes `super()`,
    nepočítej znovu) + 5000 Kč za každého podřízeného.
- **Předpověď:** napiš si odpovědi do komentáře, pak spusť:

  ```python
  dev = Developer("Petr", 60000, ["Python", "SQL"])
  print(isinstance(dev, Employee), isinstance(Employee("A", 1), Developer))
  print(type(dev) is Employee, issubclass(Manager, Employee))
  print("role" in vars(dev), "describe" in vars(Developer))
  print(dev.describe())
  ```

  Kde všude Python hledá `dev.role` a `dev.describe`, než je najde?
  Kdy je `isinstance` lepší než `type(x) is`?

### Příklady vstup/výstup

Postupně za sebou:

```python
anna = Employee("Anna", 40000)
dev = Developer("Petr", 60000, ["Python", "SQL"])
boss = Manager("Eva", 80000)
```

| Kód                                        | Výsledek                              |
|--------------------------------------------|---------------------------------------|
| `anna.monthly_cost()`                      | `53520`                               |
| `str(anna), anna.describe()`               | `('Anna (Employee)', 'Anna – zaměstnanec')` |
| `str(dev), dev.describe()`                 | `('Petr (Developer)', 'Petr – vývojář')` |
| `dev.languages`                            | `['Python', 'SQL']`                   |
| `dev.monthly_cost()`                       | `80280` (zděděná metoda)              |
| `Developer("Jana", 50000).languages`       | `[]`                                  |
| `boss.monthly_cost()`                      | `107040` (zatím bez podřízených)      |
| `boss.add_report(anna)`, `boss.add_report(dev)`, `boss.monthly_cost()` | `117040` |
| `[str(e) for e in boss.reports]`           | `['Anna (Employee)', 'Petr (Developer)']` |
| `str(boss), boss.describe()`               | `('Eva (Manager)', 'Eva – manažer')`  |
| `Employee.role, Developer.role`            | `('zaměstnanec', 'vývojář')`          |
| `Employee("X", 0).monthly_cost()`          | `0`                                   |
| `Employee("Y", 33333).monthly_cost()`      | `44600`                               |
| `langs = ["Go"]`, `d = Developer("Ota", 1, langs)`, `d.languages.append("Rust")`, `langs` | `['Go']` |

## Bonus

- `Intern(Employee)` s `__init__(self, name, school)`, který **zapomene**
  zavolat `super().__init__`. Co vrátí `vars(intern)` a co se stane při
  `intern.describe()`? Vysvětli komentářem, pak to oprav: stážista má
  výchozí plat `15000` (`__init__(self, name, school, salary=15000)`).
- Vypiš si `Developer.__mro__` (jen jména tříd). Kde končí každý řetěz?
- Polymorfismus: v seznamu `staff` jsou různé typy zaměstnanců. Spočítej
  celkové měsíční náklady jedním `sum(...)`, bez jakéhokoli `if` na typ.

### Příklady vstup/výstup (bonus)

| Kód                                                   | Výsledek                                                        |
|-------------------------------------------------------|-----------------------------------------------------------------|
| rozbitý `Intern("Ota", "ČVUT")`, `vars(...)`          | `{'school': 'ČVUT'}`                                            |
| …a `.describe()`                                      | `AttributeError: 'Intern' object has no attribute 'name'`       |
| opravený `Intern("Ota", "ČVUT").monthly_cost()`       | `20070`                                                         |
| `[c.__name__ for c in Developer.__mro__]`             | `['Developer', 'Employee', 'object']`                           |

`staff = [Employee("Anna", 40000), Developer("Petr", 60000, ["Python"]), Manager("Eva", 80000)]`
a `staff[2].add_report(staff[0])`:

| Kód                                        | Výsledek                    |
|--------------------------------------------|-----------------------------|
| `[e.monthly_cost() for e in staff]`        | `[53520, 80280, 112040]`    |
| `sum(e.monthly_cost() for e in staff)`     | `245840`                    |
| `sum(e.monthly_cost() for e in [])`        | `0`                         |
