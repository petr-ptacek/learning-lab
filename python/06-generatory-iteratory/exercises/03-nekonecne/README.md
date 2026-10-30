# 03 — Nekonečné sekvence

Generátor s `while True` běží „navždy“, ale počítá jen to, co si někdo
vyžádá. Jak z něj vzít jen část.

## Požadavky

- Napiš nekonečné generátory:
  - `naturals(start=1)` — `start, start+1, start+2, …`
  - `fibonacci()` — `0, 1, 1, 2, 3, 5, 8, …` (každé číslo je součet
    dvou předchozích).
- Napiš funkci `take(iterable, n)`, která vrátí **seznam** prvních `n`
  prvků. Musí fungovat i na nekonečném generátoru a na kratší sekvenci,
  než je `n`. Bez `itertools`. Nápověda: `zip` skončí s nejkratším
  vstupem.
- Napiš funkci `first_fib_over(limit)` — první Fibonacciho číslo
  **větší** než `limit`. Jedním řádkem přes `next` a generátorový výraz
  nad `fibonacci()`.
- **Nikdy** nevolej `list(naturals())`. Proč?

### Příklady vstup/výstup

| Volání                        | Výsledek                                   |
|-------------------------------|--------------------------------------------|
| `take(naturals(), 5)`         | `[1, 2, 3, 4, 5]`                          |
| `take(naturals(10), 3)`       | `[10, 11, 12]`                             |
| `take(fibonacci(), 10)`       | `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`        |
| `take("python", 3)`           | `['p', 'y', 't']`                          |
| `take([1, 2], 5)`             | `[1, 2]`                                   |
| `take(fibonacci(), 0)`        | `[]`                                       |
| `first_fib_over(100)`         | `144`                                      |
| `first_fib_over(1000)`        | `1597`                                     |
| `first_fib_over(1)`           | `2`                                        |
| `first_fib_over(0)`           | `1`                                        |

## Bonus

- **Předpověď:** záleží v `zip` na pořadí argumentů? Co vypíšou tyhle
  dva bloky? Vysvětli rozdíl ve druhém řádku.

  ```python
  g = naturals()
  print(list(zip(g, range(3))))
  print(next(g))

  g = naturals()
  print(list(zip(range(3), g)))
  print(next(g))
  ```

  Projdi si, jak `zip` bere hodnoty: z kterého vstupu nejdřív a kdy
  zjistí, že má skončit. Která verze je správně pro tvou `take`?

- Přepiš pomocí `itertools` (`import itertools`):
  - `take_it(iterable, n)` — přes `islice`.
  - `fib_below(limit)` — seznam Fibonacciho čísel **menších** než
    `limit`, přes `takewhile`.
  - prvních 4 čísla od 10 po pěti přes `count` + `islice`.

### Příklady vstup/výstup (bonus)

| Volání                    | Výsledek                                |
|---------------------------|-----------------------------------------|
| `take_it(naturals(), 5)`  | `[1, 2, 3, 4, 5]`                       |
| `take_it([1, 2], 5)`      | `[1, 2]`                                |
| `fib_below(50)`           | `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`     |
| `fib_below(1)`            | `[0]`                                   |
| `fib_below(0)`            | `[]`                                    |
| `count` od 10 po 5, 4 čísla | `[10, 15, 20, 25]`                    |
