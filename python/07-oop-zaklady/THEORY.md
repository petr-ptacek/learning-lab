# 07 — OOP: základy

## Cíl

Naučit se psát vlastní **třídy**: spojit data (atributy) a chování
(metody) do jednoho typu, jako jsou vestavěné `list` nebo `str`.
Hlavně ale **číst** třídy, na kterých stojí Django: model je třída,
pole modelu jsou atributy třídy, `objects` je atribut třídy, `__str__`
je dunder metoda a `@property` nebo `@classmethod` uvidíš v každém
druhém projektu.

Na čem to stavíš: funkce a `*args` / `**kwargs` z
[`03-funkce`](../03-funkce/THEORY.md), slovníky z
[`04-datove-struktury`](../04-datove-struktury/THEORY.md) (instance si
atributy drží ve slovníku) a iterační protokol z
[`06-generatory-iteratory`](../06-generatory-iteratory/THEORY.md)
(`__iter__` napíšeš jako generátor).

K čemu to bude: navazuje `08-oop-dedicnost`
(dědičnost, mixiny, vnořená `class Meta`, jak Django model „posbírá“
svá pole), pak Django modely, formuláře a class-based views.
JS obdoba: `class` s `constructor` a `this`.

Do hloubky (výtah z článků v `RESOURCES.md`):

- [`../docs/CLASSES_AND_INSTANCES.md`](../docs/CLASSES_AND_INSTANCES.md):
  jak Python hledá atributy, atributy třídy vs. instance, `self`,
  dynamické atributy, třída jako objekt, srovnání s JS
- [`../docs/METHODS_AND_PROPERTIES.md`](../docs/METHODS_AND_PROPERTIES.md):
  tři druhy metod, alternativní konstruktory, `@property`,
  `cached_property`
- [`../docs/DUNDER_METHODS.md`](../docs/DUNDER_METHODS.md): `__str__` /
  `__repr__`, porovnávání a `__hash__`, operátory, kontejnerový protokol
- [`../docs/DATACLASSES.md`](../docs/DATACLASSES.md): `@dataclass`,
  `field`, `frozen`, `order`, `__post_init__`, `asdict`

## Třída a instance

```python
class Product:
    def __init__(self, name, price, quantity=0):
        self.name = name              # atribut instance
        self.price = price
        self.quantity = quantity

    def total_value(self):            # metoda
        return round(self.price * self.quantity, 2)


milk = Product("Mléko", 24.9, 10)    # instance; bez `new`
milk.total_value()                    # 249.0
milk.quantity = 7                     # atributy jsou běžně zapisovatelné
milk.total_value()                    # 174.3
```

- `class Product:` definuje nový typ. Jména tříd se píšou `PascalCase`.
- Volání `Product(...)` vytvoří **instanci** a zavolá `__init__`.
- `__init__` je inicializace, ne konstruktor v pravém smyslu: objekt už
  existuje, `__init__` mu jen nastaví atributy. Nic nevrací.
- `self` je instance, na které se metoda volá. Python ho předává
  **automaticky** jako první argument: `milk.total_value()` je totéž
  co `Product.total_value(milk)`. V definici ho ale psát musíš.

| Python | JS |
|---|---|
| `class Product:` | `class Product {` |
| `def __init__(self, name):` | `constructor(name) {` |
| `self.name = name` | `this.name = name` |
| `Product("Mléko")` | `new Product("Mléko")` |
| `self` výslovně v parametrech | `this` implicitně |

## Atributy instance vs. atributy třídy

Tohle je **nejdůležitější** věc pro pochopení Django modelů.

```python
class Ticket:
    next_id = 1                  # atribut TŘÍDY: jeden, sdílený všemi
    priority = "normal"

    def __init__(self, title):
        self.id = Ticket.next_id  # atribut INSTANCE: každá má svůj
        Ticket.next_id += 1
        self.title = title


a = Ticket("Nejde login")
b = Ticket("Pomalý web")
a.id, b.id, Ticket.next_id      # (1, 2, 3)
a.priority                      # 'normal' — instance ho nemá, najde se na třídě
b.priority = "high"             # vytvoří atribut na INSTANCI b, třídu nemění
a.priority, b.priority          # ('normal', 'high')
vars(b)                         # {'id': 2, 'title': 'Pomalý web', 'priority': 'high'}
```

Když čteš `obj.x`, Python hledá: **instance → třída** (→ rodiče, v
`08`). Zápis `obj.x = ...` ale vždycky zapisuje **do instance**, a tím
atribut třídy „zastíní“.

Past: měnitelný atribut třídy je sdílený všemi instancemi.

```python
class Cart:
    items = []                   # ŠPATNĚ: jeden seznam pro všechny košíky

    def add(self, item):
        self.items.append(item)  # nemění se atribut, mění se sdílený seznam


c1, c2 = Cart(), Cart()
c1.add("mléko")
c2.items                         # ['mléko'] — sdílený!
```

Seznam, dict a set patří do `__init__` (`self.items = []`). Do atributů
třídy dávej konstanty a výchozí hodnoty.

V Djangu: `title = models.CharField(...)` je atribut **třídy** `Book`.
Popisuje sloupec, je jen jeden. Hodnota konkrétní knihy (`book.title`)
je atribut **instance**. Jak Django z jednoho udělá druhé, rozebírá
`08-oop-dedicnost`.

## Tři druhy metod

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def with_vat(self, rate=0.21):      # instanční: pracuje s jednou instancí
        return round(self.price * (1 + rate), 2)

    @classmethod
    def from_csv_line(cls, line):       # třídní: dostane třídu, typicky vyrobí instanci
        name, price = line.split(";")
        return cls(name, float(price))

    @staticmethod
    def is_valid_code(code):            # statická: jen funkce uložená ve třídě
        return len(code) == 8 and code.isdigit()


Product.from_csv_line("Káva;189").with_vat()   # 228.69
Product.is_valid_code("12345678")              # True
```

| Druh | První parametr | Kdy |
|---|---|---|
| instanční | `self` (instance) | práce s daty jedné instance, nejčastější |
| `@classmethod` | `cls` (třída) | alternativní konstruktor (`from_dict`, `from_csv_line`), práce s atributy třídy |
| `@staticmethod` | nic | pomocná funkce, která logicky patří ke třídě |

V Djangu: `Book.objects.create(...)` je volání metody na atributu třídy,
`from_db` je classmethod.

## `@property`: metoda, která se tváří jako atribut

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):              # čtení: t.fahrenheit (bez závorek)
        return round(self.celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value):       # zápis: t.fahrenheit = 212
        self.celsius = round((value - 32) * 5 / 9, 2)


t = Temperature(25)
t.fahrenheit                           # 77.0
t.fahrenheit = 212
t.celsius                              # 100.0
```

Použití: hodnota **dopočítaná** z jiných atributů (`full_name`,
`total`), **validace** při zápisu, atribut jen pro čtení (property bez
setteru). Nepiš `get_x()` / `set_x()` jako v Javě. Začni obyčejným
atributem, a když je později potřeba logika, předělej ho na property.
Volající kód se nezmění.

Validace se dělá vyhozením výjimky: `raise ValueError("Cena nesmí být
záporná")`. Program se v tom místě zastaví s chybou. Výjimky do hloubky
(chytání přes `try` / `except`) přijdou v `10-vyjimky`.

## Dunder metody: jak se třída chová k operátorům a vestavěným funkcím

„Dunder“ = *double underscore*, `__jméno__`. Nevoláš je přímo, volá je
Python, když na objekt použiješ operátor nebo vestavěnou funkci:

| Zápis | Volá | Bez definice |
|---|---|---|
| `print(x)`, `str(x)`, `f"{x}"` | `__str__` | použije `__repr__` |
| `repr(x)`, výpis v seznamu, konzole | `__repr__` | `<__main__.Product object at 0x...>` |
| `x == y` | `__eq__` | `True` jen pro **tentýž** objekt (`is`) |
| `x < y`, `sorted`, `max` | `__lt__` | `TypeError` |
| `x + y` | `__add__` | `TypeError` |
| `len(x)` | `__len__` | `TypeError` |
| `for v in x`, `list(x)` | `__iter__` | `TypeError` |
| `v in x` | `__contains__` | projde `__iter__` |
| `x[i]` | `__getitem__` | `TypeError` |
| `bool(x)`, `if x:` | `__bool__`, pak `__len__` | vždy `True` |

```python
class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __str__(self):                         # pro lidi
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):                        # pro programátora: jak objekt vyrobit
        return f"Money({self.amount!r}, {self.currency!r})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented              # „neumím porovnat“, Python zkusí jinak
        return (self.amount, self.currency) == (other.amount, other.currency)


price = Money(249.9)
print(price)                                   # 249.90 CZK
[price]                                        # [Money(249.9, 'CZK')]
price == Money(249.9)                          # True
```

`__str__` je v Djangu všude: to, co vrátí, vidíš v adminu, ve
výběrových polích formulářů i v shellu.

Kdo definuje `__eq__`, přijde o `__hash__`: objekt pak nejde dát do
`set` ani použít jako klíč dictu. Proč a co s tím, je v
[`DUNDER_METHODS.md`](../docs/DUNDER_METHODS.md#3-__eq__-a-__hash__).

## `@dataclass`: třída na data bez psaní `__init__`

```python
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list[str] = field(default_factory=list)   # měnitelný default jen takhle

    def total_value(self):
        return round(self.price * self.quantity, 2)


Product("Mléko", 24.9, 10)
# Product(name='Mléko', price=24.9, quantity=10, tags=[])
Product("Mléko", 24.9) == Product("Mléko", 24.9)    # True
```

Dekorátor podle anotací vygeneruje `__init__`, `__repr__` a `__eq__`.
Hodí se pro objekty, které jsou hlavně data. `frozen=True` udělá
neměnnou a hashovatelnou třídu, `order=True` přidá řazení. Django
modely dataclass **nejsou**, princip „popíšu pole na třídě a zbytek se
vygeneruje“ je ale stejný.

## Konvence: `_soukromé`

Python nemá `private`. Jméno začínající podtržítkem (`self._price`)
znamená „vnitřní věc, zvenku nesahej“. Je to jen dohoda, technicky
přístupné to zůstává. `__dvě_podtržítka` (bez podtržítek na konci)
Python přejmenuje (*name mangling*), používá se vzácně.

## Všechno je objekt, i třída

```python
type(42)          # <class 'int'>
type(Product)     # <class 'type'>
```

Třída je objekt jako každý jiný: dá se uložit do proměnné, předat
funkci (to dělá `cls` v classmethod) a může mít atributy. Atributem
může být i **jiná třída**:

```python
class Book:
    title = "?"

    class Meta:                  # vnořená třída = jen další atribut třídy Book
        ordering = ["title"]


Book.Meta.ordering               # ['title']
```

Přesně tohle je `class Meta:` v Django modelu. Sama nic nedělá, je to
schránka na nastavení. Čte ji až Django při vytvoření třídy modelu,
podrobně v `08-oop-dedicnost`.

## Django model očima tohoto konceptu

```python
class Book(models.Model):                       # dědičnost → 08
    title = models.CharField(max_length=200)    # atribut třídy (popis sloupce)
    price = models.DecimalField(...)
    objects = BookManager()                     # atribut třídy

    class Meta:                                 # vnořená třída = atribut třídy
        ordering = ["title"]

    def __str__(self):                          # dunder: text v adminu
        return self.title

    @property
    def price_with_vat(self):                   # dopočítaná hodnota
        return self.price * Decimal("1.21")

    @classmethod
    def create_draft(cls, title):               # alternativní konstruktor
        return cls(title=title, price=0)
```

## Časté chyby

| Příznak | Příčina |
|---|---|
| `TypeError: Product.total_value() takes 0 positional arguments but 1 was given` | v definici metody chybí `self` |
| `NameError: name 'price' is not defined` uvnitř metody | chybí `self.`: atributy instance jsou vždy `self.price` |
| všechny instance sdílí stejný seznam | měnitelný atribut třídy místo `self.items = []` v `__init__` |
| `print(obj)` vypíše `<__main__.X object at 0x...>` | chybí `__str__` / `__repr__` |
| `obj == jiny` je `False` pro stejná data | chybí `__eq__` (nebo použij `@dataclass`) |
| `TypeError: 'float' object is not callable` | property voláš se závorkami: `t.fahrenheit()` |
| `AttributeError: property 'x' of 'X' object has no setter` | zápis do property bez setteru |
| `TypeError: unhashable type` | definoval jsi `__eq__` bez `__hash__` |
| `RecursionError` v setteru | v setteru zapisuješ do `self.price` místo `self._price` |
