# Abstraktní základní třídy a `collections.abc`

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(hlavně dokumentace modulů `abc` a `collections.abc` a Real Python
*Python's Abstract Base Classes* / *Custom Python Lists*). Přehled je v
[`THEORY.md`](../08-oop-dedicnost/THEORY.md). Tady je, jak donutit
podtřídu, aby něco implementovala, jak napsat „kostru“ algoritmu, do
které podtřídy jen doplní kousky, a jak dostat desítku metod zadarmo
z `collections.abc`.

Navazuje na dědičnost a `super()` v
[`INHERITANCE_AND_SUPER.md`](INHERITANCE_AND_SUPER.md) a na
kontejnerový protokol v [`DUNDER_METHODS.md`](DUNDER_METHODS.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [K čemu je abstraktní třída](#1-k-čemu-je-abstraktní-třída)
2. [`ABC` a `@abstractmethod`](#2-abc-a-abstractmethod)
3. [Abstraktní property a classmethod](#3-abstraktní-property-a-classmethod)
4. [Varianta bez `abc`: `raise NotImplementedError`](#4-varianta-bez-abc-raise-notimplementederror)
5. [Vzor template method](#5-vzor-template-method)
6. [`collections.abc`: metody zadarmo](#6-collectionsabc-metody-zadarmo)
7. [`isinstance` s `collections.abc`](#7-isinstance-s-collectionsabc)
8. [`typing.Protocol`: rozhraní bez dědičnosti](#8-typingprotocol-rozhraní-bez-dědičnosti)
9. [Časté chyby](#9-časté-chyby)

---

## 1. K čemu je abstraktní třída

Abstraktní třída je **společný základ**, který sám o sobě nedává smysl
vytvořit. „Tvar“ nemá obsah, obsah má až kruh nebo obdélník. Základ
předepíše, co každá podtřída **musí** umět (`area()`), a sám může
přidat hotové chování, které na tom staví (`describe()`, řazení).

Bez kontroly by se chyba projevila pozdě: podtřída zapomene `area()`
a program spadne až ve chvíli, kdy ji někdo zavolá. S `abc` spadne už
**vytvoření instance**.

| Pojem | Význam |
|---|---|
| abstraktní metoda | metoda, kterou podtřída musí přepsat |
| abstraktní třída | třída s aspoň jednou neimplementovanou abstraktní metodou, nejde vytvořit |
| konkrétní třída | podtřída, která doplnila všechny abstraktní metody |

V TS / Javě je to `abstract class` s `abstract` metodami. Python to
řeší knihovnou `abc` (*abstract base classes*), ne klíčovým slovem.

## 2. `ABC` a `@abstractmethod`

```python
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self): ...

    @abstractmethod
    def perimeter(self): ...

    def describe(self):                    # konkrétní metoda, staví na abstraktních
        name = type(self).__name__
        return f"{name}: obsah {self.area():.2f}, obvod {self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius**2

    def perimeter(self):
        return 2 * math.pi * self.radius


Circle(5).describe()                       # 'Circle: obsah 78.54, obvod 31.42'
```

- `class Shape(ABC)` je zkratka za `class Shape(metaclass=ABCMeta)`.
  Metatřídy viz
  [`CLASS_CREATION_AND_METACLASSES.md`](CLASS_CREATION_AND_METACLASSES.md).
- Tělo abstraktní metody bývá `...` (Ellipsis) nebo docstring. Smí
  obsahovat i kód, podtřída ho pak může zavolat přes `super()`.

Pokus vytvořit abstraktní třídu, nebo podtřídu, které něco chybí:

```python
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side**2
    # perimeter chybí


Shape()    # TypeError: Can't instantiate abstract class Shape without an implementation for abstract methods 'area', 'perimeter'
Square(2)  # TypeError: Can't instantiate abstract class Square without an implementation for abstract method 'perimeter'
```

Samotná **definice** `Square` projde. Chyba přijde až při vytvoření
instance. Které metody chybí, Python drží v atributu třídy:

```python
Square.__abstractmethods__                 # frozenset({'perimeter'})
```

Díky společnému základu můžeš psát kód pro „jakýkoli tvar“:

```python
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


shapes = [Circle(1), Rectangle(2, 3)]
round(sum(s.area() for s in shapes), 2)    # 9.14
```

## 3. Abstraktní property a classmethod

`@abstractmethod` jde kombinovat s jinými dekorátory. Musí být
**nejblíž** funkci (nejníž):

```python
class Exporter(ABC):
    @property
    @abstractmethod
    def extension(self): ...

    @classmethod
    @abstractmethod
    def from_config(cls, config): ...


class CsvExporter(Exporter):
    @property
    def extension(self):
        return "csv"

    @classmethod
    def from_config(cls, config):
        return cls()


CsvExporter.from_config({}).extension      # 'csv'
```

Abstraktní property splní i obyčejný atribut třídy, protože Python
kontroluje jen to, že jméno už není abstraktní:

```python
class JsonExporter(Exporter):
    extension = "json"

    @classmethod
    def from_config(cls, config):
        return cls()


JsonExporter().extension                   # 'json'
```

## 4. Varianta bez `abc`: `raise NotImplementedError`

Starší a velmi rozšířený způsob, který používá i Django: metoda
v základu jen vyhodí `NotImplementedError`.

```python
class Storage:
    def save(self, name, content):
        raise NotImplementedError("Podtřída musí implementovat save()")


class MemoryStorage(Storage):
    def __init__(self):
        self.files = {}

    def save(self, name, content):
        self.files[name] = content


Storage()                                  # <__main__.Storage object at 0x...>
Storage().save("a.txt", "x")               # NotImplementedError: Podtřída musí implementovat save()
```

| | `ABC` + `@abstractmethod` | `raise NotImplementedError` |
|---|---|---|
| kdy spadne | při vytvoření instance | až při zavolání metody |
| instance základu | nejde vytvořit | jde |
| volitelné metody | ne, všechny abstraktní jsou povinné | ano, přepíše se jen to, co se použije |
| kde uvidíš | `collections.abc`, vlastní API | Django (`Storage`, `BaseCommand.handle`, `Field` …) |

Pozor na záměnu: `NotImplementedError` je výjimka pro „podtřída to má
doplnit“. `NotImplemented` (bez `Error`) je hodnota, kterou **vrací**
dunder metody jako `__eq__`. Viz
[`DUNDER_METHODS.md`](DUNDER_METHODS.md).

## 5. Vzor template method

Základ napíše **kostru algoritmu** jako konkrétní metodu. Proměnlivé
kroky deleguje na metody, které přepíšou podtřídy. Některé povinně
(abstraktní), jiné volitelně (*hook* s výchozím chováním).

```python
class Report(ABC):
    def render(self, rows):                # kostra, podtřídy ji nepřepisují
        lines = [self.header()]
        lines += [self.format_row(row) for row in rows]
        footer = self.footer()
        if footer:
            lines.append(footer)
        return "\n".join(lines)

    @abstractmethod
    def header(self): ...

    @abstractmethod
    def format_row(self, row): ...

    def footer(self):                      # hook: výchozí je „nic“
        return ""


class CsvReport(Report):
    def header(self):
        return "name;price"

    def format_row(self, row):
        return f"{row['name']};{row['price']}"


class MarkdownReport(Report):
    def header(self):
        return "| name | price |\n|---|---|"

    def format_row(self, row):
        return f"| {row['name']} | {row['price']} |"

    def footer(self):
        return "_konec_"


rows = [{"name": "Mléko", "price": 24.9}, {"name": "Chléb", "price": 39}]
print(CsvReport().render(rows))
# name;price
# Mléko;24.9
# Chléb;39
```

Přesně takhle fungují Django class-based views. `View.dispatch()` je
kostra, která podle HTTP metody zavolá `get()` nebo `post()`.
`ListView.get()` je další kostra, která volá `get_queryset()`
a `get_context_data()`. Ty jen přepíšeš to, co potřebuješ:

```python
# Django (ilustrace, nespouští se)
# class BookList(ListView):
#     model = Book
#
#     def get_queryset(self):              # přepsaný krok
#         return super().get_queryset().filter(published=True)
#
#     def get_context_data(self, **kwargs):  # rozšířený krok
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Knihy"
#         return context
```

Volání `super()` v přepsaném kroku znamená „udělej, co dělá základ,
a já to upravím“. Víc v [`INHERITANCE_AND_SUPER.md`](INHERITANCE_AND_SUPER.md).

## 6. `collections.abc`: metody zadarmo

Modul `collections.abc` obsahuje abstraktní základy pro kontejnery.
Každý předepíše pár abstraktních metod a k nim přidá hotové
**mixin metody**, napsané jen pomocí těch abstraktních.

| Základ | Napíšeš (abstraktní) | Dostaneš zadarmo |
|---|---|---|
| `Iterable` | `__iter__` | (jen `isinstance` kontrolu) |
| `Container` | `__contains__` | |
| `Sized` | `__len__` | |
| `Sequence` | `__getitem__`, `__len__` | `__contains__`, `__iter__`, `__reversed__`, `index`, `count` |
| `MutableSequence` | výše + `__setitem__`, `__delitem__`, `insert` | `append`, `extend`, `pop`, `remove`, `reverse`, `+=` … |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | `__contains__`, `keys`, `items`, `values`, `get`, `__eq__` |
| `MutableMapping` | výše + `__setitem__`, `__delitem__` | `pop`, `popitem`, `clear`, `update`, `setdefault` |
| `Set` | `__contains__`, `__iter__`, `__len__` | `<=`, `<`, `==`, `&`, `\|`, `-`, `^`, `isdisjoint` |
| `MutableSet` | výše + `add`, `discard` | `remove`, `pop`, `clear`, `\|=`, `&=` … |

### `Sequence`

Stačí dvě metody a třída se chová jako seznam jen pro čtení:

```python
from collections.abc import Sequence


class Playlist(Sequence):
    def __init__(self, songs=()):
        self._songs = list(songs)

    def __getitem__(self, index):
        return self._songs[index]

    def __len__(self):
        return len(self._songs)


p = Playlist(["Imagine", "Hey Jude", "Imagine"])
"Hey Jude" in p                            # True
list(reversed(p))                          # ['Imagine', 'Hey Jude', 'Imagine']
p.index("Hey Jude")                        # 1
p.count("Imagine")                         # 2
```

Rozdíl proti „půjčování“ v `DUNDER_METHODS.md`: tam si `in` a
`reversed` poradily přes záložní protokol. Tady jsou to skutečné metody
zděděné z `Sequence`, včetně `index` a `count`, které by jinak
neexistovaly.

### `MutableMapping`

Pět metod a máš plnohodnotný slovník. Slovník s klíči bez ohledu na
velikost písmen:

```python
from collections.abc import MutableMapping


class CaseInsensitiveDict(MutableMapping):
    def __init__(self, data=()):
        self._data = {}
        self.update(data)                  # update je zděděný mixin

    def __getitem__(self, key):
        return self._data[key.casefold()]

    def __setitem__(self, key, value):
        self._data[key.casefold()] = value

    def __delitem__(self, key):
        del self._data[key.casefold()]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


headers = CaseInsensitiveDict({"Content-Type": "text/html"})
headers["content-type"]                    # 'text/html'
"CONTENT-TYPE" in headers                  # True
headers.get("Accept", "*/*")               # '*/*'
headers.setdefault("Accept", "text/plain")  # 'text/plain'
headers.pop("accept")                      # 'text/plain'
dict(headers.items())                      # {'content-type': 'text/html'}
```

Proč ne rovnou `class X(dict)`? Vestavěný `dict` je napsaný v C a jeho
metody `get`, `update` a `setdefault` **nevolají** tvůj přepsaný
`__getitem__` / `__setitem__`. Přepíšeš jednu metodu a ostatní ji
obejdou:

```python
class LowerDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key.casefold(), value)


d = LowerDict()
d["A"] = 1
d.update({"B": 2})                         # update tvůj __setitem__ obešel
d                                          # {'a': 1, 'B': 2}
```

Kdo chce vlastní chování kontejneru, dědí z `collections.abc`.
Alternativou je `collections.UserDict` / `UserList`, které jsou psané
v Pythonu a přepsané metody respektují.

Zapomeneš-li abstraktní metodu, platí totéž co u `ABC`:

```python
class Broken(Sequence):
    def __getitem__(self, index):
        return index


Broken()   # TypeError: Can't instantiate abstract class Broken without an implementation for abstract method '__len__'
```

## 7. `isinstance` s `collections.abc`

`collections.abc` slouží i ke **kontrole schopností**. Ptáš se „umí to
X?“, ne „je to přesně list?“:

```python
from collections.abc import Iterable, Mapping

isinstance([1, 2], Iterable)               # True
isinstance("abc", Iterable)                # True
isinstance(42, Iterable)                   # False
isinstance({"a": 1}, Mapping)              # True
isinstance(headers, Mapping)               # True
```

Některé základy (`Iterable`, `Sized`, `Container`, `Hashable`) uznají
třídu i **bez dědění**, stačí, aby měla správnou metodu. Zajišťuje to
`__subclasshook__`:

```python
class Countdown:
    def __iter__(self):
        yield from (3, 2, 1)


isinstance(Countdown(), Iterable)          # True
```

`Sequence` a `Mapping` takhle nefungují: vyžadují dědění, nebo ruční
registraci `Sequence.register(MyClass)`.

Stejné typy se používají v anotacích: `def total(items: Iterable[float])`.
Viz [`TYPE_HINTS.md`](TYPE_HINTS.md).

## 8. `typing.Protocol`: rozhraní bez dědičnosti

ABC vyžaduje, aby třída z rodiče **dědila**. `Protocol` popisuje jen
**tvar**: kdo má správné metody, ten vyhovuje. Je to obdoba TS
`interface`, kde také stačí shodná struktura (*structural typing*).

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class HasArea(Protocol):
    def area(self) -> float: ...


class Plot:                                # nedědí z ničeho
    def area(self):
        return 120.0


isinstance(Plot(), HasArea)                # True
isinstance("text", HasArea)                # False
```

- Protokol je určený hlavně pro **type checker** (mypy, Pylance). Ten
  hlídá, že předaný objekt metody má.
- `@runtime_checkable` povolí i `isinstance`. Kontroluje se ale jen
  existence metod, ne jejich signatura.

| | ABC | Protocol |
|---|---|---|
| vztah | třída musí dědit | stačí mít metody |
| kontrola | při vytvoření instance | type checker (a volitelně `isinstance`) |
| sdílený kód | ano, konkrétní metody v základu | ne, jen popis |
| obdoba v TS | `abstract class` | `interface` |

## 9. Časté chyby

| Příznak | Příčina |
|---|---|
| `TypeError: Can't instantiate abstract class X without an implementation for abstract method 'y'` | podtřída nepřepsala `y`, nebo má překlep ve jméně |
| abstraktní třídu jde bez chyby vytvořit | chybí `ABC` v rodičích, `@abstractmethod` bez `ABCMeta` nic nedělá |
| `@abstractmethod` s `@property` nefunguje | špatné pořadí, `@abstractmethod` patří nejníž |
| `NotImplementedError` až za běhu | základ používá `raise NotImplementedError`, kontrola při vytvoření není |
| přepsaný `__setitem__` u podtřídy `dict` se ignoruje | metody `dict` ho obcházejí, použij `MutableMapping` nebo `UserDict` |
| `TypeError` u `\|` / `&` na vlastním `MutableSet` | `__init__` nepřijímá iterable, mixin metody tvoří výsledek přes `cls(iterable)` |
| `return NotImplementedError` v `__eq__` | záměna, `__eq__` vrací `NotImplemented` |
