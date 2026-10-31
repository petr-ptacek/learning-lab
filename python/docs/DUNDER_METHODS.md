# Dunder metody

Výtah z Real Python *Python's Magic Methods: Leverage Their Power in
Your Classes* a *When Should You Use .\_\_repr\_\_() vs .\_\_str\_\_()*,
plus [Data model](https://docs.python.org/3/reference/datamodel.html#special-method-names)
z oficiální reference. Odkazy jsou v
[`07-oop-zaklady/RESOURCES.md`](../07-oop-zaklady/RESOURCES.md),
přehled v [`THEORY.md`](../07-oop-zaklady/THEORY.md#dunder-metody-jak-se-třída-chová-k-operátorům-a-vestavěným-funkcím).

Dunder metody (*double underscore*, `__jméno__`, taky „magické“ nebo
„speciální“) jsou háčky, přes které Python volá tvou třídu, když na ni
použiješ operátor nebo vestavěnou funkci. `len(x)` zavolá
`x.__len__()`, `a + b` zavolá `a.__add__(b)` a tak dál. Díky nim se
vlastní třída chová jako vestavěný typ.

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [`__str__` vs. `__repr__`](#1-__str__-vs-__repr__)
2. [`__eq__` a `NotImplemented`](#2-__eq__-a-notimplemented)
3. [`__eq__` a `__hash__`](#3-__eq__-a-__hash__)
4. [Řazení: `__lt__` a `total_ordering`](#4-řazení-__lt__-a-total_ordering)
5. [Aritmetika: `__add__`, `__radd__` a `sum`](#5-aritmetika-__add__-__radd__-a-sum)
6. [Kontejner: `__len__`, `__iter__`, `__contains__`, `__getitem__`](#6-kontejner-__len__-__iter__-__contains__-__getitem__)
7. [Pravdivost: `__bool__`](#7-pravdivost-__bool__)
8. [Volatelný objekt: `__call__`](#8-volatelný-objekt-__call__)
9. [Přehledová tabulka](#9-přehledová-tabulka)

---

## 1. `__str__` vs. `__repr__`

| | `__str__` | `__repr__` |
|---|---|---|
| pro koho | uživatel | programátor (ladění, logy, konzole) |
| volá ho | `print(x)`, `str(x)`, `f"{x}"` | `repr(x)`, konzole, **výpis uvnitř kolekce**, `f"{x!r}"` |
| cíl | čitelné | jednoznačné, ideálně platný Python, který objekt vyrobí |
| když chybí | použije se `__repr__` | `<__main__.Money object at 0x...>` |

```python
class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"


m = Money(249.9)
print(m)                  # 249.90 CZK
str(m)                    # '249.90 CZK'
repr(m)                   # "Money(249.9, 'CZK')"
[m, Money(10, "EUR")]     # [Money(249.9, 'CZK'), Money(10, 'EUR')]
f"{m} / {m!r}"            # "249.90 CZK / Money(249.9, 'CZK')"
```

Pozor na výpis kolekcí: `print([m])` vypíše `repr` prvků, ne `str`.
Proto se vyplatí psát **vždycky aspoň `__repr__`**. Když je jen jeden,
použije se i pro `print`.

`!r` ve f-stringu volá `repr()`. U stringů přidá uvozovky, takže
`Money(249.9, 'CZK')` je platný Python. Bez `!r` by vyšlo
`Money(249.9, CZK)`.

V Djangu: `__str__` modelu vidíš v adminu (seznam, výběrová pole
cizích klíčů), v `manage.py shell` i v chybových hláškách. Model bez
`__str__` se v adminu zobrazí jako `Book object (1)`.

## 2. `__eq__` a `NotImplemented`

Bez `__eq__` porovná `==` **identitu**: `True` jen pro tentýž objekt
(jako `is`).

```python
class Plain:
    def __init__(self, x):
        self.x = x


Plain(1) == Plain(1)      # False
```

S `__eq__` rozhoduješ ty:

```python
class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)


Money(10, "EUR") == Money(10, "EUR")    # True
Money(10, "EUR") == Money(10, "CZK")    # False
Money(10) == 10                         # False
Money(10) != Money(11)                  # True — != se dopočítá z __eq__ samo
```

`NotImplemented` (ne `NotImplementedError`!) je zvláštní hodnota,
která znamená „s tímhle typem porovnávat neumím“. Python pak zkusí
druhou stranu (`other.__eq__(self)`), a když ani ta neumí, u `==`
vrátí `False` a u `<` nebo `+` vyhodí `TypeError`. Je to správnější než
`return False`, protože druhá strana dostane šanci.

Porovnání přes tuple `(a, b) == (c, d)` je běžný idiom, ušetří řetěz
`and`.

## 3. `__eq__` a `__hash__`

`set` a klíče `dict` potřebují **hash**: číslo spočítané z hodnoty,
podle kterého se prvek rychle najde. Pravidlo zní: **co je si rovné
(`==`), musí mít stejný hash.**

Výchozí hash je odvozený z identity, a to by s vlastním `__eq__`
nesedělo. Python proto při definici `__eq__` hash **vypne**:

```python
Money.__hash__            # None
{Money(1)}                # TypeError: cannot use 'Money' as a set element (unhashable type: 'Money')
```

Řešení: hash ze stejných hodnot, které porovnává `__eq__`:

```python
class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __hash__(self):
        return hash((self.amount, self.currency))


len({Money(1), Money(1), Money(2)})     # 2
```

Háček: když se objekt **změní** poté, co je v setu, změní se mu hash
a set ho už nenajde. Hashovatelné by proto měly být jen objekty, které
se nemění. Pro takové třídy je nejpohodlnější
`@dataclass(frozen=True)` (viz [`DATACLASSES.md`](DATACLASSES.md)),
ta vygeneruje `__eq__` i `__hash__` a zakáže změny.

Django modely mají `__eq__` i `__hash__` podle primárního klíče. Dvě
instance načtené z DB pro stejný řádek jsou si rovné.

## 4. Řazení: `__lt__` a `total_ordering`

`sorted`, `min`, `max` a `<` potřebují `__lt__` (*less than*):

```python
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __repr__(self):
        return f"Version({self.major}, {self.minor})"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) < (other.major, other.minor)


versions = [Version(1, 10), Version(1, 2), Version(0, 9)]
sorted(versions)                       # [Version(0, 9), Version(1, 2), Version(1, 10)]
max(versions)                          # Version(1, 10)
Version(2, 0) > Version(1, 9)          # True — Python otočí na Version(1, 9) < Version(2, 0)
Version(1, 0) <= Version(1, 0)         # TypeError: '<=' not supported between instances of 'Version' and 'Version'
```

`>` si Python dopočítá z `__lt__` druhé strany, `<=` ani `>=` ne.
Když chceš všechny čtyři, nemusíš je psát ručně:

```python
from functools import total_ordering


@total_ordering
class Version2:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)


Version2(1, 0) <= Version2(1, 0)       # True
```

Ještě jednodušší je `@dataclass(order=True)`. A když potřebuješ
seřadit jen jednou a jinak, než je přirozené pořadí, stačí
`sorted(items, key=...)` a žádné dunder metody nejsou potřeba.

## 5. Aritmetika: `__add__`, `__radd__` a `sum`

```python
class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(round(self.amount + other.amount, 2), self.currency)


Money(0.1) + Money(0.2)                # Money(0.3, 'CZK')
Money(1) + Money(1, "EUR")             # TypeError: unsupported operand type(s) for +: 'Money' and 'Money'
```

`__add__` vrací **nový** objekt, ten původní nemění. Stejně jako
`1 + 2` nemění jedničku.

`sum()` začíná od `0`, takže první krok je `0 + Money(...)`. `int`
neumí sčítat s `Money`, a tak Python zkusí **otočenou** metodu
`Money.__radd__` (*reflected add*). Bez ní:

```python
sum([Money(1), Money(2)])              # TypeError: unsupported operand type(s) for +: 'int' and 'Money'
sum([Money(1), Money(2)], Money(0))    # Money(3, 'CZK') — začátek zadaný ručně
```

S `__radd__` funguje i obyčejné `sum`:

```python
def money_radd(self, other):
    if other == 0:
        return self
    return NotImplemented


Money.__radd__ = money_radd            # (jen pro ukázku; normálně ji napiš do třídy)
sum([Money(1), Money(2)])              # Money(3, 'CZK')
```

Další operátory fungují stejně: `__sub__` (`-`), `__mul__` (`*`),
`__truediv__` (`/`), `__neg__` (`-x`). Každý má i verzi `__r...__`
a `__i...__` (`+=`).

## 6. Kontejner: `__len__`, `__iter__`, `__contains__`, `__getitem__`

Třída, která v sobě drží kolekci, se může chovat jako seznam:

```python
class Playlist:
    def __init__(self, songs):
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        yield from self.songs            # generátor, viz 06

    def __contains__(self, song):
        return song in self.songs

    def __getitem__(self, index):
        return self.songs[index]         # deleguje i slicing a záporné indexy


p = Playlist(["Imagine", "Hey Jude", "Yesterday"])
len(p)                    # 3
list(p)                   # ['Imagine', 'Hey Jude', 'Yesterday']
"Imagine" in p            # True
p[0], p[-1]               # ('Imagine', 'Yesterday')
p[:2]                     # ['Imagine', 'Hey Jude']
list(reversed(p))         # ['Yesterday', 'Hey Jude', 'Imagine']
sorted(p)                 # ['Hey Jude', 'Imagine', 'Yesterday']
```

Co z čeho Python odvodí:

| Máš | Zadarmo dostaneš |
|---|---|
| `__iter__` | `for`, `list()`, `sorted`, `sum`, `max`, rozbalování, a `in` (projde všechno) |
| `__len__` | `len()`, a pravdivost: prázdný = `False` |
| `__len__` + `__getitem__` s čísly | `reversed()` |
| `__contains__` | rychlejší nebo jinak definované `in` (třeba hledání podle jména) |

Jen s `__iter__` to funguje taky, ale `len` ne:

```python
class OnlyIter:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        yield from self.items


o = OnlyIter([1, 2])
2 in o                    # True
len(o)                    # TypeError: object of type 'OnlyIter' has no len()
```

Django QuerySet má všechny čtyři: `len(qs)`, `for book in qs`,
`qs[:10]` (z toho se stane `LIMIT 10` v SQL), `if qs:`.

## 7. Pravdivost: `__bool__`

`if x:` a `bool(x)` zkusí `__bool__`, pak `__len__` (nula = `False`),
a když chybí obojí, je objekt **vždy `True`**.

```python
bool(Playlist([]))        # False — přes __len__
bool(Plain(0))            # True — nemá ani __bool__, ani __len__
```

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __bool__(self):
        return self.amount != 0


bool(Money(0)), bool(Money(0.01))   # (False, True)
```

## 8. Volatelný objekt: `__call__`

Instance s `__call__` jde zavolat jako funkce. Na rozdíl od funkce si
ale drží stav v atributech:

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor


double = Multiplier(2)
double(21)                         # 42
list(map(double, [1, 2, 3]))       # [2, 4, 6]
callable(double)                   # True
```

V Djangu je takhle napsaný middleware (`__call__(self, request)`)
a validátory polí.

## 9. Přehledová tabulka

| Kategorie | Metoda | Spustí ji |
|---|---|---|
| vznik | `__init__(self, ...)` | `Třída(...)` |
| text | `__str__`, `__repr__` | `print`, `str`, `repr`, f-string |
| porovnání | `__eq__`, `__ne__` | `==`, `!=` |
| | `__lt__`, `__le__`, `__gt__`, `__ge__` | `<`, `<=`, `>`, `>=`, `sorted`, `min`, `max` |
| hash | `__hash__` | `set`, klíč `dict`, `hash()` |
| aritmetika | `__add__`, `__sub__`, `__mul__`, `__truediv__` | `+`, `-`, `*`, `/` |
| | `__radd__` … | když levá strana neumí (`0 + x` v `sum`) |
| | `__iadd__` … | `+=` (když chybí, použije se `__add__`) |
| kontejner | `__len__` | `len()` |
| | `__iter__` | `for`, `list()`, … |
| | `__contains__` | `in` |
| | `__getitem__`, `__setitem__`, `__delitem__` | `x[k]`, `x[k] = v`, `del x[k]` |
| pravdivost | `__bool__` | `if x:`, `bool()` |
| volání | `__call__` | `x(...)` |
| kontext | `__enter__`, `__exit__` | `with` (v `11-soubory`) |

Pravidla:

- dunder metody **nevolej přímo** (`x.__len__()`), vždy přes `len(x)`,
- **nevymýšlej vlastní** `__jména__`, jsou rezervované pro Python,
- vrať `NotImplemented`, když druhý operand je typ, se kterým neumíš
  pracovat.
