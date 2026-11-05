# 04 — `collections.abc`: napiš pár metod, zbytek zdědíš

V `07` jsi pro `Playlist` psal ručně `__len__`, `__iter__`,
`__contains__`, `__getitem__`… Abstraktní třídy z `collections.abc`
fungují opačně: napíšeš jen **povinné** metody a ostatní dostaneš od
rodiče hotové. Je to dědičnost jako „hotové chování“. Django dělá totéž
s formuláři, modely i views.

Teorie: [`docs/ABSTRACT_BASE_CLASSES.md`](../../../docs/ABSTRACT_BASE_CLASSES.md).

## Požadavky

- `Playlist(Sequence)` (`from collections.abc import Sequence`):
  - `__init__(self, name, songs=())`, písně (stringy) si ulož jako
    vlastní seznam,
  - napiš **jen** `__getitem__` a `__len__`. Nic dalšího.
  - Ověř, že přesto funguje `in`, `for`, `reversed`, `.index()`
    a `.count()`. Odkud se vzaly? (`"index" in vars(Playlist)` vs.
    `"index" in vars(Sequence)`.)
- `CaseInsensitiveDict(MutableMapping)`: slovník, kterému je jedno,
  jestli klíč napíšeš velkými nebo malými písmeny (jako HTTP hlavičky,
  Django má `request.headers` přesně takové):
  - `__init__(self, data=())` — počáteční data nahraj přes `self.update(data)`,
    tedy metodou, kterou sám nepíšeš,
  - uvnitř drž obyčejný dict, klíče ukládej převedené přes `casefold()`,
  - napiš **jen** pět povinných metod: `__getitem__`, `__setitem__`,
    `__delitem__`, `__iter__`, `__len__` (a `__repr__` pro hezký výpis
    `CaseInsensitiveDict({'accept': 'json'})`),
  - zdarma tak dostaneš `get`, `update`, `pop`, `setdefault`, `items`,
    `keys`, `in` i `==`.
- **Předpověď:** co se stane?

  ```python
  class Broken(Sequence):
      def __getitem__(self, index):
          return index


  Broken()
  ```

  Jak se z chybové hlášky dozvíš, co ještě musíš napsat?

### Příklady vstup/výstup

`p = Playlist("Ráno", ["Imagine", "Hey Jude", "Imagine", "Yesterday"])`:

| Kód                                      | Výsledek                                              |
|------------------------------------------|-------------------------------------------------------|
| `len(p)`, `p[0]`, `p[-1]`                | `4`, `'Imagine'`, `'Yesterday'`                       |
| `p[1:3]`                                 | `['Hey Jude', 'Imagine']`                             |
| `"Hey Jude" in p, "Help" in p`           | `(True, False)`                                       |
| `list(reversed(p))`                      | `['Yesterday', 'Imagine', 'Hey Jude', 'Imagine']`     |
| `p.index("Hey Jude")`, `p.count("Imagine")` | `1`, `2`                                           |
| `p.index("Help")`                        | `ValueError`                                          |
| `sorted(p)`                              | `['Hey Jude', 'Imagine', 'Imagine', 'Yesterday']`     |
| `bool(Playlist("Prázdný"))`              | `False`                                               |
| `isinstance(p, Sequence)`                | `True`                                                |
| `"index" in vars(Playlist), "index" in vars(Sequence)` | `(False, True)`                         |
| `Broken()` (z předpovědi)                | `TypeError: Can't instantiate abstract class Broken without an implementation for abstract method '__len__'` |

`h = CaseInsensitiveDict({"Content-Type": "text/html"})`, postupně:

| Kód                                          | Výsledek                                                                 |
|----------------------------------------------|--------------------------------------------------------------------------|
| `h["content-type"]`, `h["CONTENT-TYPE"]`     | `'text/html'`, `'text/html'`                                             |
| `"Content-type" in h`                        | `True`                                                                   |
| `h.get("Accept")`, `h.get("accept", "*/*")`  | `None`, `'*/*'`                                                          |
| `h["Accept"] = "json"`, `len(h)`, `h`        | `2`, `CaseInsensitiveDict({'content-type': 'text/html', 'accept': 'json'})` |
| `h.update({"ACCEPT": "xml", "Host": "example.cz"})`, `dict(h.items())` | `{'content-type': 'text/html', 'accept': 'xml', 'host': 'example.cz'}` |
| `h.setdefault("host", "jiny.cz")`            | `'example.cz'` (už existuje)                                             |
| `h.setdefault("X-Id", "1")`, `h.pop("x-ID")` | `'1'`, `'1'`                                                             |
| `h.pop("nic", None)`                         | `None`                                                                   |
| `del h["HOST"]`, `list(h)`                   | `['content-type', 'accept']`                                             |
| `h == {"content-type": "text/html", "accept": "xml"}` | `True`                                                          |
| `h == {"Content-Type": "text/html", "accept": "xml"}` | `False` (obyčejný dict velikost písmen řeší)                    |
| `h["nic"]`                                   | `KeyError: 'nic'`                                                        |
| `CaseInsensitiveDict()`                      | `CaseInsensitiveDict({})`                                                |
| `isinstance(h, MutableMapping), isinstance(h, dict)` | `(True, False)`                                                  |

## Bonus

- `OrderedSet(MutableSet)`: množina, která si pamatuje **pořadí
  vložení** (obyčejný `set` ho nedrží):
  - `__init__(self, iterable=())`,
  - povinné: `__contains__`, `__iter__`, `__len__`, `add`, `discard`,
    plus `__repr__` → `OrderedSet([3, 1, 2])`,
  - tip: jako úložiště se hodí dict s hodnotami `None`, ten pořadí drží
    a hledá rychle,
  - zdarma dostaneš `|`, `&`, `-`, `^`, `<=`, `==`, `isdisjoint`,
    `remove`, `pop`.
- **Otázka:** proč musí `__init__` přijmout iterable? Zkus napsat
  variantu s `__init__(self)` bez parametru a spusť `a | b`. Kde
  rodičovská třída volá tvůj konstruktor? (Nápověda: hledej
  `_from_iterable` v dokumentaci `collections.abc`.)

### Příklady vstup/výstup (bonus)

`a = OrderedSet([3, 1, 3, 2, 1])`, `b = OrderedSet([2, 5, 3])`:

| Kód                                       | Výsledek                                       |
|-------------------------------------------|------------------------------------------------|
| `a`, `len(a)`                             | `OrderedSet([3, 1, 2])`, `3`                   |
| `list(set([3, 1, 3, 2, 1]))`              | `[1, 2, 3]` (pro srovnání)                     |
| `a \| b`                                  | `OrderedSet([3, 1, 2, 5])`                     |
| `a & b`                                   | `OrderedSet([2, 3])` (pořadí podle `b`)        |
| `a - b`, `b - a`                          | `OrderedSet([1])`, `OrderedSet([5])`           |
| `a ^ b`                                   | `OrderedSet([1, 5])`                           |
| `OrderedSet([1, 2]) <= a`, `a <= b`       | `True`, `False`                                |
| `a.isdisjoint(OrderedSet([7, 8]))`        | `True`                                         |
| `a == OrderedSet([1, 2, 3])`, `a == {1, 2, 3}` | `True`, `True` (rovnost pořadí neřeší)    |
| `OrderedSet("abrakadabra")`               | `OrderedSet(['a', 'b', 'r', 'k', 'd'])`        |
| `OrderedSet()`                            | `OrderedSet([])`                               |
| `a.add(0)`, `a.discard(3)`, `a.discard(99)`, `a` | `OrderedSet([1, 2, 0])`                 |
| `a.remove(1)`, `a`                        | `OrderedSet([2, 0])`                           |
| `a.remove(99)`                            | `KeyError: 99`                                 |
| `a \| b` u varianty s `__init__(self)`    | `TypeError: NoArgs.__init__() takes 1 positional argument but 2 were given` (jméno třídy podle tvé) |
