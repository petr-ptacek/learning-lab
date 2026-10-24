# 03 — Dvojice

`zip` — procházení víc kolekcí najednou a sousedních prvků jedné kolekce.

## Požadavky

- Napiš funkci `pair_up(names, scores)`, která z dvou seznamů udělá dict
  `jméno → body` (`dict` + `zip`, jeden řádek). Co se stane, když jsou
  seznamy různě dlouhé? Vyzkoušej.
- Napiš funkci `differences(numbers)`, která vrátí rozdíly sousedních
  čísel (`druhé − první`). Jedním comprehensionem se `zip` — nápověda:
  `numbers[1:]`.
- Přepiš `path_length(points)` z `04-datove-struktury/04-body-v-rovine`
  na jeden řádek: `sum` + generátorový výraz + `zip` sousedních bodů.
  Funkci `distance` si zkopíruj.

### Příklady vstup/výstup

| Volání                                                    | Výsledek                                |
|-----------------------------------------------------------|-----------------------------------------|
| `pair_up(["Anna", "Petr", "Eva"], [90, 75, 82])`          | `{'Anna': 90, 'Petr': 75, 'Eva': 82}`   |
| `pair_up(["Anna", "Petr", "Eva"], [90, 75])`              | `{'Anna': 90, 'Petr': 75}`              |
| `pair_up([], [])`                                         | `{}`                                    |
| `differences([1, 4, 9, 16])`                              | `[3, 5, 7]`                             |
| `differences([10, 7, 7, 12])`                             | `[-3, 0, 5]`                            |
| `differences([5])`                                        | `[]`                                    |
| `differences([])`                                         | `[]`                                    |
| `path_length([(0, 0), (3, 4), (3, 0)])`                   | `9.0`                                   |
| `path_length([(0, 0), (3, 4), (-1, 2), (5, -2)])`         | `16.68` (zaokrouhleno)                  |
| `path_length([(2, 2)])`                                   | `0`                                     |
| `path_length([])`                                         | `0`                                     |

## Bonus

- `transpose(matrix)` z `04-datove-struktury/09-matice` na jeden řádek
  pomocí `zip(*matrix)`. Výsledek má být seznam **seznamů**, ne tuplů.
- Vyzkoušej `zip(..., strict=True)` na různě dlouhých seznamech a přečti
  si chybu.

### Příklady vstup/výstup (bonus)

| Volání                              | Výsledek                     |
|-------------------------------------|------------------------------|
| `transpose([[1, 2, 3], [4, 5, 6]])` | `[[1, 4], [2, 5], [3, 6]]`   |
| `transpose([[7]])`                  | `[[7]]`                      |
| `transpose([])`                     | `[]`                         |
