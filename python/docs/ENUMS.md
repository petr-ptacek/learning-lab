# Výčtové typy: `enum`

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(hlavně oficiální *Enum HOWTO* a Real Python *Build Enumerations of
Constants With Python's Enum*). Přehled je v
[`THEORY.md`](../08-oop-dedicnost/THEORY.md).

Enum je třída s **pevnou sadou instancí**: stavy objednávky, priority,
role uživatele. V Djangu ho potkáš jako `models.TextChoices`
a `models.IntegerChoices` u každého pole s výběrem hodnot. Je to taky
pěkná ukázka OOP z obou konceptů: členy jsou instance třídy, enum může
mít metody a property a Django `TextChoices` je postavené na dědičnosti
a vlastní metatřídě (viz
[`CLASS_CREATION_AND_METACLASSES.md`](CLASS_CREATION_AND_METACLASSES.md)).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Proč enum, a ne stringy nebo konstanty](#1-proč-enum-a-ne-stringy-nebo-konstanty)
2. [`Enum`: členy jsou instance třídy](#2-enum-členy-jsou-instance-třídy)
3. [Hledání člena: `Color(1)` vs. `Color["RED"]`](#3-hledání-člena-color1-vs-colorred)
4. [Porovnávání: `is`, `==` a řazení](#4-porovnávání-is--a-řazení)
5. [`auto()` a `@unique`](#5-auto-a-unique)
6. [`IntEnum` a `StrEnum`](#6-intenum-a-strenum)
7. [Metody a property na enumu](#7-metody-a-property-na-enumu)
8. [`_missing_`: tolerantní hledání](#8-_missing_-tolerantní-hledání)
9. [Hodnota a popisek: vlastní `__new__`](#9-hodnota-a-popisek-vlastní-__new__)
10. [`Flag`: kombinace příznaků](#10-flag-kombinace-příznaků)
11. [Enum v `match` a v JSON](#11-enum-v-match-a-v-json)
12. [Django: `TextChoices` a `IntegerChoices`](#12-django-textchoices-a-integerchoices)
13. [Srovnání s TS](#13-srovnání-s-ts)
14. [Časté chyby](#14-časté-chyby)

---

## 1. Proč enum, a ne stringy nebo konstanty

Stav objednávky jako obyčejný string:

```python
def can_ship(status):
    return status == "payed"     # překlep, podmínka nikdy neplatí
```

Překlep nikdo neodhalí, seznam povolených hodnot není nikde
pohromadě a editor nenapoví. Konstanty v modulu (`PAID = "paid"`)
pomůžou jen napůl: pořád jsou to obyčejné stringy, nejde je projít
cyklem a funkce dostane jakýkoli string.

Enum dá hodnotám **vlastní typ**:

```python
from enum import Enum


class Status(Enum):
    NEW = "new"
    PAID = "paid"
    SHIPPED = "shipped"


def can_ship(status: Status) -> bool:
    return status is Status.PAID


can_ship(Status.PAID)        # True
[s.value for s in Status]    # ['new', 'paid', 'shipped']
```

Překlep `Status.PAYED` spadne hned na `AttributeError`, všechny
hodnoty jsou na jednom místě a typová anotace říká přesně, co funkce
čeká.

## 2. `Enum`: členy jsou instance třídy

```python
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


Color.RED                    # <Color.RED: 1>
type(Color.RED)              # <enum 'Color'>
isinstance(Color.RED, Color)  # True
Color.RED.name               # 'RED'
Color.RED.value              # 1
str(Color.RED)               # 'Color.RED'
```

Tělo vypadá jako obyčejná třída s atributy třídy (viz
[`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md)). Metatřída
`EnumType` z nich ale při vytvoření třídy udělá **instance** `Color`.
Každá má `.name` (jméno v kódu) a `.value` (hodnotu za rovnítkem).

Třída se chová jako kontejner svých členů:

```python
list(Color)                  # [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]
len(Color)                   # 3
Color.RED in Color           # True
Color.__members__["GREEN"]   # <Color.GREEN: 2>
```

Členy jsou **singletony** (každý existuje jen jednou), jsou
hashovatelné (fungují jako klíče dictu a prvky setu) a nejdou přepsat:

```python
Color.RED is Color(1)        # True
{Color.RED: "stop"}[Color.RED]  # 'stop'
Color.RED = 5                # AttributeError: cannot reassign member 'RED'
```

Instance enumu nevyrobíš přes `Color()`. Jediné instance jsou ty
vyjmenované v těle třídy.

## 3. Hledání člena: `Color(1)` vs. `Color["RED"]`

Dva způsoby, jak se z „venkovní“ hodnoty (formulář, JSON, databáze)
dostat ke členovi:

```python
Color(1)                     # <Color.RED: 1>  — podle HODNOTY
Color["RED"]                 # <Color.RED: 1>  — podle JMÉNA
Color(4)                     # ValueError: 4 is not a valid Color
Color["PINK"]                # KeyError: 'PINK'
```

| Zápis | Hledá podle | Chyba, když neexistuje |
|---|---|---|
| `Color(value)` | `.value` | `ValueError: 4 is not a valid Color` |
| `Color[name]` | `.name` | `KeyError: 'PINK'` |
| `getattr(Color, name)` | `.name` | `AttributeError` |

Od Pythonu 3.12 funguje `in` i pro hodnoty, ne jen pro členy:

```python
1 in Color                   # True
4 in Color                   # False
```

## 4. Porovnávání: `is`, `==` a řazení

Protože jsou členy singletony, porovnávají se idiomaticky přes `is`.
`==` funguje taky. Obyčejný `Enum` se ale **nerovná** své hodnotě:

```python
Color.RED is Color.RED       # True
Color.RED == Color.RED       # True
Color.RED == 1               # False
Color.RED.value == 1         # True
Color.RED < Color.BLUE       # TypeError: '<' not supported between instances of 'Color' and 'Color'
```

To je záměr: `Color.RED` a číslo `1` jsou různé věci. Když chceš
řadit, máš dvě možnosti: řadit podle hodnoty
(`sorted(colors, key=lambda c: c.value)`), nebo použít `IntEnum`
(sekce 6).

## 5. `auto()` a `@unique`

Když na konkrétní hodnotě nezáleží, doplní ji `auto()`. U `Enum`
čísluje od 1:

```python
from enum import auto, unique


class Size(Enum):
    S = auto()
    M = auto()
    L = auto()


[s.value for s in Size]      # [1, 2, 3]
```

Dva členy se stejnou hodnotou nejsou chyba. Druhý se stane
**aliasem** prvního a při iteraci se neobjeví:

```python
class Answer(Enum):
    YES = 1
    Y = 1                    # alias


Answer.Y                     # <Answer.YES: 1>
list(Answer)                 # [<Answer.YES: 1>]
```

Když aliasy nechceš, dekorátor `@unique` je zakáže už při definici:

```python
@unique
class Strict(Enum):
    YES = 1
    Y = 1
# ValueError: duplicate values found in <enum 'Strict'>: Y -> YES
```

## 6. `IntEnum` a `StrEnum`

Někdy se hodí, aby se člen **choval jako** číslo nebo string. Pak
enum zdědí i z `int` / `str`:

```python
from enum import IntEnum, StrEnum


class Priority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


Priority.HIGH > Priority.LOW  # True
Priority.HIGH == 3           # True
sorted([Priority.HIGH, Priority.LOW])  # [<Priority.LOW: 1>, <Priority.HIGH: 3>]
Priority.LOW + 1             # 2
```

```python
class OrderStatus(StrEnum):
    NEW = auto()             # u StrEnum dá auto() jméno malými písmeny
    PAID = auto()


OrderStatus.PAID             # <OrderStatus.PAID: 'paid'>
OrderStatus.PAID == "paid"   # True
f"stav: {OrderStatus.PAID}"  # 'stav: paid'
OrderStatus("paid")          # <OrderStatus.PAID: 'paid'>
OrderStatus.PAID.upper()     # 'PAID'
```

Je to vícenásobná dědičnost z
[`MULTIPLE_INHERITANCE_AND_MIXINS.md`](MULTIPLE_INHERITANCE_AND_MIXINS.md):
`StrEnum` dědí z `str` i z `Enum`, takže člen umí všechno, co string.

| | `Enum` | `IntEnum` / `StrEnum` |
|---|---|---|
| `člen == hodnota` | `False` | `True` |
| řazení `<` | `TypeError` | podle hodnoty |
| `str(člen)` | `'Color.RED'` | `'3'` / `'paid'` |
| JSON | nejde přímo | jde přímo |
| bezpečnost typu | vysoká | nižší: `"paid"` projde všude, kde se čeká `OrderStatus` |

Výhoda `StrEnum`: hladce spolupracuje s kódem a knihovnami, které
čekají stringy (databáze, JSON, šablony). Past: protože se rovná
obyčejnému stringu, ztrácíš část ochrany proti překlepům. Podmínka
`status == "payed"` zase tiše vrátí `False`. Django `TextChoices` je
postavené na `StrEnum` právě kvůli databázi.

## 7. Metody a property na enumu

Enum je třída, takže může mít metody a property. Logika, která patří
k hodnotám, tak bydlí přímo u nich:

```python
class Status(Enum):
    NEW = "new"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

    @property
    def is_final(self):
        return self in (Status.SHIPPED, Status.CANCELLED)

    def can_change_to(self, other):
        allowed = {
            Status.NEW: {Status.PAID, Status.CANCELLED},
            Status.PAID: {Status.SHIPPED, Status.CANCELLED},
        }
        return other in allowed.get(self, set())

    @classmethod
    def active(cls):
        return [s for s in cls if not s.is_final]


Status.SHIPPED.is_final      # True
Status.NEW.can_change_to(Status.PAID)     # True
Status.SHIPPED.can_change_to(Status.NEW)  # False
Status.active()              # [<Status.NEW: 'new'>, <Status.PAID: 'paid'>]
```

`self` je tady člen enumu, například `Status.NEW`. Pozor: slovník
`allowed` je uvnitř metody schválně. Kdyby byl v těle třídy, enum by
z něj udělal dalšího člena.

## 8. `_missing_`: tolerantní hledání

Když `Color(value)` hodnotu nenajde, zavolá ještě classmethod
`_missing_`. Ta může vrátit člena místo chyby, třeba pro hodnoty
s jinými velkými písmeny:

```python
class Answer(StrEnum):
    YES = "yes"
    NO = "no"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.strip().lower():
                    return member
        return None          # None = opravdu neexistuje → ValueError


Answer(" YES ")              # <Answer.YES: 'yes'>
Answer("maybe")              # ValueError: 'maybe' is not a valid Answer
```

## 9. Hodnota a popisek: vlastní `__new__`

Častá potřeba: hodnota pro databázi a zároveň popisek pro člověka.
Tuple jako hodnota s vlastním `__new__` to umí:

```python
class Role(StrEnum):
    ADMIN = "admin", "Administrátor"
    EDITOR = "editor", "Redaktor"

    def __new__(cls, value, label):
        member = str.__new__(cls, value)
        member._value_ = value       # co bude .value
        member.label = label         # atribut navíc
        return member


Role.ADMIN                   # <Role.ADMIN: 'admin'>
Role.ADMIN.label             # 'Administrátor'
Role("editor").label         # 'Redaktor'
[(r.value, r.label) for r in Role]  # [('admin', 'Administrátor'), ('editor', 'Redaktor')]
```

Enum tuple za rovnítkem rozbalí do argumentů `__new__`. U `StrEnum`
se člen vyrábí přes `str.__new__`, protože to je string, a `_value_`
říká, co má vrátit `.value`. Přesně tohle za tebe dělá Django
`TextChoices` (sekce 12), jen chytřeji: popisek doplní i tam, kde
chybí.

## 10. `Flag`: kombinace příznaků

`Flag` je pro hodnoty, které jdou kombinovat, například oprávnění:

```python
from enum import Flag


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    DELETE = auto()


rw = Perm.READ | Perm.WRITE
rw                           # <Perm.READ|WRITE: 3>
Perm.READ in rw              # True
Perm.DELETE in rw            # False
list(rw)                     # [<Perm.READ: 1>, <Perm.WRITE: 2>]
```

V běžném webovém kódu ho potkáš málokdy. Django oprávnění řeší
přes databázi, ne přes `Flag`.

## 11. Enum v `match` a v JSON

V `match` se členy píšou s tečkou, takže je Python bere jako hodnotu
k porovnání, ne jako novou proměnnou:

```python
def label(status):
    match status:
        case Status.NEW:
            return "nová"
        case Status.PAID | Status.SHIPPED:
            return "zaplacená"
        case _:
            return "jiná"


label(Status.PAID)           # 'zaplacená'
label(Status.CANCELLED)      # 'jiná'
```

JSON: `IntEnum` a `StrEnum` se převedou samy, protože jsou to čísla
a stringy. Obyčejný `Enum` je potřeba převést přes `.value` (víc
o `default` v [`JSON.md`](JSON.md)):

```python
import json

json.dumps({"priority": Priority.HIGH})    # '{"priority": 3}'
json.dumps({"color": Color.RED.value})     # '{"color": 1}'
json.dumps({"color": Color.RED})           # TypeError: Object of type Color is not JSON serializable
```

Zpátky z JSON pak `Color(data["color"])`.

## 12. Django: `TextChoices` a `IntegerChoices`

Django nabízí vlastní enumy pro pole s výběrem hodnot. Zápis
v modelu:

```python
from django.db import models


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Koncept"
        PUBLISHED = "published", "Publikováno"
        IN_REVIEW = "in_review"          # bez popisku

    status = models.CharField(
        max_length=20,
        choices=Status,                  # od Djanga 5.0, dřív Status.choices
        default=Status.DRAFT,
    )
```

Co z toho máš (ověřeno na Djangu 6.1):

| Výraz | Výsledek |
|---|---|
| `Article.Status.DRAFT.label` | `'Koncept'` |
| `Article.Status.IN_REVIEW.label` | `'In Review'` (z názvu: `_` → mezera, `.title()`) |
| `Article.Status.choices` | `[('draft', 'Koncept'), ('published', 'Publikováno'), ('in_review', 'In Review')]` |
| `Article.Status.labels` | `['Koncept', 'Publikováno', 'In Review']` |
| `Article.Status.values` | `['draft', 'published', 'in_review']` |
| `Article.Status.names` | `['DRAFT', 'PUBLISHED', 'IN_REVIEW']` |
| `Article.Status.DRAFT == "draft"` | `True` (je to `StrEnum`) |
| `repr(Article.Status.DRAFT)` | `Article.Status.DRAFT` |
| `article.get_status_display()` | popisek aktuální hodnoty, např. `'Koncept'` |

Jak to uvnitř funguje (zdroják `django/db/models/enums.py`):

- `TextChoices` dědí z `Choices` a `StrEnum`, `IntegerChoices`
  z `Choices` a `IntEnum`. Opět vícenásobná dědičnost.
- `Choices` má metatřídu `ChoicesType` (podtřída `EnumType`). Ta při
  vytvoření třídy projde členy: když je hodnota tuple, jejíž poslední
  prvek je string, odtrhne ho jako popisek. Jinak popisek vyrobí ze
  jména. Popisek uloží členovi do `_label_` a property `label` ho
  vrací.
- `choices`, `labels`, `values` a `names` jsou property na metatřídě,
  proto se volají na třídě (`Status.choices`), ne na členovi.
- Metatřída na konci zavolá `enum.unique`, takže dvě stejné hodnoty
  jsou chyba.
- `TextChoices` s `auto()` dá jako hodnotu přímo jméno (`"RED"`),
  ne jméno malými jako `StrEnum`.

`get_status_display()` nepochází z enumu. Django ho přidá modelu pro
každé pole, které má `choices`. Pro hodnotu, která v `choices` není,
vrátí hodnotu samotnou. Pole s `choices` taky ve formulářích
a v adminu automaticky vykreslí `<select>` s popisky.

V šablonách se pak píše `{{ article.get_status_display }}`
a v kódu se porovnává se členy, ne se stringy:
`if article.status == Article.Status.PUBLISHED:`.

## 13. Srovnání s TS

| TypeScript | Python |
|---|---|
| `enum Color { Red = 1, Green = 2 }` | `class Color(Enum): RED = 1; GREEN = 2` |
| `Color.Red` | `Color.RED` |
| `Color[1]` → `"Red"` (reverse mapping) | `Color(1).name` → `'RED'` |
| `type Status = "new" \| "paid"` | `StrEnum` nebo `Literal["new", "paid"]` z `typing` |
| enum je jen sada hodnot | enum je třída: metody, property, `_missing_` |

TS komunita často dává přednost union literal typům před `enum`.
V Pythonu je enum běžný idiom a Django ho používá přímo.

## 14. Časté chyby

| Příznak | Příčina |
|---|---|
| `Color.RED == 1` je `False` | obyčejný `Enum` se nerovná hodnotě, porovnej `.value` nebo použij `IntEnum` / `StrEnum` |
| `ValueError: 'PAID' is not a valid Status` | `Status("PAID")` hledá podle **hodnoty**, podle jména je `Status["PAID"]` |
| `KeyError: 'paid'` | `Status["paid"]` hledá podle **jména**, podle hodnoty je `Status("paid")` |
| `TypeError: '<' not supported between instances` | obyčejný `Enum` se neřadí, použij `key=lambda m: m.value` nebo `IntEnum` |
| člen „chybí“ při iteraci | má stejnou hodnotu jako jiný člen a stal se aliasem, pomůže `@unique` |
| pomocný slovník se stal členem enumu | v těle enumu je každé přiřazení člen, dej ho do metody nebo mimo třídu |
| `TypeError: Object of type X is not JSON serializable` | obyčejný `Enum` převeď přes `.value` |
| `status == "payed"` tiše `False` u `StrEnum` | `StrEnum` se rovná stringům a překlep v literálu neodhalí, porovnávej se členy |
| `AttributeError: 'Status' object has no attribute 'choices'` (Django) | `choices` je na třídě (`Status.choices`), ne na členovi |
