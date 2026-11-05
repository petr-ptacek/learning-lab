# 08 — OOP: dědičnost a jak Django skládá třídy

## Cíl

Pochopit, jak třídy **stavějí na jiných třídách**: dědičnost,
`super()`, abstraktní základ, mixiny a pořadí hledání metod (MRO).
A pak to hlavní pro Django: co se děje **při vytvoření třídy**, jak
`class Meta` funguje jako konfigurace a jak model „posbírá“ svá pole
(`__init_subclass__`, deskriptory, metatřída).

Na čem to stavíš: všechno z
[`07-oop-zaklady`](../07-oop-zaklady/THEORY.md), hlavně hledání
atributů instance → třída, atributy třídy, `cls` v classmethod
a dunder metody.

K čemu to bude: každý Django model dědí z `models.Model`, každá
class-based view z `View` a mixinů (`LoginRequiredMixin, ListView`),
formuláře z `forms.Form` / `ModelForm`. Po tomhle konceptu budeš
rozumět, proč stačí napsat `title = models.CharField(...)` a
`class Meta: ordering = [...]` a zbytek se „udělá sám“.

JS obdoba: `class B extends A`, `super()`. Vícenásobnou dědičnost
a metatřídy JS nemá.

Do hloubky (výtah z článků v `RESOURCES.md`):

- [`../docs/INHERITANCE_AND_SUPER.md`](../docs/INHERITANCE_AND_SUPER.md):
  dědičnost, přepsání metody, `super()`, atributy třídy jako
  konfigurace, `isinstance`, kompozice vs. dědičnost
- [`../docs/MULTIPLE_INHERITANCE_AND_MIXINS.md`](../docs/MULTIPLE_INHERITANCE_AND_MIXINS.md):
  MRO, diamant, kooperativní `super()`, mixiny v Django views
- [`../docs/ABSTRACT_BASE_CLASSES.md`](../docs/ABSTRACT_BASE_CLASSES.md):
  `ABC`, `@abstractmethod`, template method, `collections.abc`
- [`../docs/DESCRIPTORS.md`](../docs/DESCRIPTORS.md): `__get__` /
  `__set__` / `__set_name__`, co je ve skutečnosti `property` a pole
  Django modelu
- [`../docs/CLASS_CREATION_AND_METACLASSES.md`](../docs/CLASS_CREATION_AND_METACLASSES.md):
  jak vzniká třída, `__init_subclass__`, metatřídy, jak vzniká Django
  model
- [`../docs/ENUMS.md`](../docs/ENUMS.md): `Enum`, `IntEnum` /
  `StrEnum`, metody na enumu, hodnota s popiskem, Django
  `TextChoices`

## Dědičnost

```python
class Employee:
    role = "zaměstnanec"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} – {self.role}"


class Developer(Employee):              # Developer DĚDÍ z Employee
    role = "vývojář"                    # přepíše atribut třídy


dev = Developer("Anna", 80_000)         # __init__ zdědil
dev.describe()                          # 'Anna – vývojář'
```

Hledání atributu z `07` se jen prodlouží: **instance → třída →
rodiče → … → `object`**. `dev.describe` Python nenajde v instanci ani
v `Developer`, najde ho v `Employee`. Uvnitř `describe` ale `self.role`
začne hledat znovu od instance, takže najde `"vývojář"` z `Developer`.
Na tom stojí celé Django: základní třída napíše logiku, podtřída jen
přepíše atributy (`template_name`, `paginate_by`, `model`).

```python
isinstance(dev, Employee)               # True: dev JE i Employee
issubclass(Developer, Employee)         # True
type(dev) is Employee                   # False: přesný typ je Developer
Developer.__mro__                       # pořadí hledání
# (<class '__main__.Developer'>, <class '__main__.Employee'>, <class 'object'>)
```

## `super()`: rozšíř, nepřepisuj

Když podtřída metodu napíše znovu, rodičovská verze se nezavolá.
`super()` ji zavolá, takže můžeš chování **rozšířit**:

```python
class Manager(Employee):
    role = "manažer"

    def __init__(self, name, salary, reports=()):
        super().__init__(name, salary)  # nastaví name a salary jako rodič
        self.reports = list(reports)    # a přidá vlastní atribut

    def describe(self):
        return f"{super().describe()} ({len(self.reports)} podřízených)"


boss = Manager("Eva", 120_000, [dev])
boss.describe()                         # 'Eva – manažer (1 podřízených)'
```

Nejčastější chyba: vlastní `__init__` bez `super().__init__(...)`.
Rodič pak nenastaví své atributy a první `self.name` spadne na
`AttributeError`. V Djangu stejně: přepsaný `save()` nebo
`get_context_data()` musí zavolat `super()`, jinak se neuloží nebo
nenaplní kontext.

## Abstraktní základ

Třída, která říká „každý potomek musí umět tohle“, ale sama to
neimplementuje:

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self): ...

    def describe(self):                 # konkrétní metoda využívá abstraktní
        return f"{type(self).__name__}: {self.area():.2f}"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side**2


Square(3).describe()                    # 'Square: 9.00'
```

`Shape()` vyhodí `TypeError: Can't instantiate abstract class Shape
without an implementation for abstract method 'area'`. Vzor „základ
napíše postup a volá metody, které doplní potomek“ se jmenuje
**template method**. Přesně tak fungují Django class-based views:
`ListView` napíše celý průběh requestu a ty přepíšeš
`get_queryset()` nebo `get_context_data()`.

`collections.abc` nabízí hotové abstraktní základy. Když napíšeš
`class Playlist(Sequence)` a doplníš jen `__getitem__` a `__len__`,
dostaneš zdarma `in`, `for`, `reversed`, `index` a `count`.

## Vícenásobná dědičnost, MRO a mixiny

Třída může mít víc rodičů. Pořadí, ve kterém je Python prohledává, je
**MRO** (*method resolution order*), vidíš ho v `Třída.__mro__`.
`super()` neznamená „rodič“, ale **další třída v MRO**. Díky tomu se
dá řetězit:

```python
class View:
    def dispatch(self, request):
        return "200 OK"


class LoginRequiredMixin:
    def dispatch(self, request):
        if not request.get("user"):
            return "302 /login/"
        return super().dispatch(request)  # další v MRO, tady View


class Dashboard(LoginRequiredMixin, View):
    pass


Dashboard().dispatch({"user": "anna"})  # '200 OK'
Dashboard().dispatch({})                # '302 /login/'
[cls.__name__ for cls in Dashboard.__mro__]
# ['Dashboard', 'LoginRequiredMixin', 'View', 'object']
```

**Mixin** je malá třída s jednou schopností, která se sama nepoužívá,
jen se přimíchá k jiné. Píše se **vlevo** od základní třídy, aby
dostala slovo dřív. Proto v Djangu `class MyView(LoginRequiredMixin,
ListView)`, a ne obráceně.

## `class Meta`: konfigurace ve vnořené třídě

Z `07` víš, že vnořená třída je jen atribut třídy. Základní třída si ji
může přečíst a podle ní se chovat:

```python
class Model:
    @classmethod
    def get_option(cls, name, default=None):
        meta = getattr(cls, "Meta", None)
        return getattr(meta, name, default)


class Book(Model):
    class Meta:
        ordering = ["title"]
        verbose_name = "kniha"


class Author(Model):
    pass


Book.get_option("ordering")             # ['title']
Author.get_option("ordering", [])       # []
```

Pozor na dědění: `Meta` se hledá jako každý jiný atribut, takže
podtřída bez vlastní `Meta` „vidí“ rodičovu. Když si napíše vlastní,
rodičovu celou zastíní. Proto se v Djangu u abstraktních modelů píše
`class Meta(Base.Meta):`. Django má pro dědění `Meta` vlastní
pravidla, rozebírá je
[`CLASS_CREATION_AND_METACLASSES.md`](../docs/CLASS_CREATION_AND_METACLASSES.md).

## Co se děje při `class X(...)`

1. Python spustí tělo třídy a všechno, co se v něm přiřadí, uloží do
   slovníku (`title = ...`, `def __str__`, `class Meta`).
2. Zavolá **metatřídu** (výchozí je `type`): `type("Book", (Model,),
   slovník)`. Ta vyrobí objekt třídy.
3. Každému atributu, který má `__set_name__`, řekne jeho jméno.
4. Zavolá `__init_subclass__` rodiče. Tady může základní třída
   **zareagovat na každou novou podtřídu**: zaregistrovat ji, posbírat
   její pole, přidat jí atributy.

```python
class Plugin:
    registry = {}

    def __init_subclass__(cls, *, name, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[name] = cls


class CsvExport(Plugin, name="csv"):
    pass


Plugin.registry                         # {'csv': <class '__main__.CsvExport'>}
```

Django dělá totéž, jen přes vlastní metatřídu `ModelBase`: při
vytvoření třídy modelu projde atributy, pole (`CharField`, …) si
zaregistruje, z `Meta` vyrobí `Book._meta` a přidá `objects`.

## Deskriptory: co je ve skutečnosti pole modelu

Atribut třídy, který má metody `__get__` / `__set__`, převezme čtení
a zápis toho jména na instanci. `property` je deskriptor a pole
Django modelu se chovají stejně:

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name                  # Python sem pošle jméno atributu

    def __get__(self, obj, objtype=None):
        if obj is None:                   # čtení přes třídu: Product.price
            return self
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} nesmí být záporné")
        obj.__dict__[self.name] = value


class Product:
    price = PositiveNumber()              # jedna validace, použitelná všude
    quantity = PositiveNumber()

    def __init__(self, price, quantity):
        self.price = price                # jde přes __set__
        self.quantity = quantity


p = Product(24.9, 10)
p.price                                   # 24.9
vars(p)                                   # {'price': 24.9, 'quantity': 10}
```

`p.price = -1` vyhodí `ValueError: price nesmí být záporné`. Proto
`title = models.CharField(...)` je atribut **třídy**, a přesto má
každá kniha vlastní `book.title`.

## `Enum`: pevná sada hodnot

Když má hodnota jen pár přípustných možností (stav objednávky,
priorita), patří do enumu místo stringů:

```python
from enum import Enum, StrEnum


class Status(Enum):
    NEW = "new"
    PAID = "paid"

    @property
    def is_paid(self):
        return self is Status.PAID


Status.PAID                             # <Status.PAID: 'paid'>
Status("paid") is Status.PAID           # True: hledání podle hodnoty
Status["PAID"].is_paid                  # True: podle jména, metoda na členovi
Status.PAID == "paid"                   # False: obyčejný Enum ≠ hodnota


class Role(StrEnum):                    # dědí i ze str
    ADMIN = "admin"


Role.ADMIN == "admin"                   # True
```

Členy jsou **instance** třídy `Status`, vzniknou jednou při vytvoření
třídy (dělá to metatřída `EnumType`) a nejdou přepsat ani vyrobit
další. Django `models.TextChoices` je `StrEnum` s popiskem pro každý
člen (`DRAFT = "draft", "Koncept"`). Podrobně v
[`ENUMS.md`](../docs/ENUMS.md).

## Kompozice místo dědičnosti

Dědičnost znamená „**je**“: `Developer` je `Employee`. Když platí jen
„**má**“ (knihovna má knihy, objednávka má položky), patří objekt do
atributu, ne mezi rodiče. Hluboké hierarchie dědičnosti se špatně
čtou. Dědí se hlavně z frameworku (`models.Model`, `View`) a mixiny
drž malé.

## Django model očima tohoto konceptu

```python
class TimeStamped(models.Model):        # abstraktní základ
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True                 # Django pro něj nevytvoří tabulku


class Book(TimeStamped):                # dědí pole created
    class Status(models.TextChoices):   # enum: hodnota + popisek
        DRAFT = "draft", "Koncept"
        PUBLISHED = "published", "Publikováno"

    title = models.CharField(max_length=200)   # deskriptor na třídě
    status = models.CharField(max_length=20, choices=Status, default=Status.DRAFT)

    class Meta(TimeStamped.Meta):       # zdědí volby rodičovy Meta
        ordering = ["title"]

    def save(self, *args, **kwargs):    # rozšíření přes super()
        self.title = self.title.strip()
        super().save(*args, **kwargs)


class BookList(LoginRequiredMixin, ListView):   # mixin vlevo, MRO
    model = Book                                # konfigurace atributem třídy
    paginate_by = 20

    def get_queryset(self):                     # template method
        return super().get_queryset().filter(title__icontains="a")
```

## Časté chyby

| Příznak | Příčina |
|---|---|
| `AttributeError: 'Manager' object has no attribute 'name'` | vlastní `__init__` bez `super().__init__(...)` |
| `TypeError: Employee.__init__() missing 1 required positional argument` | `super().__init__()` voláš bez argumentů, které rodič potřebuje |
| přepsaná metoda „nic nedělá“ z rodiče (Django nic neuloží) | chybí `super().save(...)` / `super().get_context_data(...)` |
| `TypeError: Can't instantiate abstract class ...` | podtřída nedoplnila všechny `@abstractmethod` |
| mixin se neuplatní | mixin je v hlavičce **vpravo** od základní třídy |
| `TypeError: Cannot create a consistent method resolution order (MRO)` | rodiče v hlavičce v pořadí, které odporuje jejich vlastní dědičnosti |
| podtřída „ztratila“ `ordering` z rodičovy `Meta` | vlastní `class Meta:` rodičovu celou zastíní, pomůže `class Meta(Parent.Meta):` |
| všechny podtřídy sdílí jeden registr / manager | stav uložený na základní třídě, ne na `cls` |
