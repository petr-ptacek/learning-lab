# 07 — Žebříček

Souhrnná úloha — `sorted` s víc kritérii, `enumerate` pro pořadí, `max`,
`sum` a formátovaný výpis.

## Požadavky

- V kódu měj výsledky:

  ```python
  results = [
      ("Anna", 87), ("Petr", 92), ("Eva", 87),
      ("Jana", 75), ("Tomáš", 92), ("Lukáš", 60),
  ]
  ```

- Napiš tyto funkce:
  - `leaderboard(results)` — seřazené výsledky: body sestupně, při shodě
    jméno abecedně.
  - `print_leaderboard(results)` — vypíše žebříček s pořadím
    (`enumerate`), zarovnaný jako ukázka níže. Prázdné výsledky →
    `Žádné výsledky`.
  - `average(results)` — průměr bodů zaokrouhlený na 1 místo (prázdné →
    `0`).
  - `top_scorers(results)` — abecedně seřazená jména všech, kdo mají
    nejvyšší počet bodů.
  - `grade(score)` — známka: `A` ≥ 90, `B` ≥ 80, `C` ≥ 70, `D` ≥ 60,
    jinak `F`.

`print_leaderboard(results)`:

```
 1. Petr      92  A
 2. Tomáš     92  A
 3. Anna      87  B
 4. Eva       87  B
 5. Jana      75  C
 6. Lukáš     60  D
```

### Příklady vstup/výstup

| Volání                  | Výsledek                                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------------|
| `leaderboard(results)`  | `[('Petr', 92), ('Tomáš', 92), ('Anna', 87), ('Eva', 87), ('Jana', 75), ('Lukáš', 60)]`                     |
| `leaderboard([])`       | `[]`                                                                                                       |
| `average(results)`      | `82.2`                                                                                                     |
| `average([])`           | `0`                                                                                                        |
| `top_scorers(results)`  | `['Petr', 'Tomáš']`                                                                                        |
| `top_scorers([])`       | `[]`                                                                                                       |

| `score` | `grade(score)` |
|---------|----------------|
| `100`   | `A`            |
| `90`    | `A`            |
| `89`    | `B`            |
| `60`    | `D`            |
| `59`    | `F`            |
| `0`     | `F`            |

## Bonus

- **Sportovní pořadí** — hráči se stejným počtem bodů sdílí stejné
  pořadí a další pořadí se přeskočí (1, 1, 3, 3, 5, 6). Uprav
  `print_leaderboard` tak, aby tohle pořadí vypisovala.
- `grade_counts(results)` — dict `známka → počet studentů`.

`print_leaderboard(results)` (bonus):

```
 1. Petr      92  A
 1. Tomáš     92  A
 3. Anna      87  B
 3. Eva       87  B
 5. Jana      75  C
 6. Lukáš     60  D
```

### Příklady vstup/výstup (bonus)

| Volání                                          | Výsledek                              |
|-------------------------------------------------|---------------------------------------|
| `grade_counts(results)`                         | `{'B': 2, 'A': 2, 'C': 1, 'D': 1}` (pořadí klíčů nehraje roli) |
| `grade_counts([])`                              | `{}`                                  |
| pořadí pro `[("A", 5), ("B", 5), ("C", 5)]`     | `1, 1, 1`                             |
