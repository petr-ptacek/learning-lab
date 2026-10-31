# Třídy a instance do hloubky

Výtah z článků, na které odkazuje
[`07-oop-zaklady/RESOURCES.md`](../07-oop-zaklady/RESOURCES.md) (hlavně
Real Python *Python Classes: The Power of OOP* a *OOP in Python*, plus
kapitola *Classes* z oficiálního tutoriálu). Přehled je v
[`THEORY.md`](../07-oop-zaklady/THEORY.md). Tady je, jak to funguje
uvnitř: kde Python hledá atributy, co přesně je `self` a proč je třída
taky objekt. Bez toho se Django modely nedají pořádně pochopit.

Navazuje: metody a `@property` v
[`METHODS_AND_PROPERTIES.md`](METHODS_AND_PROPERTIES.md), dunder metody
v [`DUNDER_METHODS.md`](DUNDER_METHODS.md), `@dataclass` v
[`DATACLASSES.md`](DATACLASSES.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Tělo třídy je obyčejný kód](#1-tělo-třídy-je-obyčejný-kód)
2. [Atributy žijí ve slovnících](#2-atributy-žijí-ve-slovnících)
3. [Jak Python hledá atribut](#3-jak-python-hledá-atribut)
4. [Zastínění a sdílené měnitelné atributy](#4-zastínění-a-sdílené-měnitelné-atributy)
5. [Co je `self`](#5-co-je-self)
6. [Kdy použít atribut třídy](#6-kdy-použít-atribut-třídy)
7. [Dynamická práce s atributy: `getattr`, `setattr`, `hasattr`](#7-dynamická-práce-s-atributy-getattr-setattr-hasattr)
8. [Třída je taky objekt](#8-třída-je-taky-objekt)
9. [Vnořená třída](#9-vnořená-třída)
10. [„Soukromé“ atributy](#10-soukromé-atributy)
11. [Srovnání s JS](#11-srovnání-s-js)

---

## 1. Tělo třídy je obyčejný kód

Python tělo `class` **spustí jednou, při definici**, shora dolů, jako
každý jiný blok. Co se v něm přiřadí, stane se atributem třídy. `def`
uvnitř je taky jen přiřazení: jméno metody → funkce.

```python
class Demo:
    print("spouštím tělo třídy")
    x = 1 + 1

    def hello(self):
        return "ahoj"
# vypíše: spouštím tělo třídy  (hned při definici, bez vytvoření instance)

Demo.x                 # 2
Demo.hello             # <function Demo.hello at 0x...>
```

Proto `next_id = 1` v těle třídy proběhne jen jednou, ne při každém
`Ticket(...)`. A proto Django může při definici modelu „posbírat“ pole:
v tu chvíli už všechna existují jako atributy třídy (viz `08`).

## 2. Atributy žijí ve slovnících

Každá instance má vlastní slovník atributů `__dict__`. Funkce `vars(obj)`
ho vrátí.

```python
class Product:
    vat = 0.21

    def __init__(self, name, price):
        self.name = name
        self.price = price


milk = Product("Mléko", 24.9)
vars(milk)                        # {'name': 'Mléko', 'price': 24.9}
"vat" in Product.__dict__         # True
"vat" in vars(milk)               # False
```

`self.name = name` v `__init__` tedy znamená „ulož do slovníku této
instance klíč `name`“. Instance nemají předem dané atributy, vznikají
přiřazením. Proto jde atribut přidat i zvenku (`milk.color = "bílá"`),
i když to v běžném kódu nedělej.

## 3. Jak Python hledá atribut

**Čtení** `obj.x`:

1. slovník instance `vars(obj)`,
2. slovník třídy,
3. slovníky rodičů v pořadí MRO (dědičnost, `08`),
4. nic → `AttributeError`.

**Zápis** `obj.x = ...` a **mazání** `del obj.x` pracují **jen se
slovníkem instance**. Do třídy se zapisuje výslovně přes `Třída.x = ...`.

```python
milk.vat                      # 0.21 — našel se na třídě
milk.color                    # AttributeError: 'Product' object has no attribute 'color'
```

(Výjimka z pravidla: `@property` a další *deskriptory* na třídě mají
přednost i před slovníkem instance. Proto setter property zachytí i
zápis. Detaily jsou v `08-oop-dedicnost`.)

## 4. Zastínění a sdílené měnitelné atributy

```python
class Settings:
    language = "cs"
    tags = []


s1 = Settings()
s2 = Settings()
s1.language = "en"            # zápis → nový atribut v instanci s1
s1.tags.append("beta")        # ČTENÍ s1.tags (najde se na třídě) + změna seznamu

s1.language, s2.language      # ('en', 'cs')
s2.tags                       # ['beta'] — tentýž seznam
vars(s1), vars(s2)            # ({'language': 'en'}, {})

Settings.language = "de"      # změna na třídě
s1.language, s2.language      # ('en', 'de') — s1 má vlastní, s2 čte z třídy

del s1.language               # smaže atribut instance
s1.language                   # 'de' — znovu se čte z třídy
```

Dvě situace, které vypadají podobně, ale chovají se úplně jinak:

| Zápis | Co se stane |
|---|---|
| `s1.language = "en"` | přiřazení: vznikne atribut **instance**, třída se nemění |
| `s1.tags.append("x")` | čtení + volání metody: najde se seznam **na třídě** a změní se, všichni to vidí |
| `s1.tags += ["x"]` | nejzáludnější: změní sdílený seznam **a navíc** uloží odkaz na něj do instance |

Pravidlo: v těle třídy jen neměnné hodnoty (čísla, stringy, tuply,
`None`). Seznamy, dicty a sety vytvářej v `__init__`. Stejnou past
znáš z výchozích hodnot parametrů (`def f(x=[])`).

## 5. Co je `self`

Když funkci uloženou ve třídě čteš **přes instanci**, Python ji vrátí
jako *vázanou metodu* (bound method): funkci, která má instanci už
připravenou jako první argument.

```python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self, step=1):
        self.value += step
        return self.value


c = Counter()
Counter.increment              # <function Counter.increment at 0x...>
c.increment                    # <bound method Counter.increment of <...Counter object...>>
c.increment()                  # 1
Counter.increment(c, 10)       # 11 — totéž, instance předaná ručně
```

`self` tedy není klíčové slovo, je to jen obvyklé jméno prvního
parametru. Fungovalo by i `this` nebo `me`, ale nikdy to nedělej.
Vázaná metoda si instanci pamatuje, takže jde předat dál jako callback:

```python
step = c.increment
step()                         # 12
list(map(str.upper, ["a", "b"]))   # ['A', 'B'] — nevázaná metoda jako funkce
```

Rozdíl proti JS: `this` v JS závisí na tom, **jak** se funkce zavolá
(proto `.bind(this)` a arrow funkce v callbacích). V Pythonu se instance
naváže při čtení `c.increment` a už se neztratí.

Chyba, když `self` zapomeneš:

```python
class Broken:
    def hello():
        return "ahoj"


Broken().hello()
# TypeError: Broken.hello() takes 0 positional arguments but 1 was given
```

Python instanci předal, ale funkce žádný parametr nečeká.

## 6. Kdy použít atribut třídy

| Použití | Příklad |
|---|---|
| konstanta společná všem | `vat = 0.21`, `MAX_ITEMS = 50` |
| výchozí hodnota, kterou jednotlivá instance může přepsat | `priority = "normal"`, v `__init__` jen `if priority: self.priority = priority` |
| počítadlo nebo registr přes všechny instance | `next_id = 1`, `objects = []` |
| konfigurace pro framework | Django: `ordering`, `list_display`, `fields`, `model = Book` |

Poslední řádek je klíčový pro Django. V class-based views i v adminu se
chování nastavuje **atributy třídy**, ne parametry:

```python
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]    # atribut třídy, čte ho admin
    search_fields = ["title"]
```

Admin si pak hodnotu přečte přes `self.list_display`. Kdyby ji
instance přepsala, platila by pro ni. Bez přepsání se najde na třídě,
to je bod 3.

Do atributu třídy se zevnitř metody zapisuje přes jméno třídy
(`Ticket.next_id += 1`) nebo `type(self).next_id += 1`. Zápis
`self.next_id += 1` by vytvořil atribut **instance** a počítadlo
na třídě by se nezměnilo:

```python
class Wrong:
    next_id = 1

    def __init__(self):
        self.id = self.next_id
        self.next_id += 1          # vytvoří atribut instance!


Wrong().id, Wrong().id, Wrong.next_id   # (1, 1, 1)
```

## 7. Dynamická práce s atributy: `getattr`, `setattr`, `hasattr`

Když je jméno atributu v proměnné (string), tečka nepomůže:

```python
coffee = Product("Káva", 189.0)
field = "price"

getattr(coffee, field)                 # 189.0 — totéž co coffee.price
getattr(coffee, "color", None)         # None — default místo AttributeError
hasattr(coffee, "name")                # True
setattr(coffee, "price", 169.0)        # totéž co coffee.price = 169.0
coffee.price                           # 169.0
```

Používá se tam, kde se pracuje s „poli podle jména“: serializace do
dictu, filtrování podle zadaných kritérií, Django `getattr(settings,
"MY_OPTION", default)`, generické views. Obdoba `obj[key]` v JS:

```python
def to_dict(obj, fields):
    return {name: getattr(obj, name) for name in fields}


to_dict(coffee, ["name", "price"])     # {'name': 'Káva', 'price': 169.0}
```

## 8. Třída je taky objekt

```python
type(milk)                    # <class '__main__.Product'>
type(Product)                 # <class 'type'>
isinstance(milk, Product)     # True
Product.__name__              # 'Product'

factory = Product             # třída v proměnné
factory("Chléb", 39.0).name   # 'Chléb'
```

Třída je instance typu `type`, a `type` je „továrna na třídy“
(*metatřída*). Důsledky:

- třídu jde předat jako argument. Na tom stojí `@classmethod` (dostane
  `cls`) i Django (`ListView` má `model = Book`, tedy třídu jako hodnotu),
- třída může mít atributy a metody jako každý objekt,
- třídu jde vytvořit i za běhu přes `type("Jméno", (), {...})`.
  Nebudeš to psát, ale Django to tak dělá uvnitř.

Metatřídy podrobně: `08-oop-dedicnost`.

## 9. Vnořená třída

Třída definovaná v těle jiné třídy je **jen další atribut** té vnější.
Nemá k ní žádný zvláštní přístup a nevidí její proměnné. Je to
jmenný prostor, „krabička na nastavení“:

```python
class Book:
    title = "?"

    class Meta:
        ordering = ["title"]
        verbose_name = "kniha"


Book.Meta                         # <class '__main__.Book.Meta'>
Book.Meta.ordering                # ['title']
getattr(Book.Meta, "db_table", "výchozí")   # 'výchozí'
```

Proč to Django dělá takhle, a ne přes atributy přímo na modelu?
Atributy modelu jsou **pole** (`title`, `author`). Kdyby tam bylo
i `ordering`, nešlo by poznat, jestli je to sloupec, nebo nastavení,
a nemohl bys mít sloupec jménem `ordering`. `Meta` drží nastavení
odděleně. Django ji při vytvoření třídy modelu přečte (právě přes
`getattr(meta, "ordering", ...)`) a výsledek uloží do `Book._meta`.
Jak přesně, je v `08-oop-dedicnost`.

Stejný vzor uvidíš v `ModelForm` (`class Meta: model = Book; fields =
[...]`) a v DRF serializerech.

## 10. „Soukromé“ atributy

| Zápis | Význam |
|---|---|
| `self.price` | veřejný atribut |
| `self._price` | konvence „vnitřní, nesahej zvenku“. Technicky dostupný, editor a linter varují |
| `self.__price` | *name mangling*: Python ho uloží jako `_Product__price`. Účel je zabránit kolizi jmen v podtřídách, ne utajení |
| `__init__`, `__str__` | dunder, rezervované pro Python. Vlastní takové nevymýšlej |

```python
class Account:
    def __init__(self):
        self._balance = 0
        self.__pin = "1234"


acc = Account()
vars(acc)                    # {'_balance': 0, '_Account__pin': '1234'}
```

V praxi stačí `_jméno`. Python spoléhá na dohodu: „všichni jsme tu
dospělí“.

## 11. Srovnání s JS

| Python | JS |
|---|---|
| `class A:` | `class A {}` |
| `def __init__(self, x):` | `constructor(x) {}` |
| `self.x = x` | `this.x = x` |
| `A(1)` | `new A(1)` |
| `self` výslovně, naváže se při čtení `obj.metoda` | `this` implicitně, závisí na způsobu volání |
| atribut třídy `x = 1` v těle | `static x = 1` (ale v Pythonu ho čte i instance) |
| `@classmethod` | `static` metoda (bez přístupu k instanci) |
| `@property` | `get x() {}` / `set x(v) {}` |
| `_x` (konvence) | `#x` (skutečně privátní) |
| `__str__` | `toString()` |
| `vars(obj)` | `{ ...obj }` / `Object.entries(obj)` |
| `getattr(obj, name)` | `obj[name]` |
| `isinstance(obj, A)` | `obj instanceof A` |

Největší rozdíl: v JS je `static` člen dostupný **jen** přes třídu
(`A.x`), instance ho nevidí. V Pythonu instance atribut třídy čte
(`obj.x`), dokud ho nezastíní vlastním.
