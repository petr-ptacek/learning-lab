# 08 — Knihovna (závěrečné)

Všechno z konceptu dohromady: dataclass, atribut třídy s výchozí
hodnotou, kterou instance přepíše, classmethod konstruktor, property,
kontejnerové dunder metody a generátor.

## Požadavky

```python
RECORDS = [
    {"isbn": "111", "title": "R.U.R.", "author": "Karel Čapek", "year": 1920},
    {"isbn": "222", "title": "Krakatit", "author": "Karel Čapek", "year": 1924},
    {"isbn": "333", "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942},
    {"isbn": "444", "title": "Babička", "author": "Božena Němcová", "year": 1855},
]
```

- `Book` jako `@dataclass`: `isbn`, `title`, `author`, `year`,
  `available: bool = True`. `__str__` → `R.U.R. (Karel Čapek, 1920)`.
- `Member(name, max_books=None)`:
  - atribut **třídy** `max_books = 2` (výchozí limit),
  - když je `max_books` zadaný, uloží se do instance a limit třídy
    pro ni zastíní,
  - `borrowed` — seznam vypůjčených knih (každý člen vlastní!),
  - `can_borrow()` → `True`, dokud nemá vypůjčeno `max_books` knih.
- `Library`:
  - knihy drž v dictu `isbn → Book`,
  - `@classmethod from_records(cls, records)` → knihovna se všemi
    knihami (`Book(**record)`),
  - `add(book)`,
  - `__len__`, `__iter__` (prochází knihy, generátor), `__contains__(isbn)`,
  - `__str__` → `Knihovna: 4 knih, 2 k dispozici`,
  - property `available_books` → seznam dostupných knih,
  - `by_author(author)` → **generátor** knih daného autora,
  - `borrow(isbn, member)` → `True`, když kniha existuje, je dostupná
    a člen může půjčit. Pak ji označ jako nedostupnou a přidej členovi.
    Jinak `False` a nic se nemění,
  - `return_book(isbn, member)` → `True`, když ji ten člen má
    vypůjčenou. Pak ji vrať. Jinak `False`.

### Příklady vstup/výstup

Postupně za sebou:

```python
lib = Library.from_records(RECORDS)
anna = Member("Anna")
petr = Member("Petr", max_books=5)
```

| Kód                                               | Výsledek                                                   |
|---------------------------------------------------|------------------------------------------------------------|
| `str(lib)`                                        | `'Knihovna: 4 knih, 4 k dispozici'`                        |
| `len(lib), "111" in lib, "999" in lib`            | `(4, True, False)`                                         |
| `[str(b) for b in lib.by_author("Karel Čapek")]`  | `['R.U.R. (Karel Čapek, 1920)', 'Krakatit (Karel Čapek, 1924)']` |
| `list(lib.by_author("Jaroslav Hašek"))`           | `[]`                                                       |
| `anna.max_books, petr.max_books, Member.max_books`| `(2, 5, 2)`                                                |
| `lib.borrow("111", anna)`                         | `True`                                                     |
| `lib.borrow("111", petr)`                         | `False` (už je půjčená)                                    |
| `lib.borrow("222", anna)`                         | `True`                                                     |
| `lib.borrow("333", anna)`                         | `False` (Anna má limit 2)                                  |
| `lib.borrow("999", anna)`                         | `False` (neexistuje)                                       |
| `[b.title for b in anna.borrowed]`                | `['R.U.R.', 'Krakatit']`                                   |
| `petr.borrowed`                                   | `[]`                                                       |
| `str(lib)`                                        | `'Knihovna: 4 knih, 2 k dispozici'`                        |
| `lib.return_book("111", petr)`                    | `False` (Petr ji nemá)                                     |
| `lib.return_book("111", anna)`                    | `True`                                                     |
| `lib.borrow("333", anna)`                         | `True`                                                     |
| `lib.borrow("111", petr), lib.borrow("444", petr)`| `(True, True)`                                             |
| `str(lib)`                                        | `'Knihovna: 4 knih, 0 k dispozici'`                        |
| `lib.available_books`                             | `[]`                                                       |
| `str(min(lib, key=lambda b: b.year))`             | `'Babička (Božena Němcová, 1855)'`                         |
| `str(Library())`                                  | `'Knihovna: 0 knih, 0 k dispozici'`                        |

## Bonus

- `__getitem__(isbn)` → kniha podle ISBN, `lib["333"]`. Neexistující
  ISBN ať vyhodí `KeyError` (stačí nechat probublat z dictu).
- `count_by_author()` → dict `autor → počet knih`.
- `oldest_available()` → nejstarší dostupná kniha, nebo `None`.
  Jedním řádkem přes `min`.
- `stats()` → dict `{"total": ..., "available": ..., "borrowed": ...}`.

### Příklady vstup/výstup (bonus)

Na **nové** knihovně `lib2 = Library.from_records(RECORDS)`:

| Kód                                    | Výsledek                                                              |
|----------------------------------------|-----------------------------------------------------------------------|
| `str(lib2["333"])`                     | `'Saturnin (Zdeněk Jirotka, 1942)'`                                   |
| `lib2["999"]`                          | `KeyError: '999'`                                                     |
| `lib2.count_by_author()`               | `{'Karel Čapek': 2, 'Zdeněk Jirotka': 1, 'Božena Němcová': 1}`        |
| `Library().count_by_author()`          | `{}`                                                                  |
| `lib2.stats()`                         | `{'total': 4, 'available': 4, 'borrowed': 0}`                         |
| `str(lib2.oldest_available())`         | `'Babička (Božena Němcová, 1855)'`                                    |
| po `lib2.borrow("444", Member("Eva"))`: `str(lib2.oldest_available())` | `'R.U.R. (Karel Čapek, 1920)'`        |
| …a `lib2.stats()`                      | `{'total': 4, 'available': 3, 'borrowed': 1}`                         |
| `Library().oldest_available()`         | `None`                                                                |
