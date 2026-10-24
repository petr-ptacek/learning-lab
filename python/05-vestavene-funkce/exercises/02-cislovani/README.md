# 02 — Číslování

`enumerate` — index a hodnota zároveň, bez `range(len(...))`.

## Požadavky

- Napiš funkci `print_numbered(items, start=1)`, která vypíše položky
  očíslované od `start` (`1. mléko`). Prázdný seznam → `Seznam je
  prázdný`. Použij `enumerate` s parametrem `start`.
- Napiš funkci `indexes_of(items, value)`, která vrátí seznam **indexů**
  (od 0), na kterých se `value` v seznamu vyskytuje. Jedním
  comprehensionem s `enumerate`.

`print_numbered(["mléko", "chleba"])`:

```
1. mléko
2. chleba
```

`print_numbered(["mléko", "chleba"], start=0)`:

```
0. mléko
1. chleba
```

### Příklady vstup/výstup

| Volání                                          | Výsledek     |
|-------------------------------------------------|--------------|
| `indexes_of(["a", "b", "a", "c", "a"], "a")`    | `[0, 2, 4]`  |
| `indexes_of([1, 2, 1], 1)`                      | `[0, 2]`     |
| `indexes_of(["a", "b"], "z")`                   | `[]`         |
| `indexes_of([], "a")`                           | `[]`         |

## Bonus

- `index_of_max(numbers)` — index největšího čísla, **jedním** voláním
  `max` nad `enumerate(numbers)` s vhodným `key`. Při shodě vyhrává první
  výskyt, prázdný seznam → `None`.

### Příklady vstup/výstup (bonus)

| Volání                      | Výsledek |
|-----------------------------|----------|
| `index_of_max([3, 9, 2, 9])` | `1`     |
| `index_of_max([5])`          | `0`     |
| `index_of_max([-1, -5])`     | `0`     |
| `index_of_max([])`           | `None`  |
