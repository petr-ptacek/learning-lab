# 04 — Body v rovině

`tuple` jako pevná dvojice hodnot, rozbalení (`x, y = point`) a seznam
tuplů.

## Požadavky

- Bod je tuple `(x, y)`.
- Napiš funkci `distance(a, b)`, která vrátí vzdálenost dvou bodů
  (`((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5`). Souřadnice získej
  **rozbalením** (`x1, y1 = a`), ne přes `a[0]`.
- Napiš funkci `path_length(points)` — délka lomené čáry přes všechny
  body v daném pořadí (součet vzdáleností sousedních bodů). Pro 0 nebo
  1 bod je délka `0`.
- Napiš funkci `bounding_box(points)`, která vrátí **tuple**
  `(min_x, min_y, max_x, max_y)` — nejmenší obdélník, do kterého se
  všechny body vejdou. Pro prázdný seznam vrať `None`. Bez `min()`/`max()`.
- Vyzkoušej si, co se stane, když zkusíš změnit bod (`point[0] = 1`).
  Chybu si přečti a řádek zakomentuj.
- Délky vypisuj zaokrouhlené na 2 desetinná místa.

### Příklady vstup/výstup

| Volání                                          | Výsledek            |
|-------------------------------------------------|---------------------|
| `distance((0, 0), (3, 4))`                      | `5.0`               |
| `distance((1, 1), (1, 1))`                      | `0.0`               |
| `distance((-1, -1), (2, 3))`                    | `5.0`               |
| `distance((0, 0), (1, 1))`                      | `1.41`              |
| `path_length([(0, 0), (3, 4), (3, 0)])`         | `9.0`               |
| `path_length([(0, 0), (3, 4), (-1, 2), (5, -2)])` | `16.68`           |
| `path_length([(2, 2)])`                         | `0`                 |
| `path_length([])`                               | `0`                 |
| `bounding_box([(0, 0), (3, 4), (-1, 2), (5, -2)])` | `(-1, -2, 5, 4)` |
| `bounding_box([(2, 2)])`                        | `(2, 2, 2, 2)`      |
| `bounding_box([])`                              | `None`              |

## Bonus

- Napiš funkci `closest_pair(points)`, která vrátí tuple dvou **nejbližších**
  bodů (v pořadí, v jakém jsou v seznamu). Při shodě vzdáleností vyhrává
  první nalezená dvojice. Pro méně než 2 body vrať `None`.

### Příklady vstup/výstup (bonus)

| Volání                                              | Výsledek               |
|-----------------------------------------------------|------------------------|
| `closest_pair([(0, 0), (3, 4), (3, 0)])`            | `((0, 0), (3, 0))`     |
| `closest_pair([(0, 0), (3, 4), (-1, 2), (5, -2)])`  | `((0, 0), (-1, 2))`    |
| `closest_pair([(2, 2)])`                            | `None`                 |
| `closest_pair([])`                                  | `None`                 |
