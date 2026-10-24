# 05 — Vestavěné funkce

## Cíl

Naučit se vestavěné funkce Pythonu, které pracují s kolekcemi — `min`,
`max`, `sum`, `sorted`, `enumerate`, `zip`, `map`, `filter`, `any`,
`all` — a hlavně parametr **`key`**, kterým jim řekneš, *podle čeho*
mají porovnávat. Staví na [`04-datove-struktury`](../04-datove-struktury/THEORY.md),
kde sis většinu z nich napsal ručně cyklem — teď uvidíš, jak se to samé
zapíše na jeden řádek. Lambdy z [`03-funkce`](../03-funkce/THEORY.md)
tu konečně dostanou smysl.

## Základ — `len`, `min`, `max`, `sum`, `abs`, `round`

```python
numbers = [3, -7, 5, 1]

len(numbers)          # 4
min(numbers)          # -7
max(numbers)          # 5
sum(numbers)          # 2
sum(numbers, 10)      # 12 — druhý argument je počáteční hodnota
abs(-7)               # 7
round(3.14159, 2)     # 3.14
round(2.5)            # 2 — banker's rounding, .5 k sudému
```

`min`/`max` jdou volat i s víc argumenty: `max(3, 8, 1)` → `8`.

Prázdná kolekce: `min([])` / `max([])` vyhodí `ValueError` — pomůže
`default`:

```python
max([], default=None)   # None
sum([])                 # 0 — sum prázdný seznam zvládne
```

## Parametr `key`

`min`, `max` a `sorted` umí porovnávat **podle výsledku funkce**, ne
podle samotné hodnoty. `key` dostane funkci (často lambdu), která se
zavolá na každý prvek:

```python
words = ["kocka", "Pes", "slon"]
max(words, key=len)                  # 'kocka' — nejdelší slovo
min([5, -2, 3], key=abs)             # -2 — nejblíž nule

products = [{"name": "Mléko", "price": 24.9}, {"name": "Káva", "price": 149.0}]
max(products, key=lambda p: p["price"])["name"]   # 'Káva'
```

Vrací se vždy **původní prvek**, ne výsledek `key`. Při shodě vrací
`min`/`max` první nalezený.

## Řazení — `sorted` vs. `.sort()`

```python
nums = [3, 1, 2]
sorted(nums)            # [1, 2, 3] — NOVÝ seznam, původní beze změny
sorted(nums, reverse=True)
nums.sort()             # seřadí NA MÍSTĚ, vrací None
```

`sorted` funguje na cokoliv, co jde procházet (tuple, set, dict, string)
a vždy vrací list. `.sort()` je jen metoda listu.

```python
sorted(["kocka", "Pes", "auto"])                 # ['Pes', 'auto', 'kocka'] — velká písmena dřív!
sorted(["kocka", "Pes", "auto"], key=str.lower)  # ['auto', 'kocka', 'Pes']
```

**Řazení podle víc kritérií** — `key` vrátí tuple, tuple se porovnávají
po složkách zleva:

```python
# podle délky, při shodě abecedně
sorted(words, key=lambda w: (len(w), w.lower()))

# body sestupně, při shodě jméno vzestupně — mínus u čísla otočí směr
sorted(results, key=lambda r: (-r[1], r[0]))
```

Řazení je **stabilní** — prvky se shodným klíčem zůstanou v původním
pořadí.

`reversed(nums)` vrátí prvky odzadu (jako iterátor, viz níže).

## `enumerate` — index i hodnota

Náhrada za `for i in range(len(items))`:

```python
for i, item in enumerate(["mléko", "chleba"]):
    print(i, item)          # 0 mléko, 1 chleba

for i, item in enumerate(["mléko", "chleba"], start=1):
    print(f"{i}. {item}")   # 1. mléko, 2. chleba
```

Každý prvek je tuple `(index, hodnota)` — proto jde rovnou rozbalit.

## `zip` — souběžné procházení

```python
names = ["Anna", "Petr"]
scores = [90, 75]

for name, score in zip(names, scores):
    print(name, score)

dict(zip(names, scores))       # {'Anna': 90, 'Petr': 75}
```

Skončí u **nejkratší** kolekce — přebytečné prvky tiše zahodí.
`zip(a, b, strict=True)` místo toho vyhodí `ValueError`.

Užitečné triky:

```python
nums = [1, 4, 9]
list(zip(nums, nums[1:]))      # [(1, 4), (4, 9)] — sousední dvojice
list(zip(*[[1, 2], [3, 4]]))   # [(1, 3), (2, 4)] — transpozice matice
```

## `map` a `filter`

```python
list(map(int, ["1", "2", "3"]))             # [1, 2, 3] — funkce na každý prvek
list(map(lambda x: x * 2, [1, 2, 3]))       # [2, 4, 6]
list(filter(lambda x: x > 0, [3, -1, 5]))   # [3, 5] — jen prvky, pro které je True
list(filter(None, ["", "a", 0, 1]))         # ['a', 1] — None = podle pravdivosti
```

Totéž jde napsat comprehensionem — v Pythonu se comprehension používá
častěji, `map` se hodí hlavně s hotovou funkcí (`map(int, ...)`):

```python
[x * 2 for x in nums]        # místo map(lambda x: x * 2, nums)
[x for x in nums if x > 0]   # místo filter(lambda x: x > 0, nums)
```

## `any` a `all`

```python
any([False, True, False])                # True — aspoň jeden pravdivý
all([True, True, False])                 # False — všechny pravdivé?
any(x < 0 for x in [3, -1, 5])           # True — je tam záporné?
all(c.isdigit() for c in "12345")        # True — samé číslice?
```

Prázdná kolekce: `any([])` → `False`, `all([])` → `True` („všechny
z nuly prvků splňují podmínku“).

## Iterátory — `map`, `filter`, `zip`, `enumerate`, `reversed`

Tyhle funkce nevrací list, ale **iterátor** — hodnoty počítá až při
procházení a projít se dá **jen jednou**:

```python
m = map(int, ["1", "2"])
list(m)   # [1, 2]
list(m)   # [] — už vyčerpaný
```

Když potřebuješ výsledek víckrát nebo ho vypsat, obal ho `list(...)`.
Podrobně se iterátorům věnuje [`06-generatory-iteratory`](../ROADMAP.md).

## Generátorový výraz uvnitř funkce

Comprehension bez hranatých závorek přímo jako argument — nevytváří
mezilist:

```python
sum(x ** 2 for x in range(5))               # 30
sum(p["price"] * p["qty"] for p in products)
any(word.startswith("a") for word in words)
```

Podrobněji opět v `06-generatory-iteratory`.

## Kdy co

| Chceš…                                   | Použij                                  |
|------------------------------------------|-----------------------------------------|
| nejmenší / největší (i podle něčeho)     | `min` / `max` + `key`, `default`        |
| součet, počet splňujících podmínku       | `sum(...)`, `sum(1 for x in ... if ...)` |
| seřazenou kopii                          | `sorted` + `key`, `reverse`             |
| index při procházení                     | `enumerate`                             |
| projít dvě kolekce zároveň / sousedy     | `zip`                                   |
| převést / vyfiltrovat                    | comprehension (nebo `map` / `filter`)   |
| „platí pro některý / pro všechny?“       | `any` / `all`                           |

Kompletní seznam viz [`RESOURCES.md`](RESOURCES.md).
