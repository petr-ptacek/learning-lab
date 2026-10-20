# `*args`, `**kwargs` a rozbalování — Python obdoba JS rest/spread

Základ `*args` / `**kwargs` je v [`03-funkce/THEORY.md`](../03-funkce/THEORY.md#args-a-kwargs).
Tady je kompletní přehled včetně rozbalování při volání, v literálech a
při přiřazení, s porovnáním s JS. Výstupy jsou ověřené na Pythonu 3.14.

Oficiální docs:
[Arbitrary Argument Lists](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists),
[Unpacking Argument Lists](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists),
[PEP 448 — Additional Unpacking Generalizations](https://peps.python.org/pep-0448/).

## Přehled: JS ↔ Python

| Co | JS | Python |
|---|---|---|
| rest parametry (libovolný počet pozičních) | `function f(...args)` | `def f(*args)` → `tuple` |
| libovolné pojmenované argumenty | objekt s volbami `function f(opts)` | `def f(**kwargs)` → `dict` |
| spread seznamu do volání | `f(...arr)` | `f(*lst)` |
| spread objektu do volání | (nejde, předává se objekt) | `f(**d)` → pojmenované argumenty |
| spread v poli | `[...a, ...b]` | `[*a, *b]` |
| spread v objektu | `{...a, b: 1}` | `{**a, "b": 1}` |
| destrukturalizace pole | `const [first, ...rest] = arr` | `first, *rest = lst` |
| destrukturalizace objektu | `const { a, b } = obj` | nemá přímou obdobu (`a, b = obj["a"], obj["b"]`) |

Pravidlo: **jedna `*` = sekvence** (pozice), **dvě `**` = slovník**
(jména). V definici funkce hvězdička **sbírá**, při volání a v literálu
**rozbaluje**.

---

## 1. `*args`: sbírání pozičních argumentů

```python
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)   # 6
total()          # 0
```

- `numbers` je **`tuple`**, ne `list`. Je neměnný, takže `numbers.append(4)`
  vyhodí `AttributeError: 'tuple' object has no attribute 'append'`.
  JS `...args` je naproti tomu pole.
- Jméno je libovolné. `args` je jen konvence pro případ, kdy nic lepšího
  nenapadá. `*numbers` je čitelnější.

## 2. `**kwargs`: sbírání pojmenovaných argumentů

```python
def describe(**info):
    return info

describe(name="Petr", age=30)   # {'name': 'Petr', 'age': 30}
```

- `info` je **`dict`**: klíče jsou jména argumentů (stringy), hodnoty
  předané hodnoty.
- V JS se tohle typicky řeší objektem s volbami: `describe({ name, age })`.
  V Pythonu se jména píšou rovnou do volání.

## 3. Pořadí parametrů v definici

```python
def f(a, b=2, *args, c, d=4, **kwargs):
    return a, b, args, c, d, kwargs

f(1, 2, 3, 4, c=5, e=6)
# (1, 2, (3, 4), 5, 4, {'e': 6})
```

| Pozice | Co | V příkladu |
|---|---|---|
| 1 | běžné poziční (i s výchozí hodnotou) | `a`, `b=2` |
| 2 | `*args`: zbytek pozičních | `args = (3, 4)` |
| 3 | **keyword-only**: za `*args` jdou zadat jen jménem | `c` (povinný), `d=4` |
| 4 | `**kwargs`: zbytek pojmenovaných | `kwargs = {"e": 6}` |

`**kwargs` je vždycky poslední.

## 4. Rozbalování při volání: `f(*lst)` a `f(**d)`

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add(*nums)                       # 6   ≈ add(1, 2, 3)
add(1, *[2, 3])                  # 6   ≈ add(1, 2, 3)

opts = {"a": 1, "b": 2, "c": 3}
add(**opts)                      # 6   ≈ add(a=1, b=2, c=3)
```

- `*` rozbalí sekvenci na **poziční** argumenty, obdoba JS `add(...nums)`.
- `**` rozbalí slovník na **pojmenované** argumenty. JS nic takového
  nemá, protože JS funkce nemají pojmenované argumenty.

Chyby, na které narazíš:

```python
add(**{"a": 1, "b": 2, "x": 3})
# TypeError: add() got an unexpected keyword argument 'x'

add(1, **{"a": 1, "b": 2, "c": 3})
# TypeError: add() got multiple values for argument 'a'

describe(**{1: "x"})
# TypeError: keywords must be strings
```

## 5. Přeposílání argumentů dál (wrapper, podtřída)

Nejčastější praktické použití: funkce nebo metoda přijme „cokoliv“,
něco upraví a zbytek **předá dál beze změny**. Typicky v podtřídě:

```python
from django.http import JsonResponse


class ReadableJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)
```

1. `**kwargs` v definici **posbírá** všechny pojmenované argumenty
   (`status=404`, `safe=False`, …) do slovníku.
2. `kwargs.setdefault(klíč, hodnota)` doplní výchozí hodnotu, **jen když
   ji volající nezadal**.
3. `**kwargs` ve volání `super().__init__(...)` slovník zase **rozbalí**
   na pojmenované argumenty.

Obdoba v JS / React: `function Button({ variant = 'primary', ...rest }) { return <button {...rest} /> }`.

Obecný tvar „přijmi všechno a předej dál“ je `def wrapper(*args, **kwargs): return original(*args, **kwargs)`.
Uvidíš ho u dekorátorů.

## 6. Rozbalování v literálech (spread)

```python
a = [1, 2]
b = [3]

[*a, *b, 4]      # [1, 2, 3, 4]     ≈ JS [...a, ...b, 4]
(*a, *b)         # (1, 2, 3)        tuple
{*a, *a}         # {1, 2}           set (duplicity zmizí)
```

```python
x = {"a": 1, "b": 2}
y = {"b": 20, "c": 3}

{**x, **y}       # {'a': 1, 'b': 20, 'c': 3}  ≈ JS {...x, ...y}
x | y            # {'a': 1, 'b': 20, 'c': 3}  totéž, operátor od Pythonu 3.9
{**x, "b": 99}   # {'a': 1, 'b': 99}          přepsání klíče
{"b": 99, **x}   # {'b': 2, 'a': 1}           pozor: pozdější vyhrává
```

Stejně jako v JS: **při kolizi klíčů vyhrává ten, který je později**.

### Pozor: je to mělká kopie

```python
book = {"id": 1, "tags": ["a"]}
copy = {**book, "url": "/x/"}
copy["tags"].append("b")

book   # {'id': 1, 'tags': ['a', 'b']}  ← změnil se i originál!
```

`{**book}` zkopíruje jen první úroveň. Vnořený seznam `tags` je
**sdílený**, úplně stejně jako u JS `{...book}`. Pro hlubokou kopii slouží
`copy.deepcopy(book)` (obdoba JS `structuredClone`).

## 7. Rozbalování při přiřazení (destrukturalizace)

```python
first, *rest = [1, 2, 3, 4]    # first = 1, rest = [2, 3, 4]
*init, last = [1, 2, 3, 4]     # init = [1, 2, 3], last = 4
first, *rest = [1]             # first = 1, rest = []

p, q = 1, 2
p, q = q, p                    # prohození bez pomocné proměnné → p = 2, q = 1

k1, (k2, k3) = (1, (2, 3))     # vnořené: k1 = 1, k2 = 2, k3 = 3

for key, value in {"a": 1}.items():   # rozbalení dvojic v cyklu
    ...
```

- `*rest` při přiřazení je vždycky **`list`** (na rozdíl od `*args`
  ve funkci, což je `tuple`).
- Hvězdička může být jen **jedna** a může stát kdekoliv (`first, *middle, last`).
- Počet musí sedět, jinak `ValueError`:

  ```python
  m, n = [1, 2, 3]
  # ValueError: too many values to unpack (expected 2, got 3)
  ```

Slovník se takhle destrukturalizovat nedá. `a, b = {"a": 1, "b": 2}`
rozbalí **klíče** (`a = "a"`, `b = "b"`), ne hodnoty.

---

## Časté chyby

| Chyba | Příčina |
|---|---|
| `TypeError: … got an unexpected keyword argument 'x'` | `**d` obsahuje klíč, který funkce nemá jako parametr |
| `TypeError: … got multiple values for argument 'a'` | hodnota pro `a` přišla pozičně i jménem (`f(1, **{"a": 1})`) |
| `TypeError: keywords must be strings` | `**d` se slovníkem, který má jiné než stringové klíče |
| `AttributeError: 'tuple' object has no attribute 'append'` | `*args` je `tuple`, převeď na `list(args)` |
| `TypeError: __init__() takes 1 positional argument but 2 were given` | podtřída má `__init__(self)` bez parametrů, ale volá se s daty |
| `ValueError: too many values to unpack` | při přiřazení nesedí počet proměnných a prvků |
| změna kopie změní originál | `{**d}` / `[*a]` je mělká kopie, vnořené objekty jsou sdílené |
