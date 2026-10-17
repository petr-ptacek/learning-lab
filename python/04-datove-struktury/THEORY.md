# 04 — Datové struktury

## Cíl

Naučit se pracovat se čtyřmi vestavěnými kolekcemi Pythonu — `list`,
`tuple`, `dict` a `set` — a vybrat tu správnou pro daný problém. Staví na
[`03-funkce`](../03-funkce/THEORY.md) (kolekce se předávají do funkcí
a vrací z nich) a [`02-podminky-cykly`](../02-podminky-cykly/THEORY.md)
(procházení cyklem `for`). Na tomhle konceptu stojí skoro všechno další:
[`05-vestavene-funkce`](../ROADMAP.md) (`sorted`, `sum`, `zip`…) i
generátory.

Z vestavěných funkcí zatím používej jen `len()`, `range()` a převody
`list()` / `tuple()` / `dict()` / `set()`. Na `sum`, `min`, `max`,
`sorted`, `enumerate` a `zip` dojde v `05` — do té doby si je v cvičeních
napiš ručně cyklem, ať vidíš, co dělají uvnitř.

## Přehled

| Typ     | Zápis              | Měnitelný | Pořadí | Duplicity | Obdoba v JS     |
|---------|--------------------|-----------|--------|-----------|-----------------|
| `list`  | `[1, 2, 3]`        | ano       | ano    | ano       | `Array`         |
| `tuple` | `(1, 2, 3)`        | **ne**    | ano    | ano       | — (readonly pole) |
| `dict`  | `{"a": 1, "b": 2}` | ano       | ano\*  | klíče ne  | `Object` / `Map` |
| `set`   | `{1, 2, 3}`        | ano       | **ne** | **ne**    | `Set`           |

\* `dict` drží pořadí vložení (od Pythonu 3.7).

## `list` — seznam

```python
numbers = [10, 20, 30, 40, 50]

numbers[0]        # 10           první prvek
numbers[-1]       # 50           poslední prvek
numbers[1:3]      # [20, 30]     slicing: od indexu 1 do 3 (bez 3)
numbers[:2]       # [10, 20]     první dva
numbers[-2:]      # [40, 50]     poslední dva
numbers[::-1]     # [50, 40, 30, 20, 10]  obrácený (nová kopie)
len(numbers)      # 5
30 in numbers     # True
```

Index mimo rozsah (`numbers[10]`) vyhodí `IndexError`, slicing mimo
rozsah ne — vrátí jen to, co existuje.

Nejčastější metody (mění seznam **na místě** a vrací `None`):

```python
items = ["a", "b"]
items.append("c")       # ['a', 'b', 'c']      přidej na konec
items.insert(0, "z")    # ['z', 'a', 'b', 'c'] vlož na index
items.extend(["d"])     # [..., 'd']           přidej víc prvků
items.remove("a")       # odeber první výskyt (ValueError, když tam není)
last = items.pop()      # odeber a vrať poslední ('d')
first = items.pop(0)    # odeber a vrať prvek na indexu
items.index("b")        # index prvního výskytu
items.count("b")        # počet výskytů
items.sort()            # seřaď na místě
items.reverse()         # obrať na místě
items.clear()           # vyprázdni
```

Procházení:

```python
for item in items:
    print(item)

for i in range(len(items)):   # když potřebuješ i index
    print(i, items[i])
```

## `tuple` — n-tice

Jako list, ale **nejde měnit** — hodí se pro pevné skupiny hodnot, které
patří k sobě (bod `(x, y)`, RGB barva, záznam).

```python
point = (3, 4)
point[0]              # 3
point[0] = 5          # TypeError — tuple nejde měnit

single = (5,)         # jednoprvkový tuple potřebuje čárku, (5) je jen číslo
x, y = point          # rozbalení (unpacking)
a, b = b, a           # prohození dvou proměnných
```

Funkce, která vrací `return a, b`, vrací ve skutečnosti tuple
(viz `03-funkce/exercises/10-tabulka-casu`).

## `dict` — slovník

Dvojice **klíč → hodnota**. Klíč musí být neměnný (str, int, tuple).

```python
person = {"name": "Petr", "age": 30}

person["name"]              # 'Petr'
person["email"]             # KeyError — klíč neexistuje
person.get("email")         # None — bezpečné čtení
person.get("email", "-")    # '-'  — s výchozí hodnotou
person["email"] = "p@x.cz"  # přidej / přepiš
del person["age"]           # smaž (KeyError, když tam není)
person.pop("email", None)   # smaž a vrať, bez chyby s výchozí hodnotou
"name" in person            # True — testuje KLÍČE, ne hodnoty
```

Procházení:

```python
for key in person:                  # klíče
    print(key, person[key])

for key, value in person.items():   # dvojice klíč–hodnota (tuple!)
    print(f"{key}: {value}")

person.keys()     # jen klíče
person.values()   # jen hodnoty
```

Typický vzor — počítání výskytů:

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1
# {'a': 2, 'b': 1}
```

## `set` — množina

Neuspořádaná kolekce **unikátních** hodnot. Rychlý test `in`, odstranění
duplicit a množinové operace.

```python
tags = {"python", "web"}
empty = set()            # {} je prázdný DICT, ne set!

tags.add("django")
tags.remove("web")       # KeyError, když tam není
tags.discard("web")      # bez chyby, když tam není
set([1, 2, 2, 3])        # {1, 2, 3} — odstranění duplicit

a = {1, 2, 3}
b = {2, 3, 4}
a | b    # {1, 2, 3, 4}  sjednocení — aspoň v jedné
a & b    # {2, 3}        průnik — v obou
a - b    # {1}           rozdíl — jen v a
a ^ b    # {1, 4}        symetrický rozdíl — právě v jedné
```

Pořadí prvků v setu **není zaručené** — výpis se může lišit od pořadí, ve
kterém jsi prvky vkládal.

## Vnořování

Kolekce můžou obsahovat jiné kolekce:

```python
matrix = [[1, 2, 3], [4, 5, 6]]
matrix[1][2]                      # 6

products = [
    {"name": "Mléko", "price": 24.9},
    {"name": "Chléb", "price": 39.0},
]
products[0]["name"]               # 'Mléko'
```

## Měnitelnost a aliasy

Přiřazení **nekopíruje** — obě proměnné ukazují na stejný objekt
(stejně jako u objektů a polí v JS):

```python
a = [1, 2, 3]
b = a            # alias, ne kopie
b.append(4)
a                # [1, 2, 3, 4] !

c = a.copy()     # mělká kopie (stejně a[:] nebo list(a))
c.append(5)
a                # [1, 2, 3, 4] — beze změny
```

Mělká kopie kopíruje jen vnější seznam — vnořené seznamy zůstávají
sdílené:

```python
grid = [[0, 0], [0, 0]]
shallow = grid.copy()
shallow[0][0] = 9
grid             # [[9, 0], [0, 0]] !
```

Stejná past je `[[0] * 3] * 2` — vytvoří dva odkazy na **jeden** vnitřní
seznam.

Dvě časté chyby s funkcemi:

```python
def add_item(item, items=[]):   # výchozí list se vytvoří JEDNOU
    items.append(item)          # a sdílí se mezi voláními
    return items

def add_item(item, items=None): # správně
    if items is None:
        items = []
    items.append(item)
    return items
```

Funkce, která dostane list a změní ho (`append`, `remove`…), mění
**původní** list volajícího. Pokud to nechceš, vytvoř a vrať nový.

Odebírání prvků ze seznamu, který zrovna procházíš `for` cyklem, přeskakuje
prvky — místo toho sestav nový seznam.

## Comprehensions

Zkrácený zápis „vytvoř kolekci cyklem“:

```python
squares = [x ** 2 for x in range(1, 6)]           # [1, 4, 9, 16, 25]
evens = [x for x in range(10) if x % 2 == 0]      # s podmínkou
lengths = {w: len(w) for w in ["pes", "kocka"]}   # dict
letters = {w[0] for w in ["pes", "papoušek"]}     # set {'p'}
flat = [x for row in matrix for x in row]         # vnořený: [1, 2, 3, 4, 5, 6]
```

Ekvivalent prvního řádku:

```python
squares = []
for x in range(1, 6):
    squares.append(x ** 2)
```

Comprehension používej na jednoduché transformace a filtry. Když se
logika nevejde na řádek nebo potřebuješ víc kroků, napiš klasický cyklus.

## Kdy co použít

- **`list`** — pořadí hraje roli, prvky se přidávají/odebírají, můžou se
  opakovat (nákupní seznam, naměřené hodnoty).
- **`tuple`** — pevná skupina hodnot, která se nemění (bod, záznam,
  návratová hodnota s víc částmi), klíč do dictu.
- **`dict`** — hledáš podle klíče (telefonní seznam, počty výskytů,
  záznam s pojmenovanými poli).
- **`set`** — zajímá tě jen „je / není tam“, unikátnost a množinové
  operace.

Podrobnosti a další metody viz [`RESOURCES.md`](RESOURCES.md).
