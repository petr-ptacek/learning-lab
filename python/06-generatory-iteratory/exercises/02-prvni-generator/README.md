# 02 — První generátor

`yield` místo `return` + `append`. Funkce, která hodnoty vydává
postupně a mezi nimi spí.

## Požadavky

- **Předpověď:** v jakém pořadí se vypíšou řádky? Napiš si odpověď do
  komentáře, pak spusť a porovnej:

  ```python
  def noisy():
      print("start")
      yield 1
      print("mezi")
      yield 2
      print("konec")


  gen = noisy()
  print("vytvořeno")
  print(next(gen))
  print(next(gen))
  print(list(gen))
  ```

  Proč se `start` nevypíše hned při `gen = noisy()`? A co vrátí
  `type(noisy())`?

- Napiš tyto generátorové funkce (každá s `yield`, žádný seznam uvnitř):
  - `countdown(n)` — vydá `n, n-1, …, 1`. Pro `n <= 0` nic.
  - `evens(limit)` — sudá čísla od `0` do `limit` (bez něj, jako
    `range`).
  - `repeat(value, times)` — vydá `value` `times`-krát.
- Výsledek vypisuj přes `list(...)`.

### Příklady vstup/výstup

| Volání                      | Výsledek               |
|-----------------------------|------------------------|
| `list(countdown(3))`        | `[3, 2, 1]`            |
| `list(countdown(1))`        | `[1]`                  |
| `list(countdown(0))`        | `[]`                   |
| `list(countdown(-2))`       | `[]`                   |
| `list(evens(7))`            | `[0, 2, 4, 6]`         |
| `list(evens(8))`            | `[0, 2, 4, 6]`         |
| `list(evens(1))`            | `[0]`                  |
| `list(evens(0))`            | `[]`                   |
| `list(repeat("ab", 3))`     | `['ab', 'ab', 'ab']`   |
| `list(repeat("x", 0))`      | `[]`                   |

## Bonus

- `running_total(numbers)` — průběžné součty: po každém čísle vydá
  součet všech dosavadních. Generátor si mezi `yield` pamatuje stav
  v lokální proměnné.
- `with_index(items, start=0)` — vlastní `enumerate`: vydává dvojice
  `(index, prvek)`. Ověř, že
  `list(with_index("abc", 5)) == list(enumerate("abc", 5))`.

### Příklady vstup/výstup (bonus)

| Volání                               | Výsledek                              |
|--------------------------------------|---------------------------------------|
| `list(running_total([1, 2, 3, 4]))`  | `[1, 3, 6, 10]`                       |
| `list(running_total([5, -5, 2]))`    | `[5, 0, 2]`                           |
| `list(running_total([]))`            | `[]`                                  |
| `list(with_index("abc"))`            | `[(0, 'a'), (1, 'b'), (2, 'c')]`      |
| `list(with_index(["x", "y"], 1))`    | `[(1, 'x'), (2, 'y')]`                |
| `list(with_index([]))`               | `[]`                                  |
