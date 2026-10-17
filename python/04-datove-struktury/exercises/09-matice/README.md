# 09 — Matice

Vnořené seznamy (seznam seznamů) a dvojitý cyklus — řádky a sloupce.

## Požadavky

- Matice je seznam řádků, každý řádek je seznam čísel stejné délky:
  `[[1, 2, 3], [4, 5, 6]]` = 2 řádky, 3 sloupce.
- Napiš funkci `print_matrix(matrix)`, která matici vypíše po řádcích,
  každé číslo zarovnané doprava na šířku 4. Prázdná matice → `(prázdná)`.
- Napiš funkci `transpose(matrix)` — vrátí novou matici, kde se řádky
  stanou sloupci.
- Napiš funkce `row_sums(matrix)` a `col_sums(matrix)` — vrátí seznam
  součtů jednotlivých řádků / sloupců (bez `sum()`). Zkus `col_sums`
  napsat pomocí `transpose` a `row_sums`.
- Prázdná matice `[]` vrací ve všech funkcích `[]`.

`print_matrix([[1, 2, 3], [4, 5, 6]])`:

```
   1   2   3
   4   5   6
```

### Příklady vstup/výstup

| `matrix`                   | `transpose`                | `row_sums` | `col_sums`  |
|----------------------------|----------------------------|------------|-------------|
| `[[1, 2, 3], [4, 5, 6]]`   | `[[1, 4], [2, 5], [3, 6]]` | `[6, 15]`  | `[5, 7, 9]` |
| `[[1, 2], [3, 4]]`         | `[[1, 3], [2, 4]]`         | `[3, 7]`   | `[4, 6]`    |
| `[[7]]`                    | `[[7]]`                    | `[7]`      | `[7]`       |
| `[]`                       | `[]`                       | `[]`       | `[]`        |

## Bonus

- Napiš funkci `multiply(a, b)` — maticový součin. Prvek na pozici
  `[i][j]` je součet `a[i][k] * b[k][j]` přes všechna `k`. Pokud počet
  sloupců `a` neodpovídá počtu řádků `b` (nebo je některá matice prázdná),
  vrať `None`.

### Příklady vstup/výstup (bonus)

| `a`                  | `b`                  | `multiply(a, b)`       |
|----------------------|----------------------|------------------------|
| `[[1, 2], [3, 4]]`   | `[[5, 6], [7, 8]]`   | `[[19, 22], [43, 50]]` |
| `[[1, 0], [0, 1]]`   | `[[4, 5], [6, 7]]`   | `[[4, 5], [6, 7]]`     |
| `[[1, 2, 3]]`        | `[[1], [2], [3]]`    | `[[14]]`               |
| `[[1, 2]]`           | `[[1, 2]]`           | `None`                 |
| `[]`                 | `[[1]]`              | `None`                 |
