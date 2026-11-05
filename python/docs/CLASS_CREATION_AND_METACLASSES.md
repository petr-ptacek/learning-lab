# Vytvoření třídy, `__init_subclass__` a metatřídy

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(oficiální *Data model — Customizing class creation*, PEP 487 a Real
Python *Python Metaclasses*). Přehled je v
[`THEORY.md`](../08-oop-dedicnost/THEORY.md).

Tohle je poslední díl skládačky „jak Django model funguje uvnitř“. Na
konci budeš vědět, co se stane mezi napsáním `class Book(models.Model):`
a chvílí, kdy existuje `Book.objects`, `Book._meta`
i `Book.DoesNotExist`.

Navazuje na „třída je taky objekt“ v
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md#8-třída-je-taky-objekt),
na deskriptory v [`DESCRIPTORS.md`](DESCRIPTORS.md) a na dědičnost
v [`INHERITANCE_AND_SUPER.md`](INHERITANCE_AND_SUPER.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Třídu vyrábí `type`](#1-třídu-vyrábí-type)
2. [Co se děje při `class X(Base):`](#2-co-se-děje-při-class-xbase)
3. [`__init_subclass__`: háček pro podtřídy](#3-__init_subclass__-háček-pro-podtřídy)
4. [Argumenty v hlavičce třídy](#4-argumenty-v-hlavičce-třídy)
5. [Sběr polí: předobraz Django modelu](#5-sběr-polí-předobraz-django-modelu)
6. [Metatřída](#6-metatřída)
7. [Kdy metatřídu, kdy `__init_subclass__`, kdy dekorátor](#7-kdy-metatřídu-kdy-__init_subclass__-kdy-dekorátor)
8. [Jak vzniká Django model](#8-jak-vzniká-django-model)
9. [Dědění `Meta` v Djangu](#9-dědění-meta-v-djangu)
10. [Mini ORM na jedné obrazovce](#10-mini-orm-na-jedné-obrazovce)
11. [Časté chyby](#11-časté-chyby)

---

## 1. Třídu vyrábí `type`

Instance vyrábí třída: `Book(...)`. Kdo vyrábí třídy? Taky třída,
a to `type`. Třída tříd se jmenuje **metatřída**.

```python
class Book:
    pass


type(Book())                     # <class '__main__.Book'>
type(Book)                       # <class 'type'>
type(type)                       # <class 'type'>
isinstance(Book, type)           # True
```

`type` se dá zavolat i přímo se třemi argumenty: jméno, rodiče a
slovník atributů. Výsledek je stejný jako zápis `class`:

```python
def describe(self):
    return f"{self.title} ({self.year})"


Movie = type("Movie", (), {"year": 2000, "describe": describe})
m = Movie()
m.title = "Matrix"
m.describe()                     # 'Matrix (2000)'
Movie.__name__                   # 'Movie'
```

Příkaz `class` je tedy jen pohodlný zápis pro „sestav slovník atributů
a zavolej metatřídu“.

## 2. Co se děje při `class X(Base):`

Pořadí kroků (ověřené výpisy z jednotlivých háčků):

1. Python určí **metatřídu**, výchozí je `type` (nebo metatřída rodiče).
2. `metatřída.__prepare__(name, bases)` vrátí prázdný jmenný prostor
   (obvykle obyčejný dict).
3. **Tělo třídy** se spustí v tom jmenném prostoru. Každé přiřazení
   a `def` do něj zapíše jméno.
4. Zavolá se `metatřída(name, bases, namespace, **kwargs)`:
   1. `metatřída.__new__` vytvoří objekt třídy (`type.__new__`),
   2. uvnitř `type.__new__` se na každém atributu, který to umí,
      zavolá **`__set_name__(owner, name)`**,
   3. pak se zavolá **`__init_subclass__`** rodiče (přesněji první
      takové metody v MRO),
   4. `metatřída.__init__`.
5. Výsledná třída se přiřadí jménu `X`.

```python
class Log:
    def __set_name__(self, owner, name):
        print("__set_name__", name)


class Base:
    def __init_subclass__(cls, **kwargs):
        print("__init_subclass__", cls.__name__)
        super().__init_subclass__(**kwargs)


class Child(Base):
    print("tělo třídy")
    x = Log()
# vypíše: tělo třídy
#         __set_name__ x
#         __init_subclass__ Child
```

Důsledek pro Django: v okamžiku, kdy háček běží, je tělo modelu
hotové. Všechna pole i `class Meta` už leží ve jmenném prostoru
a dají se projít.

## 3. `__init_subclass__`: háček pro podtřídy

`__init_subclass__` definovaný v základu se zavolá **pokaždé, když
vznikne podtřída**. Pro základ samotný ne. Je to automaticky
classmethod: `cls` je nově vytvořená podtřída. Přidal ho Python 3.6
(PEP 487) právě proto, aby běžné úlohy nevyžadovaly metatřídu.

Typické použití je **registr**: základ si pamatuje všechny podtřídy.

```python
class Plugin:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry.append(cls)


class Csv(Plugin):
    pass


class Json(Plugin):
    pass


[c.__name__ for c in Plugin.registry]   # ['Csv', 'Json']
```

Pozor na `Plugin.registry` místo `cls.registry`: zápis přes `cls`
by se při `append` choval stejně (seznam je jeden, sdílený), ale u
přiřazení (`cls.registry = ...`) bys vytvořil atribut na podtřídě.

Druhé typické použití je **kontrola podtřídy už při definici**:

```python
class Command:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "help"):
            raise TypeError(f"{cls.__name__} musí mít atribut help")


class Migrate(Command):
    help = "Spustí migrace"


class Broken(Command):           # TypeError: Broken musí mít atribut help
    pass
```

Chyba vznikne už při **importu** souboru, ne až když někdo příkaz
spustí.

## 4. Argumenty v hlavičce třídy

Pojmenované argumenty za rodiči (`class X(Base, key=value)`) Python
předá do `__init_subclass__`. Konfigurace podtřídy se tak dá zapsat
přímo do hlavičky:

```python
class Exporter:
    registry = {}

    def __init_subclass__(cls, *, format, **kwargs):
        super().__init_subclass__(**kwargs)
        if format in Exporter.registry:
            raise ValueError(f"Formát {format!r} už je registrovaný")
        cls.format = format
        Exporter.registry[format] = cls


class CsvExporter(Exporter, format="csv"):
    pass


CsvExporter.format                       # 'csv'
Exporter.registry["csv"]                 # <class '__main__.CsvExporter'>


class Bad(Exporter):                     # TypeError: Exporter.__init_subclass__() missing 1 required keyword-only argument: 'format'
    pass
```

- `*` v signatuře dělá z `format` povinný pojmenovaný argument.
- `**kwargs` a `super().__init_subclass__(**kwargs)` posílají zbylé
  argumenty dál po MRO. To je důležité, když se potká víc základů nebo
  mixinů s vlastním `__init_subclass__` (kooperativní `super()`, viz
  [`MULTIPLE_INHERITANCE_AND_MIXINS.md`](MULTIPLE_INHERITANCE_AND_MIXINS.md)).
- Kdyby nikdo argument nespotřeboval, skončí u `object.__init_subclass__`,
  který žádné argumenty nebere:

```python
class Plain:
    pass


class Colored(Plain, color="red"):       # TypeError: Colored.__init_subclass__() takes no keyword arguments
    pass
```

## 5. Sběr polí: předobraz Django modelu

`__init_subclass__` může projít atributy nové třídy a vybrat si ty,
které jsou „pole“. Totéž dělá Django s `models.CharField`:

```python
class Field:
    def __init__(self, default=None):
        self.default = default


class Schema:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = {}
        for klass in reversed(cls.__mro__):          # rodiče první, ať se dědí
            for name, value in vars(klass).items():
                if isinstance(value, Field):
                    fields[name] = value
        cls._fields = fields

    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            setattr(self, name, kwargs.pop(name, field.default))
        if kwargs:
            raise TypeError(f"Neznámé pole: {', '.join(kwargs)}")

    def __repr__(self):
        args = ", ".join(f"{n}={getattr(self, n)!r}" for n in self._fields)
        return f"{type(self).__name__}({args})"


class Timestamped(Schema):
    created = Field(default="dnes")


class Article(Timestamped):
    title = Field()
    published = Field(default=False)


list(Article._fields)                    # ['created', 'title', 'published']
Article(title="Ahoj")                    # Article(created='dnes', title='Ahoj', published=False)
Article(titel="Ahoj")                    # TypeError: Neznámé pole: titel
```

`vars(klass)` vrací jen **vlastní** atributy dané třídy, ne zděděné
(rozdíl oproti `getattr`, viz
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md)). Proto se
prochází MRO od nejvzdálenějšího předka, aby pole podtřídy přepsala
pole rodiče a pořadí začínalo poli rodičů.

## 6. Metatřída

Metatřída je podtřída `type`. Její `__new__` dostane jméno, rodiče a
**jmenný prostor ještě před vytvořením třídy**. Může ho tedy změnit:
něco odebrat, přidat nebo přejmenovat.

```python
class ModelBase(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        meta = namespace.pop("Meta", None)          # Meta se na třídu nedostane
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        cls._options = {
            "ordering": getattr(meta, "ordering", []),
            "verbose_name": getattr(meta, "verbose_name", name.lower()),
        }
        return cls


class Model(metaclass=ModelBase):
    pass


class Book(Model):
    class Meta:
        ordering = ["title"]


Book._options                            # {'ordering': ['title'], 'verbose_name': 'book'}
hasattr(Book, "Meta")                    # False
type(Book).__name__                      # 'ModelBase'
```

- Metatřída se **dědí**: `Book` nemá `metaclass=` v hlavičce, a přesto
  ji vyrobil `ModelBase`, protože ho má rodič `Model`.
- Konvence jmen: `mcls` (nebo `metacls`) je metatřída, `cls` vyrobená
  třída.
- Metody metatřídy jsou metody **třídy**, ne instancí. Díky tomu by
  šlo napsat například `__iter__` v metatřídě, aby fungovalo
  `for book in Book:`.

Dvě různé metatřídy rodičů, které nejsou ve vztahu rodič–potomek,
Python neumí spojit:

```python
class MetaA(type):
    pass


class MetaB(type):
    pass


class A(metaclass=MetaA):
    pass


class B(metaclass=MetaB):
    pass


class C(A, B):                           # TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
    pass
```

## 7. Kdy metatřídu, kdy `__init_subclass__`, kdy dekorátor

| Potřebuješ | Nástroj |
|---|---|
| reagovat na vznik podtřídy (registr, kontrola, sběr atributů) | `__init_subclass__` |
| upravit jednu konkrétní třídu (přidat metody) | dekorátor třídy, např. `@dataclass` |
| změnit jmenný prostor **před** vytvořením třídy (odebrat `Meta`, vlastní `__prepare__`) | metatřída |
| chování samotné třídy jako objektu (`len(Book)`, `Book[1]`) | metatřída |

Známý výrok Tima Peterse: metatřídy jsou hlubší magie, než o jakou se
99 % uživatelů má kdy starat. Kdo se ptá, jestli je potřebuje,
nepotřebuje je. V aplikačním kódu je skoro nenapíšeš. Potkáš je ale
v Djangu (`ModelBase`, `DeclarativeFieldsMetaclass` u formulářů),
v `abc` (`ABCMeta`) a v `enum` (`EnumType`).

Dekorátor třídy je jen funkce, která třídu dostane a vrátí:

```python
def register(cls):
    cls.registered = True
    return cls


@register
class Report:
    pass


Report.registered                        # True
```

Obdoba v TS jsou dekorátory tříd (`@Component`) nebo funkce, která
třídu obalí. Python má navíc metatřídy a `__init_subclass__`, které
se uplatní **automaticky pro všechny podtřídy**, bez psaní dekorátoru
nad každou.

## 8. Jak vzniká Django model

Django `Model` má metatřídu `ModelBase` (`django/db/models/base.py`).
Když napíšeš:

```python
# Django (ilustrace, nespouští se)
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     year = models.IntegerField()
#
#     class Meta:
#         ordering = ["title"]
```

`ModelBase.__new__` zhruba udělá tohle (Django 6.x):

1. Pro samotné `Model` neudělá nic zvláštního. Celá logika běží jen
   pro jeho podtřídy.
2. Z jmenného prostoru **vyjme** `Meta`
   (`attr_meta = attrs.pop("Meta", None)`).
3. Atributy rozdělí na ty, které mají metodu `contribute_to_class`
   (pole, managery), a ostatní. Ostatní (metody, konstanty) předá
   `type.__new__`, který vytvoří třídu.
4. Určí `meta = attr_meta or getattr(new_class, "Meta", None)`. Když
   vlastní `Meta` chybí, vezme se zděděná přes běžné hledání atributu
   (viz sekce 9).
5. Vytvoří `Options(meta, app_label)` a uloží ho jako **`Book._meta`**.
   `Options` přečte známé volby (`ordering`, `verbose_name`,
   `db_table` …) a doplní výchozí hodnoty, například `verbose_name`
   z názvu třídy (`BookReview` → `"book review"`). Neznámý atribut
   v `Meta` skončí chybou `TypeError: 'class Meta' got invalid attribute(s): ...`.
6. Pro neabstraktní model vytvoří výjimky **`Book.DoesNotExist`**
   a **`Book.MultipleObjectsReturned`** jako podtřídy výjimek rodičů.
7. Na každém poli zavolá `contribute_to_class(Book, "title")`. Pole se
   tím dozví své jméno, zapíše se do `_meta` a na třídu dosadí
   deskriptor (viz [`DESCRIPTORS.md`](DESCRIPTORS.md#10-deskriptory-v-djangu)).
8. Zpracuje rodiče: pole z abstraktních rodičů zkopíruje, pro
   konkrétního rodiče vytvoří vazbu (`book_ptr`, víctabulková dědičnost).
9. Abstraktní model tady skončí. Neabstraktní pokračuje v `_prepare()`:
   když model nemá žádný manager, přidá **`objects = Manager()`**.
   Nakonec model zaregistruje do registru aplikací (`apps`).

Proto můžeš psát `Book.objects.filter(...)`, i když jsi `objects` nikde
nedefinoval, a proto `Book._meta.get_field("title")` vrátí objekt pole.

Formuláře fungují stejně: `forms.Form` má metatřídu
`DeclarativeFieldsMetaclass`, která posbírá pole z těla třídy do
`base_fields`.

## 9. Dědění `Meta` v Djangu

Obyčejný Python by `Meta` dědil prostě hledáním atributu: podtřída bez
vlastní `Meta` najde rodičovu. Django to upravuje podle druhu rodiče:

| Rodič | Co podtřída bez vlastní `Meta` dostane |
|---|---|
| **abstraktní** (`abstract = True`) | rodičovu `Meta`. Django ji po vytvoření rodiče vrátí na třídu a nastaví v ní `abstract = False`, takže podtřída abstraktní není |
| **konkrétní** (víctabulková dědičnost) | rodičova `Meta` byla vyjmutá a na třídu se nevrátí. Z rodiče se zdědí jen `ordering` a `get_latest_by` |

Chceš-li `Meta` abstraktního rodiče **rozšířit**, dědíš ji výslovně:

```python
# Django (ilustrace, nespouští se)
# class Timestamped(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         abstract = True
#         ordering = ["-created"]
#
#
# class Article(Timestamped):
#     title = models.CharField(max_length=200)
#
#     class Meta(Timestamped.Meta):        # zdědí ordering
#         verbose_name = "článek"
```

Bez `(Timestamped.Meta)` by vlastní `Meta` podtřídy rodičovu zcela
nahradila a `ordering` by se ztratil. Obyčejné třídy v Pythonu se
chovají stejně. Vyzkoušíš si to ve cvičení `06-meta-a-konfigurace`.

## 10. Mini ORM na jedné obrazovce

Všechno dohromady: pole jako deskriptory, `__init_subclass__` posbírá
pole, přečte `Meta` a každé podtřídě dá **vlastní** manager.

```python
class Field:
    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value


class Manager:
    def __init__(self, model):
        self.model = model
        self._rows = []

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self._rows.append(obj)
        return obj

    def all(self):
        keys = self.model._meta["ordering"]
        return sorted(self._rows, key=lambda o: [getattr(o, k) for k in keys])


class Model:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        meta = getattr(cls, "Meta", None)
        cls._meta = {"ordering": getattr(meta, "ordering", [])}
        cls._fields = [
            name for klass in reversed(cls.__mro__)
            for name, value in vars(klass).items() if isinstance(value, Field)
        ]
        cls.objects = Manager(cls)       # každá podtřída svůj, ne sdílený

    def __init__(self, **kwargs):
        for name in self._fields:
            if name in kwargs:
                setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError(f"Neznámé pole: {', '.join(kwargs)}")

    def __repr__(self):
        args = ", ".join(f"{n}={getattr(self, n)!r}" for n in self._fields)
        return f"{type(self).__name__}({args})"


class Book(Model):
    title = Field()
    year = Field(default=0)

    class Meta:
        ordering = ["year"]


class Author(Model):
    name = Field()


Book.objects.create(title="Krakatit", year=1924)
Book.objects.create(title="R.U.R.", year=1920)
Author.objects.create(name="Čapek")
Book.objects.all()                       # [Book(title='R.U.R.', year=1920), Book(title='Krakatit', year=1924)]
Author.objects.all()                     # [Author(name='Čapek')]
Book.objects is Author.objects           # False
Book.title.name                          # 'title'
```

Proti Djangu chybí databáze, validace, `QuerySet` a spousta detailů.
Kostra je ale stejná: popis na třídě, sběr při vytvoření třídy,
hodnoty v instancích. Rozšířenou verzi si napíšeš ve cvičení
`09-mini-model`.

## 11. Časté chyby

| Příznak | Příčina |
|---|---|
| `TypeError: X.__init_subclass__() takes no keyword arguments` | argument v hlavičce třídy nikdo nespotřeboval, chybí vlastní `__init_subclass__` nebo předávání `**kwargs` |
| `TypeError: Base.__init_subclass__() missing 1 required keyword-only argument: 'format'` | podtřída zapomněla argument v hlavičce (`class A(Base, format="csv")`) |
| háček se nezavolal pro základ | `__init_subclass__` běží jen pro **podtřídy**, ne pro třídu, která ho definuje |
| druhý mixin s `__init_subclass__` se nespustil | chybí `super().__init_subclass__(**kwargs)` |
| všechny modely sdílejí jeden registr | registr nebo manager vytvořený jednou na základu, místo `cls.objects = Manager(cls)` pro každou podtřídu |
| zděděná pole chybí | sběr přes `vars(cls)` vidí jen vlastní atributy, projdi `cls.__mro__` |
| `TypeError: metaclass conflict: ...` | rodiče mají různé nesouvisející metatřídy, např. Django model a `ABC` |
| `TypeError: 'class Meta' got invalid attribute(s): ...` (Django) | překlep v názvu volby v `Meta` |
