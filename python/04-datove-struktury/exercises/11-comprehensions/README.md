# 11 — Comprehensions

Zkrácený zápis vytvoření listu, dictu a setu. Každý úkol vyřeš **jedním
comprehension výrazem** (jeden řádek, žádný `append` v cyklu).

## Požadavky

Napiš funkce, které vrací výsledek jako comprehension:

1. `squares(n)` — druhé mocniny čísel `1` až `n`.
2. `evens(n)` — sudá čísla od `1` do `n` (včetně).
3. `word_lengths(words)` — dict `slovo → délka`.
4. `first_letters(words)` — **set** prvních písmen (`word[0]`).
5. `long_upper(words, min_len)` — slova delší než `min_len`, převedená na
   velká písmena (`word.upper()`).
6. `flatten(matrix)` — z matice udělej jeden plochý seznam (vnořený
   comprehension se dvěma `for`).
7. `invert(d)` — prohoď klíče a hodnoty v dictu.

Pro srovnání si u `squares` napiš i verzi s klasickým `for` cyklem
a `append`.

### Příklady vstup/výstup

| Volání                                                   | Výsledek                                   |
|----------------------------------------------------------|--------------------------------------------|
| `squares(5)`                                             | `[1, 4, 9, 16, 25]`                        |
| `squares(0)`                                             | `[]`                                       |
| `evens(10)`                                              | `[2, 4, 6, 8, 10]`                         |
| `evens(1)`                                               | `[]`                                       |
| `word_lengths(["pes", "kocka", "slon", "pes"])`          | `{'pes': 3, 'kocka': 5, 'slon': 4}`        |
| `first_letters(["pes", "papoušek", "kocka", "koza"])`    | `{'p', 'k'}` (pořadí libovolné)            |
| `first_letters([])`                                      | `set()`                                    |
| `long_upper(["pes", "kocka", "slon"], 3)`                | `['KOCKA', 'SLON']`                        |
| `long_upper(["pes"], 5)`                                 | `[]`                                       |
| `flatten([[1, 2], [3], [4, 5, 6]])`                      | `[1, 2, 3, 4, 5, 6]`                       |
| `flatten([[], []])`                                      | `[]`                                       |
| `invert({"a": 1, "b": 2, "c": 3})`                       | `{1: 'a', 2: 'b', 3: 'c'}`                 |
| `invert({"a": 1, "b": 1})`                               | `{1: 'b'}` — zjisti proč                   |

## Bonus

- `fizzbuzz(n)` — seznam od `1` do `n`, kde čísla dělitelná 3 nahradíš
  `"Fizz"`, dělitelná 5 `"Buzz"` a dělitelná oběma `"FizzBuzz"`. Jedním
  comprehension s podmíněným výrazem (`a if podmínka else b`).
- `transpose(matrix)` — transpozice matice z `09-matice`, tentokrát jako
  vnořený comprehension.

### Příklady vstup/výstup (bonus)

| Volání                                  | Výsledek                                                                 |
|-----------------------------------------|--------------------------------------------------------------------------|
| `fizzbuzz(15)`                          | `[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']` |
| `fizzbuzz(0)`                           | `[]`                                                                     |
| `transpose([[1, 2, 3], [4, 5, 6]])`     | `[[1, 4], [2, 5], [3, 6]]`                                               |
| `transpose([[7]])`                      | `[[7]]`                                                                  |
