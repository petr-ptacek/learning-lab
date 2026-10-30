# Typové anotace (type hints)

Jak otypovat parametry, návratové hodnoty a proměnné. Prakticky,
pro Python 3.12+ (ověřeno na 3.14). Pro TS vývojáře: syntaxe je jiná,
myšlenka stejná. Jen s jedním zásadním rozdílem, viz hned první sekci.

Oficiální zdroje: [`typing`](https://docs.python.org/3/library/typing.html),
[`collections.abc`](https://docs.python.org/3/library/collections.abc.html),
[Type hints cheat sheet (mypy)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
— ten poslední je nejlepší rychlá reference.

## Python typy za běhu nekontroluje

```python
def greet(name: str, times: int = 1) -> str:
    return name * times


greet(5)   # 5 — proběhne bez chyby, i když 5 není str
```

Anotace jsou jen metadata (`greet.__annotations__`). Kontrolují je
**editor** (PyCharm podtrhne chybu) a **type checker** (`mypy`,
`pyright`), který spustíš zvlášť:

```bash
uvx mypy main.py
# main.py:4: error: Argument 1 to "greet" has incompatible type "int"; expected "str"  [arg-type]
```

TS obdoba: jako kdyby se `.ts` spouštělo přímo bez `tsc`. Typy pomáhají
při psaní a čtení, za běhu nic neblokují.

## Základy

```python
def greet(name: str, times: int = 1) -> str: ...   # parametr: typ = default
def log(message: str) -> None: ...                 # nic nevrací


scores: dict[str, int] = {"Anna": 87}
point: tuple[float, float] = (1.0, 2.0)            # přesně dvě položky
values: tuple[int, ...] = (1, 2, 3)                # libovolně dlouhý tuple
tags: set[str] = set()
```

| Python | TS |
|---|---|
| `int`, `float`, `str`, `bool` | `number`, `string`, `boolean` |
| `list[int]` | `number[]` |
| `dict[str, int]` | `Record<string, number>` |
| `tuple[int, str]` | `[number, string]` |
| `str \| None` | `string \| null` |
| `None` (návratový typ) | `void` |
| `Any` | `any` |

Proměnné se většinou neanotují, typ se odvodí z hodnoty (jako v TS).
Anotace u proměnné má smysl u prázdných kolekcí (`tags: set[str] = set()`).

### Může chybět: `| None`

```python
def find(names: list[str], query: str) -> str | None:
    return next((n for n in names if query in n), None)
```

Starší zápis `Optional[str]` z `typing` znamená totéž. V novém kódu
piš `str | None`.

## Parametry obecně, návratové hodnoty přesně

Pravidlo z praxe: **parametr typuj tím nejobecnějším, co funkce
opravdu potřebuje**, aby šla volat s co nejvíc typy. **Návratovou
hodnotu typuj přesně**, aby volající věděl, co dostane.

Obecné typy jsou v `collections.abc`:

```python
from collections.abc import Iterable


def total(numbers: Iterable[int]) -> int:
    return sum(numbers)


total([1, 2])               # list
total(range(3))             # range
total(n for n in [1, 2])    # generátor
```

S `numbers: list[int]` by editor hlásil chybu u `range` i u generátoru,
přestože funkce s nimi funguje.

| Potřebuješ od parametru | Typ | Projde |
|---|---|---|
| jen projít (`for`, `sum`, `iter`) | `Iterable[int]` | list, tuple, set, range, generátor, dict (klíče) |
| volat `next()` přímo | `Iterator[int]` | generátor, `map`, výsledek `iter()` |
| `len`, index, víc průchodů | `Sequence[int]` | list, tuple, range, str |
| jen číst dict | `Mapping[str, int]` | dict a podobné |
| měnit (`append`, `[k] = v`) | `list[int]`, `dict[str, int]` | jen ten typ |
| funkci | `Callable[[int], bool]` | funkce, lambda, vestavěná funkce |

`from typing import Iterable, List, Dict` taky funguje, ale je to
zastaralé. Od Pythonu 3.9 piš `list[int]` a `Iterable` ze
`collections.abc`.

## Funkce jako parametr: `Callable`

```python
from collections.abc import Callable


def apply(func: Callable[[int], int], x: int) -> int:
    return func(x)


apply(abs, -3)               # 3
apply(lambda n: n * 2, 5)    # 10
```

`Callable[[typy argumentů], návratový typ]`. TS:
`(func: (n: number) => number, x: number) => number`.

## Generika: typová proměnná

Když funkce funguje pro libovolný typ prvků a výsledek má **stejný typ
jako vstup**, použij typovou proměnnou. Od Pythonu 3.12 v hranatých
závorkách za názvem funkce:

```python
from collections.abc import Iterable, Sequence


def first[T](iterable: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(iterable), default)


def middle[T](items: Sequence[T]) -> T:
    return items[len(items) // 2]


first(["a", "b"])    # editor ví, že výsledek je str | None
middle([1, 2, 3])    # editor ví, že výsledek je int
```

TS: `function first<T>(iterable: Iterable<T>, def?: T): T | undefined`.

Ve starším kódu uvidíš totéž přes `TypeVar`:

```python
from typing import TypeVar

T = TypeVar("T")

def first(iterable: Iterable[T]) -> T | None: ...
```

## Generátory

```python
from collections.abc import Generator, Iterator


def countdown(n: int) -> Iterator[int]:
    while n > 0:
        yield n
        n -= 1
```

Generátorová funkce **vrací iterátor**, proto `Iterator[typ vydávaných
hodnot]`. Přesnější `Generator[vydává, přijímá přes send, vrací přes
return]` potřebuješ jen se `send` nebo `return hodnota`:

```python
def averager() -> Generator[float, float, str]:
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average
        if value < 0:
            return "konec"
        total += value
        count += 1
        average = total / count
```

Od Pythonu 3.13 mají poslední dva parametry výchozí hodnotu `None`,
takže `Generator[int]` znamená totéž co `Iterator[int]` s přesnějším
názvem.

## Vlastní názvy typů: `type`

```python
type Point = tuple[float, float]


def distance(a: Point, b: Point) -> float:
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
```

TS: `type Point = [number, number]`. `type` je klíčové slovo od
Pythonu 3.12.

## Slovník s pevnými klíči: `TypedDict`

Seznam dictů (sklad, JSON z API) se dá otypovat jako TS `interface`:

```python
from typing import TypedDict


class Product(TypedDict):
    name: str
    price: float
    qty: int


def value(p: Product) -> float:
    return p["price"] * p["qty"]


value({"name": "Mléko", "price": 24.9, "qty": 10})   # 249.0
```

Za běhu je to obyčejný `dict`. Editor ale hlídá názvy klíčů a typy
hodnot. Pro data s chováním (metody) jsou lepší třídy a `dataclass`
(`08-oop-zaklady`).

## `Any` a kdy ho nepoužít

`Any` vypne kontrolu: projde všechno a všechno je povolené (jako TS
`any`). Když nevíš typ, ale chceš kontrolu zachovat, použij `object`
(projde cokoliv, ale nic s tím nejde dělat bez ověření typu, jako TS
`unknown`).

## Časté chyby

| Příznak | Příčina |
|---|---|
| `TypeError: 'type' object is not subscriptable` | starý Python (< 3.9) s `list[int]`; tady nenastane |
| editor hlásí chybu u `range` / generátoru | parametr je `list[...]`, ale stačí `Iterable[...]` |
| `def f(x: list[int] = [])` | nejde o typy: výchozí `[]` se vytvoří jednou a sdílí mezi voláními. Piš `x: list[int] \| None = None` a uvnitř `if x is None: x = []` |
| `int` místo `float` v parametru | `float` přijme i `int` (výjimka v pravidlech), naopak ne |
| proměnná `total = 0`, pak `+= 1.5` hlásí mypy | typ se odvodil jako `int`, začni `0.0` nebo anotuj |

## Kde se to v repu používá

- Django modely a views: anotace se v Django kódu používají čím dál víc,
  DRF a `django-stubs` je umí využít.
- Cvičení: anotace nejsou povinné. Když je píšeš, drž se pravidla
  „parametry obecně, návratové hodnoty přesně“.
