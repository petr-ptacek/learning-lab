# Generátory a iterátory do hloubky

Výtah z článků, na které odkazuje
[`06-generatory-iteratory/RESOURCES.md`](../06-generatory-iteratory/RESOURCES.md)
(hlavně Real Python *Iterators and Iterables* a *How to Use Generators
and yield*, plus *Functional Programming HOWTO* z oficiálních docs).
Přehled konceptu je v [`THEORY.md`](../06-generatory-iteratory/THEORY.md),
tady je to, co se do přehledu nevešlo: jak to funguje uvnitř, pasti
a vzory z praxe. Hotové nástroje modulu `itertools` jsou zvlášť
v [`ITERTOOLS.md`](ITERTOOLS.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.
Jak otypovat parametr, který jde procházet (`Iterable[int]`), a generátor
(`Iterator[int]`), je v [`TYPE_HINTS.md`](TYPE_HINTS.md#generátory).

## Obsah

1. [Iterační protokol: `__iter__` a `__next__`](#1-iterační-protokol-__iter__-a-__next__)
2. [Iterable vs. iterátor: kdo se dá projít víckrát](#2-iterable-vs-iterátor-kdo-se-dá-projít-víckrát)
3. [Život generátoru](#3-život-generátoru)
4. [`yield from` a `return` v generátoru](#4-yield-from-a-return-v-generátoru)
5. [Kdy se co vyhodnotí v generátorovém výrazu](#5-kdy-se-co-vyhodnotí-v-generátorovém-výrazu)
6. [Pasti](#6-pasti)
7. [`iter(funkce, zarážka)`](#7-iterfunkce-zarážka)
8. [Vzory z praxe](#8-vzory-z-praxe)
9. [Výkon: kdy generátor, kdy seznam](#9-výkon-kdy-generátor-kdy-seznam)
10. [Srovnání s JS](#10-srovnání-s-js)

---

## 1. Iterační protokol: `__iter__` a `__next__`

Všechno iterování v Pythonu stojí na dvou metodách. Třídy přijdou až
v `07-oop-zaklady`, tady jen pro představu, co `iter()` a `next()` volají:

| Volání | Volá na objektu | Vrací |
|---|---|---|
| `iter(x)` | `x.__iter__()` | iterátor |
| `next(it)` | `it.__next__()` | další hodnotu, nebo vyhodí `StopIteration` |

Iterátor napsaný ručně jako třída:

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self              # iterátor je sám sobě iterable

    def __next__(self):
        if self.current <= 0:
            raise StopIteration  # konec
        value = self.current
        self.current -= 1
        return value


list(Countdown(3))   # [3, 2, 1]
```

Totéž jako generátor:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

Generátor je **zkratka pro psaní iterátorů**. Python za tebe vyrobí
`__iter__`, `__next__`, uložení stavu i `StopIteration`. Třídu se
`__next__` píšeš jen výjimečně, když iterátor potřebuje další metody
nebo veřejný stav.

## 2. Iterable vs. iterátor: kdo se dá projít víckrát

Rozdíl, na kterém lidé nejčastěji narazí:

```python
c = Countdown(2)
list(c)   # [2, 1]
list(c)   # [] — Countdown je iterátor, vyčerpal se
```

**Iterable** (seznam, string, dict, `range`) si iterátor vyrábí při
každém `iter()` znovu, proto ho jde projít kolikrát chceš. **Iterátor**
má jen jeden stav a jde jen dopředu.

Iterable, který jde projít opakovaně, dostaneš tak, že `__iter__` je
**generátor**. Každé `iter()` pak vytvoří nový:

```python
class Countdown2:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1


c2 = Countdown2(2)
list(c2)   # [2, 1]
list(c2)   # [2, 1] — pokaždé nový generátor
```

Rychlý test, co máš v ruce: `iter(x) is x` → `True` znamená iterátor
(jednorázový), `False` iterable (opakovatelný).

| Typ | Opakovatelný? |
|---|---|
| `list`, `tuple`, `str`, `dict`, `set`, `range` | ano |
| `dict.keys()` / `.values()` / `.items()` | ano (jsou to „pohledy“ na dict) |
| `map`, `filter`, `zip`, `enumerate`, `reversed` | ne |
| generátor, generátorový výraz | ne |
| otevřený soubor | ne (čte se od aktuální pozice) |

## 3. Život generátoru

Generátor prochází stavy, dají se vypsat přes `inspect`:

```python
import inspect


def gen_fn():
    yield 1


g = gen_fn()
inspect.getgeneratorstate(g)   # 'GEN_CREATED'   — vytvořen, tělo neběželo
next(g)
inspect.getgeneratorstate(g)   # 'GEN_SUSPENDED' — stojí na yield
next(g, None)
inspect.getgeneratorstate(g)   # 'GEN_CLOSED'    — doběhl
```

Mezi `yield` si generátor pamatuje **celý rámec funkce**: lokální
proměnné, místo v kódu, rozběhnuté cykly. Proto v něm může být
`while True` nebo `for` přes soubor a nic se „neztratí“. Ukončení
přes `close()` a úklid ve `finally` popisuje
[`THEORY.md`](../06-generatory-iteratory/THEORY.md#close-send-throw--metody-generátoru).

## 4. `yield from` a `return` v generátoru

### Co dělá `yield from`

Při běžném procházení dělají tyhle dva zápisy totéž:

```python
yield from other

for value in other:
    yield value
```

Generátor vezme **všechny hodnoty** z `other` a vydá je jednu po druhé
dál, jako by je vydával sám. Volající nepozná, že pocházejí odjinud.
`other` může být jakýkoliv iterable: seznam, string, `range`, jiný
generátor. JS obdoba je `yield* other` ve `function*`.

### `yield` vs. `yield from`: krabice vs. obsah

Volání generátorové funkce nic nespustí, jen vyrobí generátor (viz
[sekce 3](#3-život-generátoru)). Hodnoty z něj musí někdo vytáhnout:

```python
def inner():
    yield "a"
    yield "b"


def outer_wrong():
    yield inner()          # vydá JEDNU hodnotu: samotný generátor


def outer_right():
    yield from inner()     # vydá "a", pak "b"


list(outer_wrong())   # [<generator object inner at 0x...>]
list(outer_right())   # ['a', 'b']
```

`yield` pošle generátor nahoru jako jednu zavřenou krabici.
`yield from` krabici otevře a pošle nahoru její obsah.

### Rekurze: hodnoty probublávají nahoru

U rekurzivního generátoru (cvičení `06-yield-from`) se to děje na
každé úrovni:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


list(flatten([1, [2, [3]]]))   # [1, 2, 3]
```

```
flatten([3])            vydá 3
flatten([2, [3]])       vydá 2, přes yield from přepošle 3
flatten([1, [2, [3]]])  vydá 1, přes yield from přepošle 2, 3
list(...)               dostane 1, 2, 3
```

Každá úroveň vydá své hodnoty a přepošle nahoru všechno, co vydaly
úrovně pod ní. Dvě časté chyby v rekurzi:

| Zápis v rekurzivní větvi | Výsledek pro `[1, [2, [3]]]` | Co se stalo |
|---|---|---|
| `yield flatten(item)` | `[1, <generator object ...>]` | nahoru odešla zavřená krabice |
| `flatten(item)` (bez `yield`) | `[1]` | generátor se vyrobil, ale nikdo ho nespustil, hodnoty se ztratily |

### `return` v generátoru

`return hodnota` v generátoru sekvenci ukončí. Hodnota se při běžném
procházení (`for`, `list`) **zahodí**. Dostaneš ji jen jako výsledek
`yield from`:

```python
def with_result():
    yield 1
    yield 2
    return "hotovo"


def outer():
    result = yield from with_result()
    print("vnitřní vrátil:", result)


list(outer())
# vypíše: vnitřní vrátil: hotovo
# vrátí:  [1, 2]
```

V běžném kódu `return` v generátoru používáš bez hodnoty, jako
předčasný konec („už nic dalšího nevydám“).

### Víc než zkratka

`yield from x` je víc než `for v in x: yield v`: vrací hodnotu z
`return` (viz výše) a přeposílá i `send`, `throw` a `close` do vnitřního
generátoru. Pro běžné použití z toho plyne jen tohle: když skládáš
generátory, používej `yield from`, ne ruční cyklus.

## 5. Kdy se co vyhodnotí v generátorovém výrazu

Generátorový výraz je líný, ale **ne celý**. Iterable v prvním `for` se
vyhodnotí hned při vytvoření, všechno ostatní až při procházení:

```python
data = [1, 5, 10]
limit = 3
gen = (x for x in data if x > limit)
limit = 7
list(gen)    # [10] — podmínka použila limit až při čtení, tedy 7
```

```python
data = [1, 5, 10]
gen = (x for x in data)
data = [100]
list(gen)    # [1, 5, 10] — `data` se vzalo při vytvoření
```

Ponaučení: proměnné, které generátor používá, mezi vytvořením
a přečtením neměň. Nebo generátor vytvoř až těsně před použitím.

## 6. Pasti

| Situace | Co se stane | Řešení |
|---|---|---|
| `x in iterator` | vyčerpá iterátor **až po nalezený prvek**: `2 in it` u `iter([1, 2, 3, 4])` → `True`, zbyde `[3, 4]` | `in` používej na seznamu nebo množině |
| stejný generátor do dvou funkcí: `sum(g)`, pak `max(g)` | druhá dostane prázdný: `6`, pak chyba / `default` | ulož `list(g)`, nebo vytvoř generátor dvakrát |
| `if gen:` | generátor je **vždy truthy**, i prázdný: `bool(n for n in [])` → `True` | `first = next(gen, None)` a testuj to |
| `print(gen)` při ladění | vypíše `<generator object ...>` | `print(list(gen))`, ale pozor, tím ho vyčerpáš |
| `len(gen)`, `gen[0]` | `TypeError` | generátor nemá délku ani index |
| změna slovníku během `for k in d` | `RuntimeError: dictionary changed size during iteration` | iteruj přes kopii: `for k in list(d)` |
| `list()` nad nekonečným generátorem | program se zasekne, roste paměť | `islice`, `takewhile`, `break` |

## 7. `iter(funkce, zarážka)`

Málo známá forma `iter`: volá funkci bez argumentů pořád dokola, dokud
nevrátí zarážku (sentinel). Hodí se na čtení po kouscích:

```python
import io

f = io.StringIO("abcdefgh")              # chová se jako otevřený soubor
list(iter(lambda: f.read(3), ""))        # ['abc', 'def', 'gh']
```

`f.read(3)` vrací tři znaky, na konci souboru `""`. To je zarážka a
iterace skončí. Stejně se čtou binární soubory po blocích
(`f.read(8192)`, zarážka `b""`).

## 8. Vzory z praxe

### Velký soubor po řádcích

Otevřený soubor je sám iterátor přes řádky. Nečte celý soubor do paměti:

```python
def errors(path):
    with open(path) as f:          # with zavře soubor, viz 11-soubory
        for line in f:
            if "ERROR" in line:
                yield line.rstrip()
```

`f.readlines()` nebo `f.read().splitlines()` by naopak načetly všechno
najednou.

### Stránkované API jako jeden proud položek

Volající nemusí vědět nic o stránkách. Další stránka se stáhne, až když
dojdou položky z předchozí:

```python
def all_items():
    page = 1
    while page is not None:
        response = fetch_page(page)     # HTTP požadavek
        yield from response["items"]
        page = response["next"]


next(x for x in all_items() if x == "c")
#   GET ?page=1
#   GET ?page=2      ← třetí stránka se nikdy nestáhne
# 'c'
```

Stejně se v Djangu prochází obrovská tabulka:
`Book.objects.iterator(chunk_size=2000)` načítá řádky po dávkách místo
celého querysetu najednou.

### Pipeline: čtení → čištění → převod → agregace

Každý krok je malý generátor, celek se skládá vnořením (viz
[`THEORY.md`](../06-generatory-iteratory/THEORY.md#pipeline-z-generátorů)
a cvičení `04-pipeline`). Výhody: každý krok jde testovat zvlášť, paměť
je konstantní, a když konzument skončí dřív (`next`, `any`, `break`),
zbytek se nepočítá.

### Generátor jako „nekonečný zdroj“

Počítadla, ID, střídání hodnot (`cycle`), opakované pokusy. Generátor
drží stav, volající jen říká „další“:

```python
def ids(prefix):
    n = 1
    while True:
        yield f"{prefix}-{n:04d}"
        n += 1
```

## 9. Výkon: kdy generátor, kdy seznam

| | Seznam | Generátor |
|---|---|---|
| paměť | roste s počtem prvků | konstantní |
| rychlost pro malá data | o něco rychlejší | o něco pomalejší (režie volání) |
| opakované procházení | ano | ne |
| `len`, index, slicing | ano | ne |
| první výsledek | až po spočítání všeho | hned |
| předčasné ukončení | práce už je hotová | zbytek se nepočítá |

Orientačně (1000 prvků, 2000 opakování) vyšel `sum([x * 2 ...])`
0.069 s a `sum(x * 2 ...)` 0.075 s. U malých dat je seznam klidně
rychlejší, rozdíl je ale zanedbatelný. Generátor vyhrává, když je dat
hodně, když je nepotřebuješ všechna, nebo když jsou nekonečná.

Rozhodnutí v praxi: když výsledek **vracíš** z funkce a volající ho bude
používat víckrát, vrať `list`. Když ho rovnou **spotřebuješ** (`sum`,
`any`, `for`, `join`, `dict(...)`), stačí generátor.

## 10. Srovnání s JS

| Python | JS |
|---|---|
| `iter(x)` | `x[Symbol.iterator]()` |
| `next(it)` | `it.next()` → `{ value, done }` |
| `StopIteration` | `done: true` |
| `def f(): ... yield` | `function* f() { ... yield }` |
| `yield from other` | `yield* other` |
| `(x * 2 for x in xs)` | `xs.values().map(x => x * 2)` (iterator helpers) |
| `list(gen)` | `[...gen]` / `Array.from(gen)` |
| `for x in gen:` | `for (const x of gen)` |
| `itertools` | v jazyce chybí, knihovny typu `iter-tools` |
