# 06 — Yield from

`yield from` předá všechny hodnoty z jiného iterable. Spolu s rekurzí
z `03-funkce` prochází libovolně hluboké struktury.

## Požadavky

- Napiš generátor `chain(*iterables)` — vydá postupně všechny prvky ze
  všech předaných iterables. S `yield from`.
- Napiš rekurzivní generátor `flatten(nested)` — „zploští“ libovolně
  vnořené seznamy. Prvek, který je seznam, rozbal (rekurzivně), ostatní
  vydej tak, jak jsou. Rozlišení přes `isinstance(x, list)` (viz
  `THEORY.md`). Stringy se nerozkládají na znaky.
- Rozmysli si (komentářem): co je u `flatten` základní případ rekurze?

### Příklady vstup/výstup

| Volání                                         | Výsledek                       |
|------------------------------------------------|--------------------------------|
| `list(chain([1, 2], "ab", range(2)))`          | `[1, 2, 'a', 'b', 0, 1]`       |
| `list(chain([], [3]))`                         | `[3]`                          |
| `list(chain())`                                | `[]`                           |
| `list(flatten([1, [2, [3, [4]]], 5]))`         | `[1, 2, 3, 4, 5]`              |
| `list(flatten([1, 2, 3]))`                     | `[1, 2, 3]`                    |
| `list(flatten(["ab", ["cd"]]))`                | `['ab', 'cd']`                 |
| `list(flatten([[], [[]]]))`                    | `[]`                           |
| `list(flatten([]))`                            | `[]`                           |

## Bonus

- `walk(node)` — projde strom složek a vydá **cestu** ke každé položce
  (`rodič/dítě`), do hloubky, v pořadí, v jakém jsou v `children`.
  Uzel je dict `{"name": ..., "children": [...]}`. Nápověda: cestu
  rodiče předávej rekurzí jako další parametr s výchozí hodnotou.

  ```python
  tree = {"name": "src", "children": [
      {"name": "app", "children": [
          {"name": "main.py", "children": []},
          {"name": "utils.py", "children": []},
      ]},
      {"name": "README.md", "children": []},
  ]}
  ```

### Příklady vstup/výstup (bonus)

| Volání                                      | Výsledek                                                                          |
|---------------------------------------------|-----------------------------------------------------------------------------------|
| `list(walk(tree))`                          | `['src', 'src/app', 'src/app/main.py', 'src/app/utils.py', 'src/README.md']`      |
| `list(walk({"name": "x", "children": []}))` | `['x']`                                                                           |
