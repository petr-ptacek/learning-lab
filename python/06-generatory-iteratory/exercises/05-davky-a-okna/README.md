# 05 — Dávky a okna

Dva vzory, které v praxi potkáš pořád: zpracování po **dávkách**
(stránkování, hromadné ukládání do DB) a **posuvné okno** (klouzavý
průměr, sousední prvky).

## Požadavky

- Napiš generátor `chunked(items, size)`, který vydává kusy seznamu po
  `size` prvcích. Poslední kus může být kratší. Pro základ stačí, že
  `items` je seznam nebo string (smíš použít `len` a slicing).
- Napiš generátor `sliding_window(items, size)`, který vydává **tuple**
  každých `size` sousedních prvků. Když je prvků méně než `size`, nevydá
  nic.
- Napiš funkci `moving_average(numbers, size)` — klouzavý průměr přes
  `sliding_window`, zaokrouhlený na 2 místa. Jedním comprehensionem.

### Příklady vstup/výstup

| Volání                                      | Výsledek                              |
|---------------------------------------------|---------------------------------------|
| `list(chunked([1, 2, 3, 4, 5, 6, 7], 3))`   | `[[1, 2, 3], [4, 5, 6], [7]]`         |
| `list(chunked([1, 2, 3, 4], 2))`            | `[[1, 2], [3, 4]]`                    |
| `list(chunked([1, 2], 5))`                  | `[[1, 2]]`                            |
| `list(chunked("abcde", 2))`                 | `['ab', 'cd', 'e']`                   |
| `list(chunked([], 3))`                      | `[]`                                  |

| Volání                                      | Výsledek                              |
|---------------------------------------------|---------------------------------------|
| `list(sliding_window([1, 2, 3, 4], 3))`     | `[(1, 2, 3), (2, 3, 4)]`              |
| `list(sliding_window("abcd", 2))`           | `[('a', 'b'), ('b', 'c'), ('c', 'd')]` |
| `list(sliding_window([1, 2, 3], 1))`        | `[(1,), (2,), (3,)]`                  |
| `list(sliding_window([1, 2], 3))`           | `[]`                                  |
| `list(sliding_window([], 2))`               | `[]`                                  |

| Volání                                      | Výsledek                |
|---------------------------------------------|-------------------------|
| `moving_average([10, 20, 30, 40, 50], 3)`   | `[20.0, 30.0, 40.0]`    |
| `moving_average([1, 2, 4], 2)`              | `[1.5, 3.0]`            |
| `moving_average([5], 2)`                    | `[]`                    |

## Bonus

- `chunked_any(iterable, size)` — totéž co `chunked`, ale pro
  **libovolný** iterable, i nekonečný generátor. Bez `len` a slicingu
  (iterátor nic z toho neumí). Kusy vracej jako seznamy. Nápověda:
  `itertools.islice` nad **jedním** iterátorem opakovaně, dokud vrací
  něco neprázdného.
- Porovnej s hotovými `itertools.batched` (Python 3.12+)
  a `itertools.pairwise`. Co vrací místo seznamů?

### Příklady vstup/výstup (bonus)

| Volání                                          | Výsledek                              |
|-------------------------------------------------|---------------------------------------|
| `list(chunked_any(range(7), 3))`                | `[[0, 1, 2], [3, 4, 5], [6]]`         |
| `list(chunked_any(iter([]), 2))`                | `[]`                                  |
| prvních 3 kusů z `chunked_any(naturals(), 2)`   | `[[1, 2], [3, 4], [5, 6]]`            |
| `list(itertools.batched(range(7), 3))`          | `[(0, 1, 2), (3, 4, 5), (6,)]`        |
| `list(itertools.pairwise([1, 2, 3, 4]))`        | `[(1, 2), (2, 3), (3, 4)]`            |

`naturals` a `take` si zkopíruj z `03-nekonecne`.
