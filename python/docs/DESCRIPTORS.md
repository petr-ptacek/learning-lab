# Deskriptory

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(hlavně oficiální *Descriptor Guide* a Real Python *Python Descriptors:
An Introduction*). Přehled je v
[`THEORY.md`](../08-oop-dedicnost/THEORY.md).

Deskriptor je mechanismus, na kterém stojí `@property`, `@classmethod`,
`cached_property`, vázané metody i **pole Django modelů**. Když
pochopíš deskriptory, přestane být záhadou, proč `Book.title` vrací
pole, ale `book.title` vrací text.

Navazuje na hledání atributů v
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md) a na `@property`
v [`METHODS_AND_PROPERTIES.md`](METHODS_AND_PROPERTIES.md). Jak se
deskriptory zapojí při vytváření třídy, je v
[`CLASS_CREATION_AND_METACLASSES.md`](CLASS_CREATION_AND_METACLASSES.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Co je deskriptor](#1-co-je-deskriptor)
2. [`__get__`: čtení](#2-__get__-čtení)
3. [`__set_name__`: deskriptor zjistí své jméno](#3-__set_name__-deskriptor-zjistí-své-jméno)
4. [`__set__`: zápis a validace](#4-__set__-zápis-a-validace)
5. [Data vs. non-data deskriptor a pořadí hledání](#5-data-vs-non-data-deskriptor-a-pořadí-hledání)
6. [`property` je deskriptor](#6-property-je-deskriptor)
7. [Metody jsou deskriptory](#7-metody-jsou-deskriptory)
8. [Vlastní `cached_property`](#8-vlastní-cached_property)
9. [Deskriptor vs. `property`: kdy co](#9-deskriptor-vs-property-kdy-co)
10. [Deskriptory v Djangu](#10-deskriptory-v-djangu)
11. [Časté chyby](#11-časté-chyby)

---

## 1. Co je deskriptor

Deskriptor je objekt uložený jako **atribut třídy**, který má aspoň
jednu z metod `__get__`, `__set__`, `__delete__`. Když pak přistoupíš
k atributu **přes instanci**, Python nevrátí samotný objekt, ale zavolá
jeho metodu:

| Zápis | Co Python udělá, když je `Product.price` deskriptor |
|---|---|
| `p.price` | `Product.__dict__["price"].__get__(p, Product)` |
| `p.price = 10` | `Product.__dict__["price"].__set__(p, 10)` |
| `del p.price` | `Product.__dict__["price"].__delete__(p)` |
| `Product.price` | `Product.__dict__["price"].__get__(None, Product)` |

Deskriptor tedy **zachytí** přístup k atributu a rozhodne, co se
stane. Funguje to jen tehdy, když je deskriptor na **třídě**. V
`__dict__` instance je to obyčejná hodnota.

## 2. `__get__`: čtení

```python
class Answer:
    def __get__(self, obj, objtype=None):
        return 42


class Universe:
    answer = Answer()          # instance deskriptoru jako atribut TŘÍDY


u = Universe()
u.answer                       # 42
Universe.answer                # 42
```

`__get__(self, obj, objtype)` dostane:

- `self`: samotný deskriptor (objekt `Answer()`),
- `obj`: instanci, přes kterou se čte, nebo `None` při čtení přes třídu,
- `objtype`: třídu.

Konvence: při čtení přes třídu (`obj is None`) vrať deskriptor sám.
Díky tomu jde deskriptor prozkoumat a Django ti tak přes `Book.title`
ukáže objekt pole:

```python
class Loud:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.text.upper()


class Message:
    shout = Loud()

    def __init__(self, text):
        self.text = text


Message("ahoj").shout          # 'AHOJ'
type(Message.shout).__name__   # 'Loud'
```

## 3. `__set_name__`: deskriptor zjistí své jméno

Deskriptor často potřebuje vědět, pod jakým jménem je ve třídě
uložený, například aby věděl, kam hodnotu uložit nebo co napsat do
chybové hlášky. Python mu to řekne sám: při vytváření třídy zavolá
`__set_name__(owner, name)` na každém atributu, který tu metodu má.

```python
class Field:
    def __set_name__(self, owner, name):
        print(f"{owner.__name__}.{name}")
        self.name = name


class Book:
    title = Field()
    year = Field()
# vypíše: Book.title
#         Book.year


Book.__dict__["year"].name     # 'year'
```

Volá se jednou, **při definici třídy**, ne při vytváření instancí.
Proto `title = models.CharField()` v Djangu nemusí jméno sloupce
opakovat: pole se jméno dozví samo. Django na to historicky používá
vlastní `contribute_to_class`, princip je ale stejný.

## 4. `__set__`: zápis a validace

Znovupoužitelná validace, kterou bys s `@property` musel psát pro
každý atribut zvlášť:

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} nesmí být záporné: {value}")
        obj.__dict__[self.name] = value


class String:
    def __init__(self, max_length):
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if len(value) > self.max_length:
            raise ValueError(f"{self.name}: max {self.max_length} znaků")
        obj.__dict__[self.name] = value


class Product:
    name = String(max_length=10)
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, name, price, quantity=0):
        self.name = name                   # jde přes String.__set__
        self.price = price                 # jde přes PositiveNumber.__set__
        self.quantity = quantity


p = Product("Mléko", 24.9, 10)
p.price                                    # 24.9
vars(p)                                    # {'name': 'Mléko', 'price': 24.9, 'quantity': 10}
p.price = -1                               # ValueError: price nesmí být záporné: -1
Product("Velmi dlouhý název", 10)          # ValueError: name: max 10 znaků
Product.price.name                         # 'price'
```

Jedna třída `PositiveNumber` hlídá libovolně mnoho atributů v
libovolně mnoha třídách. Deskriptor je jen jeden pro všechny instance,
proto hodnotu ukládá do instance (`obj.__dict__`), ne do sebe. Kdyby
psal `self.value = value`, sdílely by ji všechny produkty, jako
seznam na třídě v `Cart`.

Ukládání pod **stejné jméno**, `obj.__dict__["price"]`, funguje jen
díky pravidlu z další sekce: data deskriptor má přednost před
`__dict__` instance.

## 5. Data vs. non-data deskriptor a pořadí hledání

| Druh | Má | Příklady |
|---|---|---|
| **data deskriptor** | `__set__` nebo `__delete__` (a obvykle `__get__`) | `property`, `PositiveNumber` výše |
| **non-data deskriptor** | jen `__get__` | funkce (metody), `classmethod`, `staticmethod`, `cached_property` |

Rozdíl je v tom, **kdo vyhraje** při čtení `obj.x`. Celé pořadí
(`object.__getattribute__`):

1. **data deskriptor** na třídě (nebo na rodiči v MRO) → jeho `__get__`,
2. `obj.__dict__["x"]`, atribut instance,
3. **non-data deskriptor** na třídě → jeho `__get__`,
4. obyčejný atribut třídy,
5. `AttributeError` (předtím ještě zkusí `__getattr__`, pokud existuje).

Zápis `obj.x = v` je jednodušší: když je na třídě data deskriptor,
volá se jeho `__set__`. Jinak se hodnota zapíše do `obj.__dict__`.

Ukázka: data deskriptor vyhraje i nad ručně podstrčeným `__dict__`,
non-data deskriptor prohraje:

```python
class DataDesc:
    def __get__(self, obj, objtype=None):
        return "z deskriptoru"

    def __set__(self, obj, value):
        pass                               # zápis ignoruje


class NonDataDesc:
    def __get__(self, obj, objtype=None):
        return "z deskriptoru"


class Demo:
    data = DataDesc()
    nondata = NonDataDesc()


d = Demo()
d.__dict__["data"] = "z instance"
d.__dict__["nondata"] = "z instance"
d.data                                     # 'z deskriptoru'
d.nondata                                  # 'z instance'
```

Tohle pravidlo vysvětluje:

- proč zápis do property bez setteru nevytvoří atribut instance, ale
  skončí chybou (property je data deskriptor vždycky),
- proč jde metodu na instanci zastínit (`obj.save = lambda: ...`):
  funkce je non-data deskriptor,
- proč `cached_property` po prvním čtení „zmizí“ z cesty (sekce 8).

## 6. `property` je deskriptor

`property` je vestavěná třída s `__get__`, `__set__` a `__delete__`,
které volají tvoje funkce. Zjednodušeně:

```python
class MyProperty:
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("property nemá setter")
        self.fset(obj, value)

    def setter(self, fset):
        return MyProperty(self.fget, fset)  # nová property i se setterem


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @MyProperty
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9


t = Temperature(100)
t.fahrenheit                               # 212.0
t.fahrenheit = 32
t.celsius                                  # 0.0
hasattr(property, "__set__")               # True
```

`@MyProperty` nad metodou je jen `fahrenheit = MyProperty(fahrenheit)`.
Výsledek je deskriptor uložený jako atribut třídy.

## 7. Metody jsou deskriptory

Funkce má metodu `__get__`, takže každá funkce v těle třídy je non-data
deskriptor. Čtení `obj.metoda` zavolá `funkce.__get__(obj, Třída)` a
to vrátí **vázanou metodu**, funkci s přilepeným `self`. Odtud pochází
`self`, které Python předává „automaticky“:

```python
class Greeter:
    def hello(self):
        return f"ahoj z {type(self).__name__}"


g = Greeter()
f = Greeter.__dict__["hello"]              # obyčejná funkce
type(f).__name__                           # 'function'
bound = f.__get__(g, Greeter)              # přesně tohle dělá g.hello
type(bound).__name__                       # 'method'
bound()                                    # 'ahoj z Greeter'
bound.__self__ is g                        # True
```

Stejně fungují `classmethod` (její `__get__` přilepí třídu místo
instance) a `staticmethod` (její `__get__` vrátí funkci beze změny).
Proto `type(Product.from_dict)` vrátí `method` a
`type(Product.is_valid_code)` vrátí `function`.

## 8. Vlastní `cached_property`

Non-data deskriptor, který při prvním čtení spočítá hodnotu a uloží ji
do `obj.__dict__` pod **stejným jménem**. Při dalším čtení vyhraje
`__dict__` instance (krok 2 před krokem 3), takže se deskriptor už
vůbec nezavolá:

```python
class cached:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value    # další čtení najde hodnotu v instanci
        return value


class Report:
    def __init__(self, numbers):
        self.numbers = numbers

    @cached
    def total(self):
        print("počítám…")
        return sum(self.numbers)


r = Report([1, 2, 3])
r.total                                    # 6  (vypíše počítám…)
r.total                                    # 6  (bez výpisu, čte se z __dict__)
vars(r)                                    # {'numbers': [1, 2, 3], 'total': 6}
del r.total                                # smaže hodnotu z instance
r.total                                    # 6  (znovu počítám…)
```

Přesně tak funguje `functools.cached_property` i Django
`django.utils.functional.cached_property`. Kdyby `cached` měl
`__set__`, byl by data deskriptorem a cache by nikdy nezafungovala.

## 9. Deskriptor vs. `property`: kdy co

| Situace | Použij |
|---|---|
| jeden dopočítaný / validovaný atribut v jedné třídě | `@property` |
| stejná logika pro mnoho atributů nebo tříd (validace typů, rozsahů) | vlastní deskriptor |
| drahý výpočet jednou za život objektu | `functools.cached_property` |
| knihovna, kde uživatel popisuje strukturu atributy třídy (ORM, formuláře, serializery) | deskriptory + `__set_name__` nebo `__init_subclass__` |

V běžném aplikačním kódu vlastní deskriptory skoro nepíšeš. Hlavně je
potkáš **v knihovnách** a teď víš, co se děje.

## 10. Deskriptory v Djangu

Model:

```python
# Django (ilustrace, nespouští se)
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

- Při vytváření třídy modelu zavolá Django na každém poli
  `contribute_to_class(cls, name)`. Pole se zaregistruje do
  `Book._meta` a na třídu místo sebe dosadí **deskriptor**:
  `setattr(cls, attname, self.descriptor_class(self))`.
- Pro běžná pole je to `DeferredAttribute`, non-data deskriptor s jen
  `__get__`. Hodnota konkrétní knihy leží v `book.__dict__["title"]`,
  takže ji běžné čtení najde přímo v instanci. Deskriptor zasáhne jen
  tehdy, když hodnota v `__dict__` chybí, například u pole odloženého
  přes `.defer("title")`. Pak ji dotáhne z databáze.
- `Book.title` vrátí přes třídu ten deskriptor (`obj is None` → `self`)
  a přes `Book.title.field` se dostaneš k objektu pole. Seznam polí je
  v `Book._meta.get_fields()`.
- `ForeignKey` dosadí `ForwardManyToOneDescriptor`, data deskriptor
  s `__get__` i `__set__`. `book.author` při prvním čtení načte autora
  z databáze a uloží si ho do cache. `book.author = anna` uloží objekt
  a zároveň nastaví `book.author_id`. Opačná strana vazby
  (`author.book_set`) je zase deskriptor, který vrací manager.
- `Book.objects` je deskriptor `ManagerDescriptor`. Přes instanci
  záměrně vyhodí `AttributeError: Manager isn't accessible via Book instances`.

Shrnutí: v těle modelu píšeš **pole** (popis sloupců). Django z nich
při vytváření třídy udělá deskriptory na třídě a metadata v `_meta`.
Hodnoty jednotlivých záznamů jsou v `__dict__` instancí. Jak přesně
vytváření třídy probíhá, je v
[`CLASS_CREATION_AND_METACLASSES.md`](CLASS_CREATION_AND_METACLASSES.md).

## 11. Časté chyby

| Příznak | Příčina |
|---|---|
| deskriptor nic nedělá, vrací se objekt deskriptoru | je uložený v instanci (`self.x = Desc()`), ne jako atribut třídy |
| všechny instance mají stejnou hodnotu | deskriptor ukládá do sebe (`self.value`), ne do `obj.__dict__` |
| `RecursionError` v `__set__` | `setattr(obj, self.name, value)` znovu zavolá `__set__`, piš do `obj.__dict__[self.name]` |
| `KeyError` při čtení | hodnota ještě nebyla nastavena, doplň výchozí hodnotu (`obj.__dict__.get(self.name, self.default)`) |
| `AttributeError: 'X' object has no attribute 'name'` uvnitř deskriptoru | chybí `__set_name__`, nebo deskriptor nevznikl v těle třídy (přidaný později přes `setattr` → `__set_name__` se nezavolá) |
| `Class.attr` spadne na `AttributeError` / `TypeError` | `__get__` neřeší `obj is None` |
| vlastní cache se přepočítává pokaždé | deskriptor má `__set__`, je data deskriptor a vyhraje nad `__dict__` |
