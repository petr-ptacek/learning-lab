# 08 — Aliasy a kopie

Nejčastější zdroj chyb s kolekcemi: přiřazení nekopíruje. Nejdřív
**předpovídej**, pak ověř a nakonec oprav.

## Část 1 — předpověď

Pro každý úryvek si **nejdřív bez spuštění** napiš do `main.py` jako
komentář, co se vypíše. Pak úryvek spusť a porovnej. U těch, kde ses
spletl, si do komentáře napiš proč.

```python
# A
a = [1, 2, 3]
b = a
b.append(4)
print(a)

# B
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)

# C
grid = [[0, 0], [0, 0]]
copy = grid.copy()
copy[0][0] = 9
print(grid)

# D
row = [0] * 3
grid = [row] * 2
grid[0][0] = 1
print(grid)

# E
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))
print(add_item("b"))

# F
def double_all(numbers):
    for i in range(len(numbers)):
        numbers[i] *= 2

values = [1, 2, 3]
double_all(values)
print(values)
```

## Část 2 — opravy

- Oprav `add_item` z úryvku E tak, aby každé volání bez druhého argumentu
  začínalo s prázdným seznamem.
- Napiš funkci `remove_negatives(numbers)`, která vrátí **nový** seznam
  bez záporných čísel. Původní seznam se nesmí změnit.
- Vyzkoušej si i špatnou verzi — `for n in numbers: if n < 0:
  numbers.remove(n)` — na vstupu `[-1, -2, 3]` a zjisti, proč nefunguje.

### Příklady vstup/výstup

| Volání                                | Výsledek          | Původní seznam po volání |
|---------------------------------------|-------------------|--------------------------|
| `add_item("a")` a pak `add_item("b")` | `['a']`, `['b']`  | —                        |
| `add_item("c", ["x"])`                | `['x', 'c']`      | —                        |
| `remove_negatives([1, -2, -3, 4])`    | `[1, 4]`          | `[1, -2, -3, 4]`         |
| `remove_negatives([-1, -2, 3])`       | `[3]`             | `[-1, -2, 3]`            |
| `remove_negatives([0, 5])`            | `[0, 5]`          | `[0, 5]`                 |
| `remove_negatives([])`                | `[]`              | `[]`                     |

## Bonus

- Napiš funkci `copy_matrix(matrix)`, která vrátí **hlubokou** kopii
  seznamu seznamů (vlastním cyklem, bez modulu `copy`) — změna v kopii se
  nesmí projevit v originálu (na rozdíl od úryvku C).
- Napiš funkci `create_grid(rows, cols, value=0)`, která past z úryvku D
  nemá.

### Příklady vstup/výstup (bonus)

| Kód                                                                 | Výsledek                         |
|---------------------------------------------------------------------|----------------------------------|
| `m = [[1, 2], [3, 4]]; c = copy_matrix(m); c[0][0] = 9; print(m)`   | `[[1, 2], [3, 4]]`               |
| `copy_matrix([])`                                                   | `[]`                             |
| `g = create_grid(2, 3); g[0][0] = 1; print(g)`                      | `[[1, 0, 0], [0, 0, 0]]`         |
| `create_grid(1, 2, "-")`                                            | `[['-', '-']]`                   |
| `create_grid(0, 3)`                                                 | `[]`                             |
