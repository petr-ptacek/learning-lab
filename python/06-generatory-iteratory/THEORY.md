# 06 — Generátory a iterátory

## Cíl

Pochopit, co se děje, když píšeš `for x in ...`, a naučit se psát vlastní
**líné** sekvence: hodnoty, které se počítají až ve chvíli, kdy je někdo
chce. V [`05-vestavene-funkce`](../05-vestavene-funkce/THEORY.md) jsi
viděl, že `map` nebo `zip` jde projít jen jednou. Tady zjistíš proč
a napíšeš si stejné chování sám přes `yield`.

Na čem to stavíš: funkce a rekurze z [`03-funkce`](../03-funkce/THEORY.md),
kolekce z [`04-datove-struktury`](../04-datove-struktury/THEORY.md)
a generátorové výrazy uvnitř `sum` / `any` / `max` z `05`.

K čemu to bude: zpracování velkých dat po kouscích (soubory v `11-soubory`,
řádky z databáze, stránkované API), nekonečné sekvence a „pipeline“ ve
stylu `data → filtr → převod → výsledek` bez mezilistů. V JS je to totéž
co `function*` + `yield` a protokol `Symbol.iterator`.

Do hloubky (víc, než se sem vešlo, výtah z článků v `RESOURCES.md`):

- [`../docs/GENERATORS_AND_ITERATORS.md`](../docs/GENERATORS_AND_ITERATORS.md):
  iterační protokol, opakovatelné vs. jednorázové, život generátoru,
  pasti, vzory z praxe, výkon, srovnání s JS
- [`../docs/ITERTOOLS.md`](../docs/ITERTOOLS.md): všechny důležité
  funkce `itertools` s příklady, past u `groupby`

## Iterable vs. iterátor

| | Co to je | Příklady |
|---|---|---|
| **iterable** | něco, co se dá procházet, umí vyrobit iterátor | `list`, `str`, `dict`, `set`, `range`, soubor |
| **iterátor** | „kurzor“, který si pamatuje, kde je, a vydává další hodnotu | výsledek `iter(...)`, `map`, `filter`, `zip`, `enumerate`, generátor |

```python
numbers = [10, 20, 30]      # iterable
it = iter(numbers)          # iterátor nad ním

next(it)                    # 10
next(it)                    # 20
next(it)                    # 30
next(it)                    # StopIteration — konec, výjimka
next(it, "konec")           # 'konec' — s defaultem výjimka nenastane
```

- `iter(x)` vyrobí z iterable nový iterátor. Ze seznamu můžeš udělat
  kolik iterátorů chceš, každý začíná od začátku.
- `next(it)` vrátí další hodnotu. Za koncem vyhodí `StopIteration`
  (výjimky v `10-vyjimky`), s druhým argumentem vrátí default.
- Iterátor jde jen **dopředu** a **jednou**. Vyčerpaný iterátor zůstane
  prázdný. Proto `list(m)` podruhé vrátí `[]`.

Iterátor je sám sobě iterable (`iter(it) is it`), proto ho jde dát do
`for` i do `list()`.

JS obdoba: `arr[Symbol.iterator]()` ≈ `iter(arr)`, `it.next()` ≈
`next(it)`. JS vrací `{value, done}`, Python místo `done: true` vyhodí
`StopIteration`.

## Co dělá `for` uvnitř

```python
for x in numbers:
    print(x)
```

je zhruba tohle:

```python
it = iter(numbers)
while True:
    x = next(it, KONEC)    # ve skutečnosti chytá StopIteration
    if x is KONEC:
        break
    print(x)
```

Každý `for`, `list()`, `sum()`, `sorted()`, `in`, rozbalení
`a, b = ...` … pracuje přes `iter` a `next`. Proto fungují na čemkoliv
iterovatelném, nejen na seznamu.

## Generátorová funkce — `yield`

Funkce, ve které je `yield`, se při zavolání **nespustí**. Vrátí
generátor (druh iterátoru). Tělo běží až při `next()`, vždycky jen do
dalšího `yield`, kde se zastaví a pamatuje si stav (lokální proměnné,
místo v kódu):

```python
def countdown(n):
    print("start")
    while n > 0:
        yield n
        n -= 1
    print("konec")


gen = countdown(2)   # nic se nevypíše — tělo zatím neběží
next(gen)            # vypíše "start", vrátí 2
next(gen)            # vrátí 1
next(gen)            # vypíše "konec", pak StopIteration
list(countdown(3))   # [3, 2, 1] (+ výpisy start / konec)
```

| `return` | `yield` |
|---|---|
| ukončí funkci, vrátí jednu hodnotu | pozastaví funkci, vydá jednu z mnoha hodnot |
| volání funkce spustí tělo | volání vrátí generátor, tělo běží až při `next` |
| výsledek máš celý najednou | hodnoty přicházejí postupně |

`return` v generátoru jde použít bez hodnoty: znamená „konec sekvence“.

JS obdoba:

```js
function* countdown(n) { while (n > 0) { yield n; n--; } }
[...countdown(3)]   // [3, 2, 1]
```

V Pythonu není hvězdička, generátor pozná podle toho, že je v těle `yield`.

## Generátorový výraz

Comprehension v kulatých závorkách. Nevytvoří seznam, ale generátor:

```python
squares_list = [x * x for x in range(5)]   # [0, 1, 4, 9, 16] — hned celý seznam
squares_gen = (x * x for x in range(5))    # <generator object ...> — nic nespočítáno

next(squares_gen)       # 0
list(squares_gen)       # [1, 4, 9, 16] — zbytek
```

Jako jediný argument funkce stačí jedny závorky: `sum(x * x for x in ...)`.

Krátký generátor piš jako výraz. Když potřebuješ víc řádků, stav nebo
podmínky, napiš generátorovou funkci.

## Líné vyhodnocení na příkladu

Jádro celého konceptu: seznam se počítá **hned a celý** (eager),
generátor **až na vyžádání a po jednom** (lazy). Nejlíp je to vidět na
výpisech. Dva kroky, „načti“ a „zdvojnásob“, jednou se seznamy, jednou
s generátory:

```python
def load(n):
    print(f"načítám {n}")
    return n


def double(n):
    print(f"  zdvojuji {n}")
    return n * 2
```

| Seznamy `[...]` | Generátory `(...)` |
|---|---|
| `loaded = [load(n) for n in [1, 2, 3]]`<br>`doubled = [double(n) for n in loaded]`<br>`print("hotovo, teď čtu")`<br>`for d in doubled: print("výsledek", d)` | `loaded = (load(n) for n in [1, 2, 3])`<br>`doubled = (double(n) for n in loaded)`<br>`print("hotovo, teď čtu")`<br>`for d in doubled: print("výsledek", d)` |

Výstup (ověřeno):

```
--- seznamy               --- generátory
načítám 1                 hotovo, teď čtu
načítám 2                 načítám 1
načítám 3                   zdvojuji 1
  zdvojuji 1              výsledek 2
  zdvojuji 2              načítám 2
  zdvojuji 3                zdvojuji 2
hotovo, teď čtu           výsledek 4
výsledek 2                načítám 3
výsledek 4                  zdvojuji 3
výsledek 6                výsledek 6
```

Co z toho plyne:

- **Seznamy** jdou po vrstvách: nejdřív se načte všechno, pak se
  všechno zdvojnásobí, a teprve pak se čte. V paměti jsou v jednu
  chvíli celé dva seznamy.
- **Generátory** při vytvoření neudělají nic (`hotovo, teď čtu` je
  první). Každá hodnota pak projde **celou cestou** (načíst → zdvojit →
  vypsat), než se začne další. V paměti je vždycky jen jedna.
- Když si vezmeš jen první výsledek, `next(doubled)`, generátory vypíšou
  jen `načítám 1` a `zdvojuji 1`. Zbytek se nikdy nespočítá. Seznamy by
  stejně udělaly všechnu práci dopředu.

Rozdíl v paměti pro milion čísel (`sys.getsizeof`, Python 3.14):

```python
import sys

sys.getsizeof([n * 2 for n in range(1_000_000)])   # 8448728 — cca 8 MB, jen seznam odkazů
sys.getsizeof(n * 2 for n in range(1_000_000))     # 208 — bajtů, ať je dat kolik chce
sum(n * 2 for n in range(1_000_000))               # 999999000000 — výsledek stejný
```

Cena za to: generátor jde projít jen jednou, nemá `len` ani index,
a každá hodnota se počítá znovu, když vytvoříš nový generátor.

V JS stejný rozdíl uvidíš mezi `arr.map(...).filter(...)` (každý krok
nové pole) a generátorem `function*` nebo iterátorovými helpery
(`Iterator.prototype.map`).

## Líné vyhodnocení a nekonečné sekvence

Generátor počítá jen to, co si někdo vyžádá. Proto může být nekonečný:

```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1
```

`list(naturals())` by běžel navždy. Z nekonečného generátoru se bere
jen část: `next(...)`, `zip` s konečnou sekvencí, `break` ve `for`, nebo
`itertools.islice` (viz níže).

Užitečný idiom „první, který splňuje podmínku“:

```python
next((n for n in naturals() if n * n > 50), None)   # 8
```

Prochází se jen do první shody, zbytek se nepočítá.

## Pipeline z generátorů

Generátory jde řetězit: každý bere iterable a vydává iterátor. Data
tečou jedno po druhém, celou cestou najednou, bez mezilistů:

```python
def read_numbers(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield int(line)


def only_even(numbers):
    return (n for n in numbers if n % 2 == 0)


raw = ["3", "4", "", "10", "7"]
sum(only_even(read_numbers(raw)))    # 14
```

Pro jeden řádek: `read_numbers` přečte a vydá `3`, `only_even` ho
zahodí, `read_numbers` přečte `4`, projde až do `sum`… V paměti je
v každé chvíli jen jedna hodnota. S milionem řádků ze souboru je to
rozdíl mezi pár kB a pár GB.

FE obdoba: RxJS `pipe(filter(...), map(...))` nebo stream. Na rozdíl
od `arr.filter().map()` v JS, kde každý krok vytvoří nové pole.

## `yield from`

Vydá postupně všechno z jiného iterable. Typicky při skládání generátorů
a v rekurzi:

```python
def chain(a, b):
    yield from a     # totéž co: for x in a: yield x
    yield from b


list(chain([1, 2], "ab"))   # [1, 2, 'a', 'b']
```

Rekurzivní generátor (strom, vnořené seznamy) volá sám sebe
a `yield from` předá výsledky „nahoru“. Pro rozlišení, jestli je prvek
seznam, se používá `isinstance(x, list)`: vrací `True`, když je `x`
seznam (nebo jeho podtřída). Je to přesnější než `type(x) == list`.

Rozdíl `yield` vs. `yield from`, jak hodnoty v rekurzi probublávají
nahoru a typické chyby rozebírá
[`docs/GENERATORS_AND_ITERATORS.md`](../docs/GENERATORS_AND_ITERATORS.md#4-yield-from-a-return-v-generátoru).

## `close`, `send`, `throw` — metody generátoru

Generátor (ne každý iterátor, `map` nebo `zip` je nemají) má navíc tři
metody. V aplikačním kódu je skoro nevoláš, ale je dobré vědět, co
dělají:

| Metoda | Co dělá | Jak důležité |
|---|---|---|
| `close()` | ukončí generátor: v místě, kde stojí na `yield`, vyvolá `GeneratorExit`, takže proběhne `finally` | pochopit |
| `send(value)` | jako `next()`, ale pošle hodnotu **dovnitř**: `x = yield ...` ji dostane | vědět, že existuje |
| `throw(exc)` | vyvolá výjimku uvnitř generátoru v místě `yield` | vědět, že existuje |

### `close` a úklid

Generátor, který něco otevře (soubor, spojení), musí uklidit i tehdy,
když ho nikdo nedočte. Úklid patří do `finally`:

```python
def read_rows(path):
    f = open(path)
    try:
        for line in f:
            yield line
    finally:
        print("zavírám")
        f.close()


rows = read_rows("data.csv")
next(rows)      # 'a\n'
rows.close()    # vypíše "zavírám", i když se soubor nedočetl

for row in read_rows("data.csv"):
    break       # po break Python generátor zahodí a zavolá close sám → "zavírám"
```

`try` / `finally` a `with` přijdou v `10-vyjimky` a `11-soubory`. Zatím
si pamatuj: kód za posledním `yield` se nemusí nikdy provést, `finally`
ano.

### `send` — jen pro představu

```python
def averager():
    total = count = 0
    average = None
    while True:
        value = yield average    # vydá průměr, pak čeká na hodnotu zvenku
        total += value
        count += 1
        average = total / count


a = averager()
next(a)        # None — „nastartování“, dojde k prvnímu yield
a.send(10)     # 10.0
a.send(20)     # 15.0
a.send(60)     # 30.0
```

Kde tyhle metody žijí, aniž je voláš sám:

- **`@contextlib.contextmanager`** udělá z generátoru s jedním `yield`
  kontextový manažer pro `with`. Uvnitř volá `next`, `throw` a `close`.
- **pytest fixtures s `yield`**: kód za `yield` je úklid po testu, stejný
  mechanismus.
- **`async` / `await`**: před Pythonem 3.5 se asynchronní kód psal přes
  generátory a `send`. Dnešní `async def` na stejném principu stojí
  uvnitř.

Když `send` nebo `throw` potkáš v kódu, je to starší knihovna nebo hodně
specifický kód, ne běžný vzor.

## `itertools` — hotové nástroje

Modul ze standardní knihovny (`import itertools`). Nejčastější:

| Funkce | Co dělá | Příklad |
|---|---|---|
| `islice(it, n)` / `islice(it, start, stop)` | slicing pro iterátory | `list(islice(naturals(), 3))` → `[1, 2, 3]` |
| `count(start, step)` | nekonečné počítadlo | `count(10, 5)` → 10, 15, 20, … |
| `takewhile(pred, it)` | bere, dokud platí podmínka | `takewhile(lambda x: x < 4, naturals())` → 1, 2, 3 |
| `chain(a, b, ...)` | spojí iterables za sebe | `chain([1], "ab")` → 1, 'a', 'b' |
| `pairwise(it)` | sousední dvojice | `pairwise([1, 2, 3])` → (1, 2), (2, 3) |
| `batched(it, n)` | dávky po `n` (tuple), od Pythonu 3.12 | `batched(range(5), 2)` → (0, 1), (2, 3), (4,) |

Cvičení je nejdřív píšou ručně, `itertools` přijde v bonusech.
Kompletní přehled s příklady: [`ITERTOOLS.md`](../docs/ITERTOOLS.md).

## Kdy co

| Chceš… | Použij |
|---|---|
| výsledek procházet víckrát, indexovat, znát `len` | `list` |
| projít jednou, hodně dat nebo nekonečno | generátor |
| jednoduchý převod / filtr | generátorový výraz `(... for ...)` |
| víc kroků, stav mezi hodnotami | generátorová funkce s `yield` |
| první prvek splňující podmínku | `next((x for x in ... if ...), default)` |
| prvních `n` z generátoru | `itertools.islice` |

## Časté chyby

| Příznak | Příčina |
|---|---|
| podruhé prázdný výsledek | iterátor / generátor už je vyčerpaný, ulož si `list(...)` |
| funkce „nic nedělá“, výpisy v ní se neobjeví | je v ní `yield`, takže vrací generátor a tělo neběží, dokud ho někdo neprochází |
| `<generator object ...>` ve výpisu | vypisuješ generátor, ne hodnoty, obal ho `list(...)` |
| program se zasekne | `list()` / `sum()` / `for` bez `break` nad nekonečným generátorem |
| `TypeError: object of type 'generator' has no len()` | generátor nezná délku ani index, `len` / `[0]` jen na seznamu |
| `StopIteration` | `next()` za koncem bez defaultu |

Odkazy viz [`RESOURCES.md`](RESOURCES.md).
