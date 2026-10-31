# `itertools` — přehled s příklady

Modul standardní knihovny s hotovými nástroji pro iterátory. Výtah
z [oficiální dokumentace](https://docs.python.org/3/library/itertools.html)
a článku [Real Python — Python's itertools](https://realpython.com/python-itertools/),
seřazený podle toho, jak často se v praxi používá. Úvod do iterátorů
a generátorů je v
[`06-generatory-iteratory/THEORY.md`](../06-generatory-iteratory/THEORY.md)
a do hloubky v [`GENERATORS_AND_ITERATORS.md`](GENERATORS_AND_ITERATORS.md).

```python
import itertools as it
```

Všechny funkce vrací **iterátor** (líný, jednorázový). Ve výpisech níže
je kolem nich `list(...)`, ať je vidět obsah. Ověřeno na Pythonu 3.14.

## Nejčastější

| Funkce | Co dělá | Příklad → výsledek |
|---|---|---|
| `islice(it, stop)` / `islice(it, start, stop, step)` | slicing pro cokoliv iterovatelného, i nekonečné | `islice("abcdefg", 2, 6, 2)` → `['c', 'e']` |
| `chain(a, b, ...)` | spojí iterables za sebe | `chain([1, 2], "ab")` → `[1, 2, 'a', 'b']` |
| `chain.from_iterable(xs)` | totéž, když máš iterables v seznamu (zploštění o jednu úroveň) | `chain.from_iterable([[1, 2], [3], []])` → `[1, 2, 3]` |
| `pairwise(it)` | sousední dvojice | `pairwise("abcd")` → `[('a', 'b'), ('b', 'c'), ('c', 'd')]` |
| `batched(it, n)` | dávky po `n` jako tuple, poslední kratší (3.12+) | `batched("abcdefg", 3)` → `[('a', 'b', 'c'), ('d', 'e', 'f'), ('g',)]` |
| `groupby(it, key)` | seskupí **sousední** prvky se stejným klíčem | viz níže, má past |
| `accumulate(it, func)` | průběžné výsledky (default součet) | `accumulate([1, 2, 3, 4])` → `[1, 3, 6, 10]` |
| `zip_longest(a, b, fillvalue=)` | `zip`, který doplní kratší vstup | `zip_longest([1, 2, 3], "ab", fillvalue="-")` → `[(1, 'a'), (2, 'b'), (3, '-')]` |
| `product(a, b)` | všechny kombinace (vnořené cykly) | `product("ab", [1, 2])` → `[('a', 1), ('a', 2), ('b', 1), ('b', 2)]` |

## Nekonečné

Vždycky je kombinuj s něčím, co je zastaví (`islice`, `takewhile`,
`zip` s konečnou sekvencí, `break`).

| Funkce | Co dělá | Příklad → výsledek |
|---|---|---|
| `count(start=0, step=1)` | počítadlo | `islice(count(0, 0.5), 3)` → `[0, 0.5, 1.0]` |
| `cycle(it)` | opakuje dokola | `islice(cycle("ab"), 5)` → `['a', 'b', 'a', 'b', 'a']` |
| `repeat(x, times=None)` | opakuje jednu hodnotu (bez `times` donekonečna) | `repeat("x", 3)` → `['x', 'x', 'x']` |

Typické použití `count`: `zip(count(1), items)` je totéž co
`enumerate(items, 1)`. `cycle` se hodí na střídání (barvy řádků
tabulky, round-robin rozdělování úkolů).

## Filtrování

| Funkce | Co dělá | Příklad → výsledek |
|---|---|---|
| `takewhile(pred, it)` | bere, dokud platí podmínka, pak **skončí** | `takewhile(lambda x: x < 3, [1, 2, 3, 1])` → `[1, 2]` |
| `dropwhile(pred, it)` | zahazuje, dokud platí podmínka, pak vydá **všechno** zbylé | `dropwhile(lambda x: x < 3, [1, 2, 3, 1])` → `[3, 1]` |
| `filterfalse(pred, it)` | opak `filter` | `filterfalse(lambda x: x % 2, range(6))` → `[0, 2, 4]` |
| `compress(data, selectors)` | nechá prvky, kde je selektor truthy | `compress("abcd", [1, 0, 1, 0])` → `['a', 'c']` |

Rozdíl `takewhile` vs. `filter`: `filter` projde všechno, `takewhile`
skončí u prvního nesplnění. Poslední `1` v příkladu proto `takewhile`
už nevidí. Proto `takewhile` funguje i na nekonečném generátoru,
`filter` by běžel navždy.

## `groupby` a jeho past

`groupby` seskupuje jen **sousední** stejné prvky, nic netřídí:

```python
words = ["auto", "kolo", "auto", "dum", "kolo", "auto"]

[(k, len(list(g))) for k, g in it.groupby(words)]
# [('auto', 1), ('kolo', 1), ('auto', 1), ('dum', 1), ('kolo', 1), ('auto', 1)]

[(k, len(list(g))) for k, g in it.groupby(sorted(words))]
# [('auto', 3), ('dum', 1), ('kolo', 2)]
```

Seskupení podle klíče: **stejný `key` pro `sorted` i `groupby`**:

```python
people = [("Anna", "Praha"), ("Petr", "Brno"), ("Eva", "Praha")]

def city(person):
    return person[1]

for town, group in it.groupby(sorted(people, key=city), key=city):
    print(town, [name for name, _ in group])
# Brno ['Petr']
# Praha ['Anna', 'Eva']
```

Druhá past: `group` je iterátor nad stejným zdrojem. Než se posuneš na
další skupinu, musíš ho spotřebovat (nebo převést na `list`), jinak
zmizí.

Kdy `groupby` nepotřebuješ: na „seskup do dictu“ je jednodušší cyklus
s `dict.setdefault(key, []).append(item)`, který nic třídit nemusí.
`groupby` se hodí na data, která už seřazená jsou (výsledek SQL
s `ORDER BY`, logy podle času) a na „po sobě jdoucí úseky“:

```python
[k for k, _ in it.groupby("aaabccaa")]   # ['a', 'b', 'c', 'a']
```

## `accumulate` podrobněji

```python
it.accumulate([1, 2, 3, 4])               # [1, 3, 6, 10]   — průběžný součet
it.accumulate([3, 1, 4, 1, 5], max)       # [3, 3, 4, 4, 5] — průběžné maximum
it.accumulate([1, 2, 3], initial=100)     # [100, 101, 103, 106]
```

Je to obdoba JS `reduce`, která vrací všechny mezivýsledky, ne jen
poslední. Jen konečný výsledek dá `functools.reduce`:

```python
import functools

functools.reduce(lambda acc, x: acc + x, [1, 2, 3], 10)   # 16
```

V Pythonu se `reduce` používá málo: na součet je `sum`, na maximum
`max`, na spojení stringů `"".join`.

## Kombinatorika

| Funkce | Co vrací | Příklad → výsledek |
|---|---|---|
| `product(a, b)` / `product(a, repeat=n)` | kartézský součin | `len(list(product(range(3), repeat=2)))` → `9` |
| `permutations(it, r)` | uspořádané výběry, **záleží** na pořadí | `permutations("abc", 2)` → `[('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]` |
| `combinations(it, r)` | výběry bez opakování, **nezáleží** na pořadí | `combinations("abcd", 2)` → `[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]` |
| `combinations_with_replacement(it, r)` | jako `combinations`, prvek se smí opakovat | `combinations_with_replacement("ab", 2)` → `[('a', 'a'), ('a', 'b'), ('b', 'b')]` |

`product` nahrazuje vnořené cykly:

```python
for size, color in it.product(["S", "M"], ["red", "blue"]):
    ...   # totéž co dva vnořené for
```

Pozor na velikost: počet výsledků roste velmi rychle (`permutations`
z 10 prvků je 3 628 800 n-tic).

## Ostatní

| Funkce | Co dělá | Příklad → výsledek |
|---|---|---|
| `starmap(func, it)` | `map`, který rozbalí každou n-tici do argumentů | `starmap(pow, [(2, 3), (10, 2)])` → `[8, 100]` |
| `tee(it, n=2)` | rozdělí jeden iterátor na `n` nezávislých | `a, b = tee(iter([1, 2, 3]))` → `list(a)`, `list(b)` oba `[1, 2, 3]` |

`tee` si interně ukládá hodnoty, které jedna kopie už přečetla a druhá
ještě ne. Když jednu kopii přečteš celou dřív, než začneš druhou, je
`list(...)` jednodušší a stejně paměťově náročný.

## Recepty z dokumentace

Na konci [oficiální stránky](https://docs.python.org/3/library/itertools.html#itertools-recipes)
jsou hotové krátké funkce postavené z `itertools` (`take`, `nth`,
`flatten`, `sliding_window`, `unique_everseen` …). Hodí se jako inspirace
a jako ukázka idiomatického stylu. Nejdřív si je ale zkus napsat sám,
několik z nich je ve cvičeních `06-generatory-iteratory`.

Balíček [`more-itertools`](https://more-itertools.readthedocs.io/)
(instalace přes uv, viz `12-moduly-balicky`) obsahuje recepty
a desítky dalších nástrojů hotové.
