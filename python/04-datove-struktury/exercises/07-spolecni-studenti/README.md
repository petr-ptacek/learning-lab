# 07 — Společní studenti

`set` a množinové operace — kdo chodí do kterého kurzu.

## Požadavky

- V kódu měj dvě množiny:

  ```python
  python_course = {"Anna", "Petr", "Jana", "Tomáš"}
  js_course = {"Petr", "Eva", "Tomáš", "Lukáš"}
  ```

- Napiš funkci `course_report(a, b)`, která pro dvě množiny vypíše:
  - kdo chodí do **obou** kurzů,
  - kdo chodí **aspoň do jednoho**,
  - kdo chodí **jen do prvního**,
  - kdo chodí **jen do druhého**,
  - kdo chodí **právě do jednoho**,
  - kolik je celkem různých studentů.
- Každou skupinu získej **jedním množinovým operátorem** (`&`, `|`, `-`,
  `^`), ne cyklem.
- Pořadí jmen ve výpisu setu se může lišit od tabulky — to je v pořádku,
  set pořadí nezaručuje.
- Zavolej funkci pro kurzy výše a pro `python_course` s prázdnou
  množinou (pozor, jak se prázdný set zapisuje).

### Příklady vstup/výstup

Pro `python_course` a `js_course`:

| Skupina          | Výsledek                                            |
|------------------|-----------------------------------------------------|
| oba kurzy        | `{'Petr', 'Tomáš'}`                                 |
| aspoň jeden      | `{'Anna', 'Eva', 'Jana', 'Lukáš', 'Petr', 'Tomáš'}` |
| jen první        | `{'Anna', 'Jana'}`                                  |
| jen druhý        | `{'Eva', 'Lukáš'}`                                  |
| právě jeden      | `{'Anna', 'Eva', 'Jana', 'Lukáš'}`                  |
| počet studentů   | `6`                                                 |

Pro `python_course` a prázdnou množinu:

| Skupina          | Výsledek                                  |
|------------------|-------------------------------------------|
| oba kurzy        | `set()`                                   |
| aspoň jeden      | `{'Anna', 'Jana', 'Petr', 'Tomáš'}`       |
| jen první        | `{'Anna', 'Jana', 'Petr', 'Tomáš'}`       |
| jen druhý        | `set()`                                   |
| právě jeden      | `{'Anna', 'Jana', 'Petr', 'Tomáš'}`       |
| počet studentů   | `4`                                       |

## Bonus

- Data přijdou jako seznam přihlášek (tuple `(student, kurz)`), ve kterém
  se můžou opakovat:

  ```python
  registrations = [
      ("Anna", "python"),
      ("Petr", "js"),
      ("Anna", "python"),
      ("Petr", "python"),
      ("Eva", "js"),
  ]
  ```

- Napiš funkci `group_by_course(registrations)`, která vrátí dict
  `kurz → set studentů` (duplicitní přihláška se tak sama zahodí).
- Výsledek pak předej do `course_report`.

### Příklady vstup/výstup (bonus)

| Vstup                    | `group_by_course(...)`                                |
|--------------------------|-------------------------------------------------------|
| `registrations` výše     | `{'python': {'Anna', 'Petr'}, 'js': {'Petr', 'Eva'}}` |
| `[]`                     | `{}`                                                  |
| `[("Anna", "python")]`   | `{'python': {'Anna'}}`                                |
