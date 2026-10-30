# 01 — Iter a next

Ručně to, co `for` dělá za tebe: `iter()` vyrobí iterátor, `next()` z něj
bere hodnoty. A `next` s defaultem jako „první, nebo nic“.

## Požadavky

- **Předpověď:** co vypíše tenhle kód? Napiš si odpověď do komentáře,
  pak spusť:

  ```python
  it = iter([10, 20, 30])
  print(next(it))
  print(next(it))
  print(next(it))
  print(next(it, "konec"))
  ```

  Co by se stalo, kdyby poslední řádek byl `print(next(it))` bez
  druhého argumentu? Vyzkoušej a přečti si chybu.

- Napiš funkci `first(iterable, default=None)`, která vrátí první prvek
  **libovolného** iterable (seznam, string, `range`, dict, `map` …),
  nebo `default`, když je prázdný. Jedním řádkem přes `iter` a `next`,
  bez `[0]` a bez `if`.
- Napiš funkci `first_match(items, predicate, default=None)`, která
  vrátí první prvek, pro který `predicate(prvek)` vrátí `True`. Jedním
  řádkem: `next` + generátorový výraz.
- **Předpověď 2:** co vypíše tohle a proč?

  ```python
  m = map(int, ["1", "2", "3"])
  print(first(m))
  print(list(m))
  ```

### Příklady vstup/výstup

| Volání                                  | Výsledek |
|-----------------------------------------|----------|
| `first([5, 6])`                         | `5`      |
| `first("abc")`                          | `'a'`    |
| `first(range(3, 10))`                   | `3`      |
| `first({"a": 1, "b": 2})`               | `'a'`    |
| `first(map(str.upper, ["x", "y"]))`     | `'X'`    |
| `first([])`                             | `None`   |
| `first({})`                             | `None`   |
| `first([], "nic")`                      | `'nic'`  |

| Volání                                                  | Výsledek |
|---------------------------------------------------------|----------|
| `first_match([1, 4, 7, 10], lambda n: n > 5)`           | `7`      |
| `first_match([1, 2], lambda n: n > 5)`                  | `None`   |
| `first_match(["kocka", "Pes", "Zebra"], str.istitle)`   | `'Pes'`  |
| `first_match([], bool, "nic")`                          | `'nic'`  |

## Bonus

- `manual_sum(iterable)` — sečte čísla **bez `for`**, `sum` ani
  comprehension. Jen `iter`, `next` a `while`, tedy přesně to, co dělá
  `for` uvnitř (viz `THEORY.md`). Konec poznáš přes default u `next`.
- Rozmysli si (komentářem): proč jako default není dobré použít `None`
  nebo `0`? Co kdyby v datech byla právě ta hodnota? Pomůže hodnota,
  která se s ničím v datech nemůže rovnat: `done = object()`
  a porovnání přes `is`.

### Příklady vstup/výstup (bonus)

| Volání                             | Výsledek |
|------------------------------------|----------|
| `manual_sum([1, 2, 3])`            | `6`      |
| `manual_sum([0, 0, 7])`            | `7`      |
| `manual_sum(range(5))`             | `10`     |
| `manual_sum(map(int, ["4", "5"]))` | `9`      |
| `manual_sum([])`                   | `0`      |
