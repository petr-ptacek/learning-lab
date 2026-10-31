# Metody a `@property`

Výtah z Real Python *Python's Instance, Class, and Static Methods
Demystified* a *Python's property(): Add Managed Attributes to Your
Classes*, plus oficiální docs k `classmethod`, `staticmethod`,
`property` a `functools.cached_property`. Odkazy jsou v
[`07-oop-zaklady/RESOURCES.md`](../07-oop-zaklady/RESOURCES.md),
přehled v [`THEORY.md`](../07-oop-zaklady/THEORY.md#tři-druhy-metod).

Souvisí: co je `self` a jak se hledají atributy, v
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Tři druhy metod vedle sebe](#1-tři-druhy-metod-vedle-sebe)
2. [`@classmethod`: alternativní konstruktory](#2-classmethod-alternativní-konstruktory)
3. [Proč `cls`, a ne jméno třídy](#3-proč-cls-a-ne-jméno-třídy)
4. [`@staticmethod`: kdy ano, kdy radši funkce](#4-staticmethod-kdy-ano-kdy-radši-funkce)
5. [`@property`: getter](#5-property-getter)
6. [Setter: validace a převod](#6-setter-validace-a-převod)
7. [Property jen pro čtení](#7-property-jen-pro-čtení)
8. [`cached_property`: spočítat jednou](#8-cached_property-spočítat-jednou)
9. [Kdy property nepoužít](#9-kdy-property-nepoužít)
10. [V Djangu](#10-v-djangu)

---

## 1. Tři druhy metod vedle sebe

```python
class Demo:
    def instance_method(self):
        return f"instance: {self!r}"

    @classmethod
    def class_method(cls):
        return f"třída: {cls.__name__}"

    @staticmethod
    def static_method():
        return "statická: nic nedostane"


d = Demo()
d.class_method()           # 'třída: Demo' — jde volat i přes instanci
Demo.class_method()        # 'třída: Demo'
Demo.static_method()       # 'statická: nic nedostane'
Demo.instance_method()     # TypeError: Demo.instance_method() missing 1 required positional argument: 'self'
```

| | Dostane | Může číst/měnit instanci | Může číst/měnit třídu | Volá se |
|---|---|---|---|---|
| instanční | `self` | ano | ano (`type(self)`) | přes instanci |
| `@classmethod` | `cls` | ne | ano | přes třídu i instanci |
| `@staticmethod` | nic | ne | ne | přes třídu i instanci |

Dekorátor jen mění, **co** Python předá jako první argument. Tělo
metody je obyčejná funkce.

## 2. `@classmethod`: alternativní konstruktory

Python nemá přetěžování konstruktorů (`__init__` je jen jeden). Když
chceš objekt vyrábět z různých vstupů, napíšeš classmethod
`from_něco`, která data připraví a zavolá `cls(...)`:

```python
class Product:
    def __init__(self, name, price, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product({self.name!r}, {self.price!r}, {self.quantity!r})"

    @classmethod
    def from_csv_line(cls, line):
        name, price, quantity = line.split(";")
        return cls(name.strip(), float(price), int(quantity))

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"], data.get("quantity", 0))


Product.from_csv_line("Mléko;24.9;10")       # Product('Mléko', 24.9, 10)
Product.from_dict({"name": "Sůl", "price": 12.5})   # Product('Sůl', 12.5, 0)
```

Takové konstruktory najdeš i ve standardní knihovně:
`dict.fromkeys(...)`, `datetime.fromisoformat(...)`,
`int.from_bytes(...)`.

```python
dict.fromkeys(["a", "b"], 0)                 # {'a': 0, 'b': 0}
```

Druhé použití classmethod je práce s atributy třídy (počítadla,
registry), viz bonus cvičení `05`.

## 3. Proč `cls`, a ne jméno třídy

`cls` je třída, **přes kterou** se metoda zavolala. U podtřídy je to
podtřída:

```python
class SpecialProduct(Product):     # dědičnost, viz 08
    pass


type(SpecialProduct.from_csv_line("A;1;2")).__name__    # 'SpecialProduct'
```

Kdyby `from_csv_line` volala `Product(...)` natvrdo, vracela by vždy
`Product`, i při volání přes podtřídu. S `cls(...)` funguje správně.
Stejně tak `cls.next_id` místo `Product.next_id`.

## 4. `@staticmethod`: kdy ano, kdy radši funkce

```python
class Product:
    @staticmethod
    def is_valid_code(code):
        return len(code) == 8 and code.isdigit()


Product.is_valid_code("12345678")     # True
Product.is_valid_code("1234567a")     # False
```

Statická metoda nedostane nic, je to funkce, která jen **bydlí** ve
třídě. Smysl má, když logicky patří k třídě a volající ji tam čeká
hledat (`Product.is_valid_code`). Jinak je v Pythonu úplně normální
napsat obyčejnou funkci na úrovni modulu. Na rozdíl od Javy nemusí
být všechno ve třídě.

Rychlé rozhodnutí:

- potřebuješ instanci → instanční metoda,
- potřebuješ třídu (vyrobit instanci, číst atribut třídy) → `@classmethod`,
- nepotřebuješ ani jedno → funkce v modulu. `@staticmethod` jen tehdy,
  když k třídě opravdu patří.

## 5. `@property`: getter

Property je metoda, která se **čte jako atribut**: bez závorek.

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


p = Person("Anna", "Nováková")
p.full_name               # 'Anna Nováková'
p.last_name = "Dvořáková"
p.full_name               # 'Anna Dvořáková' — vždy aktuální, počítá se při čtení
p.full_name()             # TypeError: 'str' object is not callable
```

Proč ne obyčejný atribut `self.full_name = ...` v `__init__`? Ten by
se po změně `last_name` neaktualizoval. Proč ne metoda `full_name()`?
Klidně může být, ale property je pro hodnotu, která se **chová jako
údaj** objektu. Volající nemusí vědět, jestli je uložená, nebo
spočítaná.

## 6. Setter: validace a převod

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price          # projde přes setter i tady

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Cena nesmí být záporná")
        self._price = round(value, 2)


x = Product("Mléko", 24.999)
x.price                   # 25.0
vars(x)                   # {'name': 'Mléko', '_price': 25.0}
x.price = -5              # ValueError: Cena nesmí být záporná
```

Jak to celé funguje:

- hodnota se ukládá pod **jiným jménem** (`_price`). Kdyby setter
  zapisoval do `self.price`, zavolal by sám sebe → `RecursionError`,
- `@price.setter` musí mít **stejné jméno** jako getter,
- v `__init__` piš `self.price = price`, ne `self._price = price`.
  Validace pak platí i pro vytvoření objektu.

Zvenku je to pořád `x.price = 30`. Původně obyčejný atribut můžeš
kdykoliv předělat na property a nikde jinde v kódu se nic nezmění.
Proto se v Pythonu **nezačíná** gettery a settery „pro jistotu“.

Setter i u dopočítané hodnoty:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return round(self.celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = round((value - 32) * 5 / 9, 2)


t = Temperature(25)
t.fahrenheit = 212
t.celsius                 # 100.0
```

Uložená je jen jedna hodnota (`celsius`), druhá se z ní vždy
dopočítá. Nemůžou se rozejít.

## 7. Property jen pro čtení

Property bez setteru zápis nepovolí:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return round(3.14159 * self.radius ** 2, 2)


c = Circle(2)
c.area                    # 12.57
c.area = 100              # AttributeError: property 'area' of 'Circle' object has no setter
```

Hodí se pro hodnoty, které dávají smysl jen dopočítané, a pro
„veřejný pohled na vnitřní stav“: `_balance` uvnitř, `balance` jen
pro čtení venku.

## 8. `cached_property`: spočítat jednou

Property se počítá **při každém čtení**. Když je výpočet drahý
(dotaz do DB, velký soubor), použij `functools.cached_property`:
spočítá se při prvním čtení a výsledek se uloží do instance.

```python
from functools import cached_property


class Report:
    def __init__(self, numbers):
        self.numbers = numbers

    @cached_property
    def total(self):
        print("počítám…")
        return sum(self.numbers)


r = Report([10, 20, 30])
r.total                   # vypíše počítám…, vrátí 60
r.total                   # 60 — bez výpočtu
r.numbers.append(100)
r.total                   # 60 — POZOR: zastaralé, cache o změně neví
del r.total               # smaže cache
r.total                   # vypíše počítám…, vrátí 160
```

Jak to funguje: hodnota se uloží do `vars(r)` pod stejným jménem a
čtení ji pak najde dřív než property (viz hledání atributů v
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md#3-jak-python-hledá-atribut)).
Smazáním se cache vyprázdní.

Kdy: hodnota se během života objektu nemění, nebo ti nevadí, že bude
zastaralá. Django má vlastní `django.utils.functional.cached_property`
se stejným chováním. Používá se u modelů a views, typicky pro výsledek
dotazu, který se v jednom requestu čte víckrát.

## 9. Kdy property nepoužít

- **Drahá nebo pomalá operace bez cache.** `obj.x` vypadá jako
  okamžité čtení. Kdo by čekal, že spustí HTTP požadavek? Radši
  metoda `fetch_x()`.
- **Operace s vedlejším efektem.** Čtení atributu by nic nemělo měnit.
- **Potřebuješ parametry.** Property žádné nebere. To je metoda.
- **Jen přeposílá atribut bez logiky.** `@property def name(self):
  return self._name` + setter, který jen ukládá, je zbytečná Java.
  Nech obyčejný atribut.

## 10. V Djangu

```python
class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    @property
    def is_paid(self):                    # dopočítaný údaj, v šabloně {{ order.is_paid }}
        return self.status == "paid"

    @classmethod
    def create_draft(cls, **fields):      # alternativní konstruktor
        return cls.objects.create(status="draft", **fields)
```

- šablony volají property i metody bez argumentů stejně: `{{
  order.is_paid }}`,
- property **nejde** použít ve filtrech QuerySetu
  (`Order.objects.filter(is_paid=True)` nefunguje). Filtruje se podle
  sloupců v DB, property existuje jen v Pythonu,
- `Model.objects` je atribut třídy, `objects.create(...)` je metoda
  manageru, ne classmethod modelu. Princip „vyrob instanci přes třídu“
  je ale stejný.
