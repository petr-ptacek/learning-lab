# 05 — Map a filter

`map` a `filter` — a srovnání s comprehensionem, který dělá totéž.

## Požadavky

- Napiš tyto funkce pomocí `map` / `filter` (výsledek vždy jako `list`):
  - `parse_numbers(text)` — z textu čísel oddělených mezerami vrátí
    seznam `int` (`text.split()` + `map`).
  - `only_positive(numbers)` — jen čísla větší než nula (`filter`
    s lambdou).
  - `with_vat(prices, rate=0.21)` — ceny s DPH zaokrouhlené na 2 místa
    (`map` s lambdou).
- U `only_positive` a `with_vat` napiš i druhou verzi jako
  comprehension a porovnej, která se ti čte líp.
- **Předpověď:** co vypíše tenhle kód? Napiš si odpověď do komentáře,
  pak spusť a vysvětli rozdíl:

  ```python
  numbers = map(int, ["1", "2", "3"])
  print(list(numbers))
  print(list(numbers))
  ```

### Příklady vstup/výstup

| Volání                              | Výsledek               |
|-------------------------------------|------------------------|
| `parse_numbers("3 1 4")`            | `[3, 1, 4]`            |
| `parse_numbers("  10   -2 0 ")`     | `[10, -2, 0]`          |
| `parse_numbers("")`                 | `[]`                   |
| `only_positive([3, -1, 0, 5])`      | `[3, 5]`               |
| `only_positive([-1, 0])`            | `[]`                   |
| `only_positive([])`                 | `[]`                   |
| `with_vat([100, 24.9, 0])`          | `[121.0, 30.13, 0.0]`  |
| `with_vat([100, 24.9], 0.1)`        | `[110.0, 27.39]`       |

## Bonus

- `apply_all(functions, value)` — zavolá každou funkci ze seznamu na
  stejnou hodnotu a vrátí seznam výsledků (`map` přes seznam **funkcí**).
- Předpověz, co vrátí `list(filter(None, ["", "a", 0, 1, None, [], [0]]))`,
  a pak to ověř. Proč tam je `[0]`, ale ne `[]`? (Souvisí s chybou
  u prázdného čísla v `04-datove-struktury/06-telefonni-seznam`.)

### Příklady vstup/výstup (bonus)

| Volání                                          | Výsledek             |
|-------------------------------------------------|----------------------|
| `apply_all([abs, str, lambda x: x * 2], -3)`    | `[3, '-3', -6]`      |
| `apply_all([], 5)`                              | `[]`                 |
