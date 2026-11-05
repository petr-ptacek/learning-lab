# Dědičnost a `super()`

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(hlavně Real Python *Inheritance and Composition*, *Supercharge Your
Classes With Python super()* a kapitola *Inheritance* z oficiálního
tutoriálu). Přehled je v
[`THEORY.md`](../08-oop-dedicnost/THEORY.md). Tady je podrobně, jak
dědičnost funguje uvnitř: kde Python hledá atributy, co přesně dělá
`super()` a kdy dědičnost vůbec nepoužít.

Staví na [`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md)
(hledání atributů instance → třída) a
[`METHODS_AND_PROPERTIES.md`](METHODS_AND_PROPERTIES.md) (`cls`
v classmethod). Navazuje vícenásobná dědičnost a mixiny v
[`MULTIPLE_INHERITANCE_AND_MIXINS.md`](MULTIPLE_INHERITANCE_AND_MIXINS.md)
a abstraktní třídy v [`ABSTRACT_BASE_CLASSES.md`](ABSTRACT_BASE_CLASSES.md).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Podtřída: `class B(A)`](#1-podtřída-class-ba)
2. [Hledání atributů přes rodiče](#2-hledání-atributů-přes-rodiče)
3. [Přepsání metody](#3-přepsání-metody)
4. [`super()`: zavolej verzi rodiče](#4-super-zavolej-verzi-rodiče)
5. [`super().__init__()` a co když zapomeneš](#5-super__init__-a-co-když-zapomeneš)
6. [Atributy třídy jako konfigurace](#6-atributy-třídy-jako-konfigurace)
7. [`cls` a `type(self)` v podtřídě](#7-cls-a-typeself-v-podtřídě)
8. [`isinstance`, `issubclass`, `type(x) is`](#8-isinstance-issubclass-typex-is)
9. [`object`: kořen všech tříd](#9-object-kořen-všech-tříd)
10. [Kompozice vs. dědičnost](#10-kompozice-vs-dědičnost)
11. [Srovnání s JS](#11-srovnání-s-js)
12. [Časté chyby](#12-časté-chyby)

---

## 1. Podtřída: `class B(A)`

Třída v závorce za jménem je **rodič** (základní třída, *base class*,
*superclass*). Nová třída je **podtřída** (*subclass*). Podtřída dostane
všechno, co má rodič, a může přidat nebo změnit, co potřebuje.

```python
class Employee:
    role = "zaměstnanec"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} – {self.role}"


class Developer(Employee):
    role = "vývojář"


dev = Developer("Petr", 80_000)    # __init__ zdědil od Employee
dev.describe()                     # 'Petr – vývojář'
dev.salary                         # 80000
Developer.__bases__                # (<class '__main__.Employee'>,)
```

`Developer` nemá vlastní `__init__` ani `describe`. Obojí najde
u `Employee`. `describe` ale čte `self.role` a `self` je `Developer`,
takže najde jeho `role`.

Dědičnost vyjadřuje vztah **„je“**: vývojář *je* zaměstnanec.
V Djangu je to `class Book(models.Model)`: kniha *je* model.

## 2. Hledání atributů přes rodiče

V [`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md) platilo:
při čtení `obj.x` hledá Python v instanci a pak ve třídě. S dědičností
pokračuje dál **po rodičích**, dokud atribut nenajde:

```
dev.describe
  1. vars(dev)            → není
  2. vars(Developer)      → není
  3. vars(Employee)       → je → použije se
  4. vars(object)         → (sem by došel, kdyby nebyl ani v Employee)
```

Pořadí tříd, kterými Python prochází, je uložené v `__mro__`
(*method resolution order*):

```python
Developer.__mro__
# (<class '__main__.Developer'>, <class '__main__.Employee'>, <class 'object'>)

[cls.__name__ for cls in Developer.__mro__]      # ['Developer', 'Employee', 'object']
"describe" in vars(Developer)                    # False
"describe" in vars(Employee)                     # True
"role" in vars(Developer)                        # True
```

Při jednoduché dědičnosti je MRO prostě řetěz od podtřídy k `object`.
U vícenásobné dědičnosti je pořadí zajímavější, viz
[`MULTIPLE_INHERITANCE_AND_MIXINS.md`](MULTIPLE_INHERITANCE_AND_MIXINS.md).

Zápis funguje pořád stejně: `obj.x = ...` zapíše **do instance**,
rodičů ani třídy se nedotkne.

## 3. Přepsání metody

Když podtřída definuje metodu se stejným jménem, najde se dřív než ta
u rodiče. Rodičovská verze se pro instance podtřídy „přepíše“
(*override*):

```python
class Manager(Employee):
    role = "manažer"

    def describe(self):
        return f"{self.name} vede tým"


Manager("Jana", 120_000).describe()     # 'Jana vede tým'
Employee("Eva", 50_000).describe()      # 'Eva – zaměstnanec'
```

Rodič se nezměnil. Přepsání platí jen pro `Manager` a jeho podtřídy.

Důležitý důsledek: metoda rodiče, která volá `self.něco()`, zavolá
**přepsanou** verzi, pokud ji podtřída má. Python to rozhoduje až za
běhu podle skutečného typu `self`. Tomu se říká **polymorfismus**:

```python
class Shape:
    def area(self):
        return 0

    def describe(self):
        return f"{type(self).__name__} má obsah {self.area()}"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


Square(3).describe()       # 'Square má obsah 9'
```

`describe` je napsaná jen jednou v `Shape`, ale pro čtverec použije
jeho `area`. Na tomhle stojí Django class-based views: `ListView.get()`
volá `self.get_queryset()` a ty v podtřídě přepíšeš jen `get_queryset`.

## 4. `super()`: zavolej verzi rodiče

Často nechceš rodičovskou metodu nahradit, ale **rozšířit**: udělat to,
co rodič, a něco navíc. K tomu je `super()`:

```python
class Manager(Employee):
    role = "manažer"

    def __init__(self, name, salary):
        super().__init__(name, salary)
        self.reports = []

    def describe(self):
        base = super().describe()          # 'Jana – manažer'
        return f"{base}, podřízených: {len(self.reports)}"


boss = Manager("Jana", 120_000)
boss.describe()            # 'Jana – manažer, podřízených: 0'
```

`super()` vrátí zástupný objekt, přes který se hledání atributu
**přeskočí aktuální třídu** a začne až u další třídy v MRO. Volání
`super().describe()` tedy najde `Employee.describe` a předá mu
stejné `self`.

Bez argumentů funguje jen uvnitř metody třídy. Python si sám doplní
třídu, ve které metoda vznikla, a `self`. Starší zápis
`super(Manager, self).describe()` dělá totéž, dnes ho psát nemusíš.

Kdy rozšířit přes `super()` a kdy přepsat celé:

| Situace | Postup |
|---|---|
| rodič dělá správnou věc a chceš přidat krok před / po | `super()` |
| chování rodiče je pro podtřídu úplně špatně | přepiš celé, `super()` nevolej |
| rodič nastavuje atributy v `__init__` | **vždy** `super().__init__(...)` |

`super()` funguje stejně i v classmethod, jen místo instance předá
třídu:

```python
class Base:
    @classmethod
    def create(cls):
        return cls()


class Child(Base):
    @classmethod
    def create(cls):
        obj = super().create()      # zavolá Base.create s cls=Child
        obj.ready = True
        return obj


type(Child.create()).__name__     # 'Child'
Child.create().ready              # True
```

## 5. `super().__init__()` a co když zapomeneš

Nejčastější chyba v dědičnosti: podtřída napíše vlastní `__init__`
a zapomene zavolat rodičovský. Rodičovský `__init__` se pak **nespustí
vůbec** a atributy, které nastavuje, chybí:

```python
class Intern(Employee):
    def __init__(self, name, salary, school):
        self.school = school        # chybí super().__init__(name, salary)


intern = Intern("Ondra", 20_000, "ČVUT")
vars(intern)                        # {'school': 'ČVUT'}
intern.describe()                   # AttributeError: 'Intern' object has no attribute 'name'
```

Chyba se neobjeví při vytvoření instance, ale až při prvním použití
chybějícího atributu, často úplně jinde v kódu. Opravené:

```python
class Intern(Employee):
    role = "stážista"

    def __init__(self, name, salary, school):
        super().__init__(name, salary)
        self.school = school


Intern("Ondra", 20_000, "ČVUT").describe()     # 'Ondra – stážista'
```

Pravidla:

- Když podtřída **nemá** vlastní `__init__`, zdědí rodičův a není co
  řešit.
- Když ho má, skoro vždy volá `super().__init__(...)`, obvykle jako
  první řádek. Pak teprve nastaví vlastní atributy.
- Nový měnitelný atribut (seznam, dict) vytvoř v `__init__` podtřídy,
  ne jako atribut třídy. Platí stejná past jako v
  [`CLASSES_AND_INSTANCES.md`](CLASSES_AND_INSTANCES.md#4-zastínění-a-sdílené-měnitelné-atributy).

## 6. Atributy třídy jako konfigurace

Rodič může napsat obecnou logiku, která čte atributy třídy, a podtřídy
jen ty atributy přepíšou. Kód se nemění, mění se „nastavení“:

```python
class Account:
    fee = 0

    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        total = amount + self.fee
        if total > self.balance:
            return False
        self.balance -= total
        return True


class BusinessAccount(Account):
    fee = 5


a, b = Account(100), BusinessAccount(100)
a.withdraw(50), b.withdraw(50)      # (True, True)
a.balance, b.balance                # (50, 45)
```

`withdraw` čte `self.fee`. U `BusinessAccount` ho Python najde dřív
v podtřídě než v `Account`.

Tohle je hlavní styl Django class-based views. Logiku má `ListView`,
ty jen nastavíš atributy:

```python
class BookListView(ListView):        # Django, jen pro ilustraci
    model = Book
    template_name = "books/list.html"
    paginate_by = 20
```

Totéž `ModelAdmin` (`list_display`, `search_fields`) nebo formuláře.

## 7. `cls` a `type(self)` v podtřídě

V [`METHODS_AND_PROPERTIES.md`](METHODS_AND_PROPERTIES.md) jsme psali
alternativní konstruktory přes `cls(...)`, ne `Product(...)`. Teď je
vidět proč:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"])

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price!r})"


class DigitalProduct(Product):
    pass


DigitalProduct.from_dict({"name": "E-kniha", "price": 199})
# DigitalProduct('E-kniha', 199)
```

- `cls` je třída, přes kterou se metoda zavolala. Podtřída tak dostane
  instanci podtřídy, i když je metoda napsaná v rodiči.
- `type(self).__name__` v `__repr__` vypíše skutečnou třídu. Kdybys
  napsal natvrdo `"Product("`, každá podtřída by se vypisovala jako
  `Product`.

Stejné pravidlo platí uvnitř metod: na atribut třídy se odkazuj přes
`type(self).x` nebo `self.x`, ne `Product.x`, jinak podtřída nemůže
hodnotu přepsat.

## 8. `isinstance`, `issubclass`, `type(x) is`

```python
dev = Developer("Petr", 80_000)

isinstance(dev, Developer)          # True
isinstance(dev, Employee)           # True  (vývojář JE zaměstnanec)
isinstance(dev, Manager)            # False
type(dev) is Employee               # False (přesný typ je Developer)
type(dev) is Developer              # True
issubclass(Developer, Employee)     # True
issubclass(Employee, Developer)     # False
issubclass(Developer, Developer)    # True  (třída je podtřída sama sebe)
isinstance(dev, (Manager, Developer))   # True (stačí jedna z tuple)
```

| Test | Otázka |
|---|---|
| `isinstance(x, A)` | je `x` instance `A` **nebo kterékoli podtřídy**? |
| `issubclass(B, A)` | je třída `B` potomkem `A` (nebo `A` sama)? |
| `type(x) is A` | je přesný typ `x` právě `A`? |

Skoro vždy chceš `isinstance`. `type(x) is A` by odmítl podtřídu, i když
se chová stejně, a tím rozbije polymorfismus. Proto se v `__eq__` píše
`isinstance(other, Money)`.

Ještě lepší je často typ vůbec nekontrolovat a prostě zavolat metodu
(*duck typing*): „když to kváká jako kachna…“.

## 9. `object`: kořen všech tříd

Každá třída bez uvedeného rodiče dědí z `object`. `class A:` je totéž
co `class A(object):`.

```python
class Plain:
    pass


Plain.__mro__                       # (<class '__main__.Plain'>, <class 'object'>)
issubclass(int, object)             # True
"__repr__" in vars(object)          # True
"__eq__" in vars(object)            # True
```

Odtud pochází výchozí chování, které zná každý objekt:
`<__main__.Plain object at 0x...>` je `object.__repr__`, porovnání
identity je `object.__eq__`. Když v třídě napíšeš vlastní `__repr__`,
je to taky přepsání metody rodiče `object`.

## 10. Kompozice vs. dědičnost

Dědičnost je silná vazba: podtřída zdědí **všechno** a závisí na
vnitřnostech rodiče. Druhá možnost je **kompozice**: objekt má jiný
objekt jako atribut a deleguje na něj práci.

| Vztah | Nástroj | Příklad |
|---|---|---|
| „je“ (*is-a*) | dědičnost | `Developer` je `Employee`, `Book` je `Model` |
| „má“ (*has-a*) | kompozice | `Car` má `Engine`, `Order` má seznam položek |

```python
class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"motor {self.power} kW běží"


class Car:
    def __init__(self, brand, power):
        self.brand = brand
        self.engine = Engine(power)     # kompozice: auto MÁ motor

    def start(self):
        return f"{self.brand}: {self.engine.start()}"


Car("Škoda", 110).start()       # 'Škoda: motor 110 kW běží'
```

`class Car(Engine)` by tvrdilo, že auto *je* motor. To nesedí a auto by
zdědilo metody, které mu nepatří. Rada z praxe: když váháš, zvol
kompozici. Dědičnost použij, když podtřídu opravdu jde použít všude,
kde se čeká rodič (bez překvapení pro volajícího kód).

V Djangu najdeš obojí. Model dědí z `models.Model`, ale `ForeignKey`
je kompozice: kniha *má* autora.

## 11. Srovnání s JS

| Python | JS |
|---|---|
| `class B(A):` | `class B extends A {}` |
| `super().__init__(x)` | `super(x)` v `constructor` |
| `super().metoda()` | `super.metoda()` |
| zapomenutý `super().__init__()` → atributy chybí, chyba až později | zapomenuté `super()` → `ReferenceError` hned při `this` |
| podtřída bez `__init__` zdědí rodičův | podtřída bez `constructor` zdědí rodičův |
| `B.__mro__` | řetěz prototypů (`Object.getPrototypeOf`) |
| `isinstance(b, A)` | `b instanceof A` |
| `issubclass(B, A)` | `A.prototype.isPrototypeOf(B.prototype)` |
| vícenásobná dědičnost `class C(A, B)` | neexistuje (jen mixin funkce) |

Hlavní rozdíl: JS volání `super()` v konstruktoru vynucuje, Python ne.
Proto je zapomenutý `super().__init__()` v Pythonu tak zrádný.

## 12. Časté chyby

| Příznak | Příčina |
|---|---|
| `AttributeError: 'X' object has no attribute 'name'` u atributu z rodiče | vlastní `__init__` v podtřídě bez `super().__init__(...)` |
| `TypeError: Employee.__init__() missing 2 required positional arguments: 'name' and 'salary'` | `super().__init__()` voláš bez argumentů, které rodič potřebuje |
| podtřída se vypisuje jménem rodiče | `__repr__` / `__str__` s natvrdo napsaným jménem místo `type(self).__name__` |
| `from_dict` na podtřídě vrací instanci rodiče | v classmethod `Product(...)` místo `cls(...)` |
| přepsání atributu třídy v podtřídě nic nezmění | rodič čte `Product.fee` místo `self.fee` |
| `RecursionError` v přepsané metodě | voláš `self.describe()` místo `super().describe()` |
| podtřída „dědí“ věci, které jí nedávají smysl | vztah „má“, ne „je“: použij kompozici |
