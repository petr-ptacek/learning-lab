# Dataclasses

Výtah z Real Python *Data Classes in Python* a z oficiální dokumentace
modulu [`dataclasses`](https://docs.python.org/3/library/dataclasses.html).
Odkazy jsou v [`07-oop-zaklady/RESOURCES.md`](../07-oop-zaklady/RESOURCES.md),
přehled v [`THEORY.md`](../07-oop-zaklady/THEORY.md#dataclass-třída-na-data-bez-psaní-__init__).

Souvisí: co generované metody dělají, v
[`DUNDER_METHODS.md`](DUNDER_METHODS.md), typové anotace v
[`TYPE_HINTS.md`](TYPE_HINTS.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Co dekorátor vygeneruje](#1-co-dekorátor-vygeneruje)
2. [Výchozí hodnoty a `field(default_factory=...)`](#2-výchozí-hodnoty-a-fielddefault_factory)
3. [Další volby `field()`](#3-další-volby-field)
4. [`__post_init__`: úprava a validace](#4-__post_init__-úprava-a-validace)
5. [`frozen=True`: neměnné a hashovatelné](#5-frozentrue-neměnné-a-hashovatelné)
6. [`order=True`: řazení](#6-ordertrue-řazení)
7. [`asdict`, `replace`, `fields`](#7-asdict-replace-fields)
8. [`kw_only` a `slots`](#8-kw_only-a-slots)
9. [Dataclass, nebo něco jiného?](#9-dataclass-nebo-něco-jiného)

---

## 1. Co dekorátor vygeneruje

```python
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0

    def total_value(self):
        return round(self.price * self.quantity, 2)


milk = Product("Mléko", 24.9, 10)
milk                                  # Product(name='Mléko', price=24.9, quantity=10)
milk == Product("Mléko", 24.9, 10)    # True
milk.total_value()                    # 249.0
Product(name="Káva", price=189.0)     # Product(name='Káva', price=189.0, quantity=0)
```

Dekorátor projde **anotované atributy třídy** v pořadí, v jakém jsou
napsané, a vygeneruje:

- `__init__(self, name, price, quantity=0)` s přiřazením `self.name = name`…,
- `__repr__` ve tvaru `Product(name='Mléko', ...)`,
- `__eq__`, který porovná všechna pole jako tuple.

Bez dekorátoru by to bylo asi patnáct řádků opakovaného kódu. Metody
(`total_value`) a property se píšou normálně.

Anotace jsou povinné: atribut bez anotace (`vat = 0.21`) se stane
obyčejným atributem třídy, ne polem. Typ ale Python za běhu nekontroluje
(viz [`TYPE_HINTS.md`](TYPE_HINTS.md#python-typy-za-běhu-nekontroluje)),
`Product("x", "levné")` projde.

## 2. Výchozí hodnoty a `field(default_factory=...)`

Měnitelnou výchozí hodnotu dataclass **nedovolí**, protože by ji
sdílely všechny instance (stejná past jako atribut třídy `items = []`):

```python
@dataclass
class Bad:
    tags: list = []
# ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory
```

Správně: továrna, která se zavolá pro každou instanci zvlášť:

```python
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)


a = Product("Mléko", 24.9)
b = Product("Chléb", 39.0)
b.tags.append("pečivo")
a.tags, b.tags            # ([], ['pečivo'])
```

`default_factory` bere cokoliv volatelného bez argumentů: `list`,
`dict`, `set`, `lambda: {"cs": ""}`, `datetime.now`.

Pole s výchozí hodnotou musí být **za** poli bez ní. Platí to stejně
jako u parametrů funkce:

```python
@dataclass
class Bad2:
    a: int = 0
    b: int
# TypeError: non-default argument 'b' follows default argument 'a'
```

## 3. Další volby `field()`

| Parametr | Co dělá | Příklad |
|---|---|---|
| `default=` | výchozí hodnota (totéž co `= hodnota`) | `field(default=0)` |
| `default_factory=` | továrna na výchozí hodnotu | `field(default_factory=list)` |
| `repr=False` | pole se nevypíše v `repr` | hesla, tokeny, velká data |
| `compare=False` | pole se ignoruje v `==` (a v řazení) | čas vytvoření, cache |
| `init=False` | pole není parametr `__init__`, nastaví se jinak | dopočítané v `__post_init__` |
| `kw_only=True` | jen jako pojmenovaný argument | volitelná nastavení |

```python
@dataclass
class User:
    username: str
    password: str = field(repr=False)
    is_active: bool = True


User("anna", "tajne123")      # User(username='anna', is_active=True)
```

## 4. `__post_init__`: úprava a validace

Vygenerovaný `__init__` jen ukládá. Když potřebuješ hodnoty upravit,
zkontrolovat nebo dopočítat, napiš `__post_init__`. Zavolá se hned po
něm:

```python
@dataclass
class Email:
    address: str

    def __post_init__(self):
        self.address = self.address.strip().lower()
        if "@" not in self.address:
            raise ValueError(f"Neplatný e-mail: {self.address}")

    @property
    def domain(self):
        return self.address.split("@")[1]


e = Email("  Anna.Novakova@Example.CZ ")
e                             # Email(address='anna.novakova@example.cz')
e.domain                      # 'example.cz'
Email("A@B.cz") == Email("a@b.CZ ")     # True — porovnává už upravené hodnoty
Email("bez-zavinace")         # ValueError: Neplatný e-mail: bez-zavinace
```

Dopočítané pole s `init=False`:

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = self.width * self.height


Rectangle(3, 4)               # Rectangle(width=3, height=4, area=12)
```

Pozor: `area` se spočítá jen jednou. Po změně `width` zůstane stará.
Pro hodnotu, která má být vždy aktuální, je lepší `@property`.

## 5. `frozen=True`: neměnné a hashovatelné

```python
from dataclasses import FrozenInstanceError


@dataclass(frozen=True)
class Point:
    x: float
    y: float


p = Point(0, 0)
p.x = 5                       # FrozenInstanceError: cannot assign to field 'x'
len({Point(0, 0), Point(1, 2), Point(0, 0)})   # 2
{Point(0, 0): "start"}[Point(0, 0)]           # 'start'
```

Obyčejná dataclass má `__eq__`, a proto **nemá** `__hash__` (pravidlo
z [`DUNDER_METHODS.md`](DUNDER_METHODS.md#3-__eq__-a-__hash__)):

```python
{Product("x", 1)}             # TypeError: cannot use 'Product' as a set element (unhashable type: 'Product')
```

S `frozen=True` dataclass vygeneruje i `__hash__`. Je to bezpečné,
protože se objekt nemůže změnit. Hodí se pro hodnoty typu bod, verze,
peníze nebo souřadnice, tedy věci, které mají smysl jako klíč dictu
nebo prvek setu.

„Změna“ zmrazeného objektu = nový objekt přes `replace` (sekce 7).

## 6. `order=True`: řazení

Vygeneruje `<`, `<=`, `>`, `>=`. Porovnává pole **v pořadí
definice**, jako tuple:

```python
@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    @classmethod
    def parse(cls, text):
        return cls(*(int(part) for part in text.split(".")))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


Version.parse("1.10.0") > Version.parse("1.9.3")   # True
"1.10.0" > "1.9.3"                                  # False — stringy se řadí po znacích
versions = [Version.parse(t) for t in ["1.10.0", "1.2.3", "0.9"]]
[str(v) for v in sorted(versions)]                  # ['0.9.0', '1.2.3', '1.10.0']
```

Vlastní `__str__` dataclass nepřepíše. Generuje jen `__repr__`, takže
`print(v)` použije tvůj `__str__`.

Když chceš řadit podle jiného pole, než je první, buď změň pořadí
polí, nebo nepoužívej `order=True` a řaď přes `sorted(key=...)`.

## 7. `asdict`, `replace`, `fields`

```python
import json
from dataclasses import asdict, fields, replace


coffee = Product("Káva", 189.0, ["bio"])
asdict(coffee)                # {'name': 'Káva', 'price': 189.0, 'tags': ['bio']}
json.dumps(asdict(coffee), ensure_ascii=False)
# '{"name": "Káva", "price": 189.0, "tags": ["bio"]}'

cheaper = replace(coffee, price=169.0)   # nová instance, ostatní pole převzatá
coffee.price, cheaper.price   # (189.0, 169.0)

[f.name for f in fields(Product)]        # ['name', 'price', 'tags']
```

- `asdict` převede rekurzivně i vnořené dataclasses a seznamy. Je to
  nejkratší cesta do JSON (viz [`JSON.md`](JSON.md)),
- `replace` je obdoba JS `{ ...obj, price: 169 }`,
- `fields` vrátí popis polí. Tohle je princip, na kterém stojí i
  Django: z popisu polí na třídě se generuje formulář, serializace,
  SQL.

## 8. `kw_only` a `slots`

```python
@dataclass(kw_only=True)
class Options:
    debug: bool = False
    retries: int = 3


Options(retries=5)            # Options(debug=False, retries=5)
Options(True)                 # TypeError: Options.__init__() takes 1 positional argument but 2 were given
```

`kw_only=True` vynutí pojmenované argumenty. Hodí se, když je polí
hodně a `Options(True, 5, False)` by nebylo čitelné.

`slots=True` vytvoří třídu se `__slots__`: instance nemají `__dict__`,
zabírají méně paměti a nejde jim přidat nový atribut. Má smysl u
milionů malých objektů, jinak to neřeš.

## 9. Dataclass, nebo něco jiného?

| | Kdy |
|---|---|
| `@dataclass` | objekt hlavně nese data a má pár metod. Výchozí volba |
| `@dataclass(frozen=True)` | hodnotový objekt: neměnný, do setu, jako klíč |
| obyčejná třída | složitější logika v `__init__`, stav, který se mění řízeně, nebo když nechceš generované `__eq__` |
| `TypedDict` | data **zůstávají dict** (JSON z API) a chceš jen typovou kontrolu, viz [`TYPE_HINTS.md`](TYPE_HINTS.md#slovník-s-pevnými-klíči-typeddict) |
| `NamedTuple` | neměnný záznam, který se má chovat i jako tuple (rozbalování, index) |
| Django model | data v databázi. Pole se taky popisují na třídě, ale `models.CharField(...)` místo anotace |
| Pydantic / DRF serializer | data **zvenku**, která se musí validovat a převádět (typy se za běhu kontrolují) |

Pro TS vývojáře: dataclass je nejblíž `class` s parametrovými
vlastnostmi (`constructor(public name: string, public price: number)`)
plus vygenerovaný `toString` a strukturální `equals`.
