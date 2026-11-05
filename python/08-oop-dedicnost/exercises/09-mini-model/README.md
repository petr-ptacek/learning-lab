# 09 — Mini model (závěrečné)

Všechno z konceptu dohromady: napíšeš si zmenšený Django model bez
databáze. Pole jsou deskriptory (`08`), podtřídy polí volají
`super()` (`02`), rodič si při vzniku podtřídy posbírá pole a `Meta`
(`06`, `07`) a každý model dostane vlastní `objects` manager (jako
`Book.objects` z `05-classmethod` v `07-oop-zaklady`).

Až to budeš mít, přečti si znovu
[Django — Models](https://docs.djangoproject.com/en/6.1/topics/db/models/).
Každý řádek modelu už budeš umět vysvětlit.

Teorie: [`docs/CLASS_CREATION_AND_METACLASSES.md`](../../../docs/CLASS_CREATION_AND_METACLASSES.md),
[`docs/DESCRIPTORS.md`](../../../docs/DESCRIPTORS.md),
[`docs/INHERITANCE_AND_SUPER.md`](../../../docs/INHERITANCE_AND_SUPER.md).

## Požadavky

**Pole** (deskriptory):

- `Field(default=NOT_PROVIDED)`, kde `NOT_PROVIDED = object()` je
  sentinel pro „bez výchozí hodnoty“ (`None` může být platný default):
  - `__set_name__`, `__get__` jako ve cvičení 08,
  - `__set__` zavolá `self.validate(value)` a hodnotu uloží do
    `obj.__dict__`,
  - `validate(value)` v základu nedělá nic, podtřídy ho přepíšou.
- `CharField(max_length, **kwargs)`:
  - ne-string → `TypeError(f"{name}: očekávám text, ne {typ}")`,
  - delší → `ValueError(f"{name}: nejvýš {max_length} znaků")`.
- `IntegerField(min_value=None, **kwargs)`:
  - ne-`int` → `TypeError(f"{name}: očekávám celé číslo, ne {typ}")`,
  - pod `min_value` → `ValueError(f"{name}: nejméně {min_value}")`.
- `BooleanField(default=False)`: ne-`bool` →
  `TypeError(f"{name}: očekávám bool, ne {typ}")`.
- Podtřídy polí předávají `default` dál přes `super().__init__(**kwargs)`.

**Model**:

- `__init_subclass__`:
  - posbírá pole do `cls._fields`, i zděděná, pole rodičů první
    (cvičení 07),
  - z **vlastní** `Meta` třídy (`vars(cls).get("Meta")`) přečte
    `ordering` (výchozí `[]`) a `verbose_name` (výchozí jméno třídy
    malými) do `cls._ordering` a `cls._verbose_name`,
  - nastaví `cls.objects = Manager(cls)`. **Každá** podtřída má
    vlastní manager, ne jeden sdílený.
- `__init__(self, **values)`:
  - neznámé pole → `TypeError(f"{Třída}: neznámé pole {jména}")`,
  - chybějící pole bez defaultu →
    `TypeError(f"{Třída}: chybí povinné pole {jméno}")`,
  - jinak nastaví hodnotu nebo default. Validace proběhne sama přes
    deskriptor.
- `__repr__` → `Book(title='Proces', author='Kafka', year=1925, available=True)`.
- `__eq__`: stejná třída a stejné hodnoty. Pro jinou třídu
  `NotImplemented`.
- `@classmethod sort(cls, items)` podle `cls._ordering`, jako ve
  cvičení 06.

**Manager(model)**:

- `create(**values)` — vytvoří instanci, uloží ji a vrátí,
- `all()` — všechny instance seřazené podle `Meta.ordering`,
- `filter(**conditions)` — seřazené instance, které splňují všechny
  podmínky (`==`),
- `get(**conditions)` — právě jednu, jinak
  `LookupError(f"{Model}: nalezeno {n} záznamů, čekám 1")`,
- `count()`.

```python
class Book(Model):
    title = CharField(max_length=50)
    author = CharField(max_length=30)
    year = IntegerField(min_value=0)
    available = BooleanField(default=True)

    class Meta:
        ordering = ["author", "-year"]
        verbose_name = "kniha"


class Author(Model):
    name = CharField(max_length=30)


class Ebook(Book):
    url = CharField(max_length=100, default="")


Book.objects.create(title="Proces", author="Kafka", year=1925)
Book.objects.create(title="Švejk", author="Hašek", year=1923)
Book.objects.create(title="Zámek", author="Kafka", year=1926, available=False)
Book.objects.create(title="Saturnin", author="Jirotka", year=1942)
Author.objects.create(name="Kafka")
```

**Předpověď:** kolik záznamů má `Author.objects` a `Ebook.objects`?
Jaké `ordering` má `Ebook`? Proč `Book.objects.create(...)` a ne
`Book.create(...)`?

### Příklady vstup/výstup

| Kód                                                | Výsledek                                                  |
|----------------------------------------------------|-----------------------------------------------------------|
| `list(Book._fields)`                               | `['title', 'author', 'year', 'available']`                |
| `Book._verbose_name, Book._ordering`               | `('kniha', ['author', '-year'])`                          |
| `Book.objects.count()`                             | `4`                                                       |
| `[b.title for b in Book.objects.all()]`            | `['Švejk', 'Saturnin', 'Zámek', 'Proces']`                |
| `Book.objects.filter(author="Kafka", available=True)` | `[Book(title='Proces', author='Kafka', year=1925, available=True)]` |
| `Book.objects.filter(author="Čapek")`              | `[]`                                                      |
| `Book.objects.get(title="Švejk")`                  | `Book(title='Švejk', author='Hašek', year=1923, available=True)` |
| `Book.objects.get(author="Kafka")`                 | `LookupError: Book: nalezeno 2 záznamů, čekám 1`          |
| `Book.objects.get(author="Čapek")`                 | `LookupError: Book: nalezeno 0 záznamů, čekám 1`          |
| `Book(title="X", author="Y", year=1)`, pak `Book.objects.count()` | `4` (bez `create` se neuloží)              |
| `Book(title="X", author="Y", year=1) == Book(title="X", author="Y", year=1)` | `True`                          |
| `Author.objects.count(), Author.objects is Book.objects` | `(1, False)`                                        |
| `Author._verbose_name, Author._ordering`           | `('author', [])`                                          |
| `list(Ebook._fields)`                              | `['title', 'author', 'year', 'available', 'url']`         |
| `Ebook.objects.count(), Ebook._ordering`           | `(0, [])` (vlastní manager, `Meta` se nedědí)             |
| `Ebook(title="A", author="B", year=2000)`          | `Ebook(title='A', author='B', year=2000, available=True, url='')` |
| `Book(title="X", author="Y", year=1) == Ebook(title="X", author="Y", year=1)` | `False`                        |
| `hasattr(Model, "objects")`                        | `False`                                                   |

| Kód                                                | Výsledek                                                  |
|----------------------------------------------------|-----------------------------------------------------------|
| `Book(title="X", author="Y")`                      | `TypeError: Book: chybí povinné pole year`                |
| `Book(title="X", author="Y", year=1, pages=100)`   | `TypeError: Book: neznámé pole pages`                     |
| `Book(title="X", author="Y", year=-5)`             | `ValueError: year: nejméně 0`                             |
| `Book(title="X", author="Y", year="1920")`         | `TypeError: year: očekávám celé číslo, ne str`            |
| `Book(title="X" * 60, author="Y", year=1)`         | `ValueError: title: nejvýš 50 znaků`                      |
| `Book(title="X", author="Y", year=1, available="ano")` | `TypeError: available: očekávám bool, ne str`         |

## Bonus

Django to celé nedělá přes `__init_subclass__`, ale přes **metatřídu**
`ModelBase`. Vyzkoušej si obě cesty a porovnej je.

- Přepiš sběr polí a `Meta` do metatřídy
  `class ModelBase(type)` s `__new__(mcls, name, bases, namespace, **kwargs)`
  a použij ji: `class Model(metaclass=ModelBase)`. Samotný `Model`
  (nemá žádného rodiče typu `ModelBase`) nech beze změny.
- `Meta.abstract = True`: abstraktní model nedostane `objects`
  a jeho instance vyhodí `TypeError(f"{Třída} je abstraktní model")`.
  Jeho pole se ale dědí.
- Lookupy ve `filter` jako v Djangu: `pole__gt`, `__gte`, `__lt`,
  `__contains`, `__exact` (a bez přípony totéž co `exact`). Neznámý
  lookup → `ValueError(f"Neznámý lookup: {lookup}")`. Nápověda:
  `str.partition("__")` a dict lookup → funkce.

```python
class TimestampedModel(Model):
    created = IntegerField(default=0)

    class Meta:
        abstract = True


class Book(TimestampedModel):
    title = CharField(max_length=50)
    author = CharField(max_length=30)
    year = IntegerField(min_value=0)

    class Meta:
        ordering = ["year"]
```

(se stejnými čtyřmi knihami, bez `available`)

### Příklady vstup/výstup (bonus)

| Kód                                                       | Výsledek                                      |
|-----------------------------------------------------------|-----------------------------------------------|
| `type(Book).__name__, type(Model).__name__`               | `('ModelBase', 'ModelBase')`                  |
| `list(Book._fields)`                                      | `['created', 'title', 'author', 'year']`      |
| `hasattr(TimestampedModel, "objects"), hasattr(Book, "objects")` | `(False, True)`                        |
| `TimestampedModel(created=1)`                             | `TypeError: TimestampedModel je abstraktní model` |
| `[b.title for b in Book.objects.filter(year__gte=1925)]`  | `['Proces', 'Zámek', 'Saturnin']`             |
| `[b.title for b in Book.objects.filter(year__gt=1925, author="Kafka")]` | `['Zámek']`                     |
| `[b.title for b in Book.objects.filter(title__contains="r")]` | `['Proces', 'Saturnin']`                  |
| `[b.title for b in Book.objects.filter(year__lt=1900)]`   | `[]`                                          |
| `[b.title for b in Book.objects.filter(author__exact="Kafka")]` | `['Proces', 'Zámek']`                   |
| `Book.objects.filter(year__between=1)`                    | `ValueError: Neznámý lookup: between`         |
