# Vícenásobná dědičnost, MRO a mixiny

Výtah z článků, na které odkazuje
[`08-oop-dedicnost/RESOURCES.md`](../08-oop-dedicnost/RESOURCES.md)
(hlavně Real Python *Supercharge Your Classes With Python super()*,
*Inheritance and Composition*, Raymond Hettinger *Python's super()
considered super!* a dokument *The Python 2.3 Method Resolution
Order*). Přehled je v [`THEORY.md`](../08-oop-dedicnost/THEORY.md).

Tohle je klíč k Django class-based views: `class
BookListView(LoginRequiredMixin, ListView)` je vícenásobná dědičnost
a celé chování stojí na tom, v jakém pořadí Python prochází rodiče
a co přesně volá `super()`.

Staví na [`INHERITANCE_AND_SUPER.md`](INHERITANCE_AND_SUPER.md)
(jednoduchá dědičnost, `super()`, `__mro__`).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## Obsah

1. [Víc rodičů: `class C(A, B)`](#1-víc-rodičů-class-ca-b)
2. [MRO: pořadí hledání](#2-mro-pořadí-hledání)
3. [Diamant](#3-diamant)
4. [`super()` znamená „další v MRO“, ne „rodič“](#4-super-znamená-další-v-mro-ne-rodič)
5. [Kooperativní `super()` a `**kwargs`](#5-kooperativní-super-a-kwargs)
6. [Nekonzistentní MRO](#6-nekonzistentní-mro)
7. [Mixiny](#7-mixiny)
8. [Mixiny v Djangu](#8-mixiny-v-djangu)
9. [Kdy mixiny nepoužívat](#9-kdy-mixiny-nepoužívat)
10. [Srovnání s JS](#10-srovnání-s-js)
11. [Časté chyby](#11-časté-chyby)

---

## 1. Víc rodičů: `class C(A, B)`

Třída může mít víc rodičů. Dostane atributy a metody od všech:

```python
class Flyer:
    def fly(self):
        return "letím"


class Swimmer:
    def swim(self):
        return "plavu"


class Duck(Flyer, Swimmer):
    pass


duck = Duck()
duck.fly(), duck.swim()          # ('letím', 'plavu')
isinstance(duck, Swimmer)        # True
Duck.__bases__                   # (<class '__main__.Flyer'>, <class '__main__.Swimmer'>)
```

Dokud mají rodiče různá jména metod, je to jednoduché. Zajímavé to
začne, když stejnou metodu definuje víc rodičů.

## 2. MRO: pořadí hledání

Když stejné jméno najde Python u víc rodičů, rozhodne **MRO** (*method
resolution order*): seznam tříd, kterými prochází, a první nález
vyhrává.

```python
class A:
    def hello(self):
        return "A"


class B:
    def hello(self):
        return "B"


class AB(A, B):
    pass


class BA(B, A):
    pass


AB().hello(), BA().hello()                   # ('A', 'B')
[c.__name__ for c in AB.__mro__]             # ['AB', 'A', 'B', 'object']
[c.__name__ for c in BA.mro()]               # ['BA', 'B', 'A', 'object']
```

Základní pravidla MRO:

1. Třída je vždy před svými rodiči.
2. Rodiče jsou v pořadí, v jakém je píšeš do hlavičky: **zleva doprava**.
3. Každá třída je v MRO jen jednou, i když k ní vede víc cest.
4. `object` je vždy poslední.

Python MRO počítá algoritmem **C3 linearizace**, který tahle pravidla
splní. Ručně ho počítat nemusíš: vždycky se podívej na `Třída.__mro__`
(tuple) nebo `Třída.mro()` (seznam).

## 3. Diamant

Diamant vznikne, když dva rodiče mají společného předka:

```
      Base
     /    \
  Left    Right
     \    /
     Child
```

```python
class Base:
    def who(self):
        return "Base"


class Left(Base):
    def who(self):
        return "Left"


class Right(Base):
    def who(self):
        return "Right"


class Child(Left, Right):
    pass


Child().who()                                # 'Left'
[c.__name__ for c in Child.__mro__]          # ['Child', 'Left', 'Right', 'Base', 'object']
```

Všimni si: `Base` je až **za** `Right`, ne hned za `Left`. Pravidlo 1
říká, že potomek musí být před předkem, a `Right` je potomek `Base`.
Kdyby `Base` byl hned za `Left`, `Right.who` by se nikdy nenašlo.

V Pythonu je diamant všude, protože každá třída dědí z `object`.
Jakákoli vícenásobná dědičnost je tedy diamant s `object` nahoře.

## 4. `super()` znamená „další v MRO“, ne „rodič“

Tohle je nejdůležitější věc celého souboru. `super()` nevolá rodiče
třídy, ve které je napsané. Volá **další třídu v MRO instance**, se
kterou se právě pracuje:

```python
class Base:
    def hello(self):
        return ["Base"]


class Left(Base):
    def hello(self):
        return ["Left"] + super().hello()


class Right(Base):
    def hello(self):
        return ["Right"] + super().hello()


class Child(Left, Right):
    def hello(self):
        return ["Child"] + super().hello()


Child().hello()          # ['Child', 'Left', 'Right', 'Base']
Left().hello()           # ['Left', 'Base']
```

`Left` dědí jen z `Base`, a přesto `super().hello()` uvnitř `Left`
zavolalo `Right.hello`. Proč: instance je `Child` a její MRO je
`Child → Left → Right → Base → object`. Další po `Left` je `Right`.

U samostatného `Left()` je MRO `Left → Base → object`, takže stejný
řádek `super().hello()` zavolá `Base.hello`.

Důsledek: když každá třída v řetězu volá `super()`, proběhne **každá
metoda právě jednou** a ve správném pořadí. `Base.hello` se zavolá
jen jednou, i když k ní vedou dvě cesty. Kdyby `Left` volala natvrdo
`Base.hello(self)`, `Right` by se přeskočila.

## 5. Kooperativní `super()` a `**kwargs`

Aby řetěz fungoval, musí třídy **spolupracovat**:

1. Každá metoda v řetězu volá `super()`.
2. Metody mají kompatibilní signaturu.
3. Řetěz někde končí: nejvyšší třída `super()` nevolá (nebo volá
   `object`, který danou metodu má).

U `__init__` je problém s argumenty: každá třída potřebuje jiné.
Řešení je vzít si svoje pojmenované argumenty a zbytek poslat dál přes
`**kwargs`:

```python
class Named:
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Priced:
    def __init__(self, price, **kwargs):
        super().__init__(**kwargs)
        self.price = price


class Product(Named, Priced):
    pass


p = Product(name="Káva", price=189)
vars(p)                           # {'price': 189, 'name': 'Káva'}
```

Průchod: `Named.__init__` si vezme `name`, zbytek (`price=189`) pošle
dál. Další v MRO je `Priced`, ten si vezme `price` a pošle prázdné
`**kwargs` do `object.__init__`, který nic nechce.

Kdyby zůstal nějaký argument nespotřebovaný, `object.__init__` spadne:

```python
Product(name="Káva", price=189, color="hnědá")
# TypeError: object.__init__() takes exactly one argument (the instance to initialize)
```

Proto se kooperativní `__init__` volá s pojmenovanými argumenty.
Poziční argumenty v řetězu nejde rozumně rozdělit.

## 6. Nekonzistentní MRO

Některé kombinace rodičů nejde seřadit tak, aby platila všechna
pravidla. Python pak třídu vůbec nevytvoří:

```python
class A:
    pass


class B(A):
    pass


class X(A, B):     # TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B
    pass
```

Hlavička říká „`A` před `B`“ (pořadí zleva doprava), dědičnost říká
„`B` před `A`“ (potomek před předkem). Obojí platit nemůže.

Oprava: obecnější třídu piš **víc vpravo**, tedy `class X(B, A)`, nebo
`A` úplně vynech, protože ji `B` už obsahuje. To je přesně důvod,
proč se v Djangu mixiny píšou vlevo a základní view vpravo.

## 7. Mixiny

**Mixin** je malá třída, která přidává **jednu schopnost**. Sama
o sobě se nepoužívá, jen se „přimíchá“ k jiné třídě:

```python
import json


class ReprMixin:
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({fields})"


class JsonMixin:
    def to_json(self):
        return json.dumps(vars(self), ensure_ascii=False)


class Customer(ReprMixin, JsonMixin):
    def __init__(self, name, city):
        self.name = name
        self.city = city


c = Customer("Anna", "Brno")
c                                 # Customer(name='Anna', city='Brno')
c.to_json()                       # '{"name": "Anna", "city": "Brno"}'
```

`ReprMixin` neví nic o zákaznících. Funguje na čemkoli, co má
atributy instance. Stejný `__repr__` teď můžeš dát `Product`, `Order`
a dalším bez kopírování.

Pravidla pro mixiny:

| Pravidlo | Proč |
|---|---|
| jméno končí na `Mixin` | čtenář hned ví, že to není samostatná třída |
| jedna schopnost, málo kódu | snadno se kombinují |
| žádný vlastní `__init__`, nebo kooperativní s `**kwargs` | nesmí rozbít `__init__` třídy, ke které se přimíchá |
| metody, které třída má i jinde, volají `super()` | řetěz pokračuje dál (sekce 4) |
| v hlavičce **vlevo** před základní třídou | jejich metody se najdou dřív a přes `super()` předají řízení základu |

Mixin, který **mění** existující metodu, ji obalí a zavolá `super()`:

```python
class Saver:
    def save(self):
        self.log.append("uloženo")


class ValidationMixin:
    def save(self):
        if not self.title:
            self.log.append("chyba: chybí titulek")
            return
        super().save()


class TimestampMixin:
    def save(self):
        self.log.append("nastavuji čas")
        super().save()


class Article(TimestampMixin, ValidationMixin, Saver):
    def __init__(self, title):
        self.title = title
        self.log = []


a = Article("Python")
a.save()
a.log                             # ['nastavuji čas', 'uloženo']
b = Article("")
b.save()
b.log                             # ['nastavuji čas', 'chyba: chybí titulek']
[c.__name__ for c in Article.__mro__]    # ['Article', 'TimestampMixin', 'ValidationMixin', 'Saver', 'object']
```

Každý mixin udělá svůj krok a předá řízení dál. Pořadí v hlavičce určuje
pořadí kroků. Když `ValidationMixin` validaci neprojde, `super().save()`
nezavolá a řetěz se zastaví.

## 8. Mixiny v Djangu

Django class-based views jsou celé postavené z mixinů. `ListView` sám
je jen složení:

```
ListView = MultipleObjectTemplateResponseMixin + BaseListView
BaseListView = MultipleObjectMixin + View
```

Ty pak přidáváš vlastní mixiny vlevo:

```python
class BookListView(LoginRequiredMixin, ListView):     # Django, jen pro ilustraci
    model = Book
```

Jak to funguje, si můžeš napsat sám ve zjednodušené podobě:

```python
class View:
    def dispatch(self, request):
        return self.get(request)


class LoginRequiredMixin:
    def dispatch(self, request):
        if request.get("user") is None:
            return "302 /login/"
        return super().dispatch(request)


class BookListView(LoginRequiredMixin, View):
    def get(self, request):
        return f"200 seznam knih pro {request['user']}"


view = BookListView()
view.dispatch({"user": "anna"})      # '200 seznam knih pro anna'
view.dispatch({})                    # '302 /login/'
```

`LoginRequiredMixin.dispatch` je v MRO před `View.dispatch`, takže
proběhne první. Když je uživatel přihlášený, pustí request dál přes
`super()`. Kdyby byl mixin vpravo (`class BookListView(View,
LoginRequiredMixin)`), `View.dispatch` by se našel dřív a kontrola
přihlášení by se **nikdy nezavolala**. Proto Django dokumentace
opakuje: mixiny vlevo.

Další mixiny, které v Djangu potkáš: `PermissionRequiredMixin`,
`UserPassesTestMixin`, `SuccessMessageMixin`, `FormMixin`,
`SingleObjectMixin`.

## 9. Kdy mixiny nepoužívat

- **Mixin s vlastním stavem a povinným `__init__`**: to už je
  plnohodnotná třída a skládání se rozbije. Zvaž kompozici
  ([`INHERITANCE_AND_SUPER.md`](INHERITANCE_AND_SUPER.md#10-kompozice-vs-dědičnost)).
- **Hluboké hierarchie**: pět mixinů, které všechny přepisují
  `dispatch`, se čtou těžko. Každý krok skládání přidává místo, kde
  hledat chybu.
- **Pomocná funkce stačí**: když mixin nepotřebuje `self` ani jiné
  metody třídy, je to obyčejná funkce, ne třída.
- **Schopnost potřebuje jen jedna třída**: napiš metodu přímo do ní.

Rada: mixin piš, až když stejnou schopnost potřebuješ aspoň ve dvou
nesouvisejících třídách.

## 10. Srovnání s JS

| Python | JS |
|---|---|
| `class C(A, B):` | neexistuje, třída má jen jeden `extends` |
| mixin třída v hlavičce | mixin funkce: `const C = JsonMixin(ReprMixin(Base))` |
| MRO (`C.__mro__`) | řetěz prototypů, vždy lineární |
| kooperativní `super()` přes MRO | `super` vede vždy na přímého rodiče v řetězu |
| `Object.assign(C.prototype, mixin)` | (bez `super`, metody se jen zkopírují) |

JS mixin vzor `const Mixin = (Base) => class extends Base {...}`
vyrábí ve skutečnosti lineární řetěz, který odpovídá Python MRO:
`JsonMixin(ReprMixin(Base))` je v Pythonu `class C(JsonMixin, ReprMixin,
Base)`.

## 11. Časté chyby

| Příznak | Příčina |
|---|---|
| kontrola v mixinu se vůbec nezavolá | mixin je v hlavičce vpravo od základní třídy, ta se najde dřív |
| metoda jedné z rodičovských tříd se přeskočí | některá třída v řetězu nevolá `super()`, nebo volá rodiče natvrdo (`Base.save(self)`) |
| metoda společného předka proběhne dvakrát | volání natvrdo `Left.f(self)`, `Right.f(self)` místo `super()` |
| `TypeError: object.__init__() takes exactly one argument (the instance to initialize)` | v kooperativním `__init__` zůstal nespotřebovaný argument v `**kwargs` |
| `TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B` | obecnější třída je v hlavičce vlevo od své podtřídy |
| `TypeError: X.__init__() missing 1 required positional argument` u mixinu | mixin má vlastní `__init__` s povinným argumentem a řetěz `super()` mu ho nepředal |
| nevíš, odkud se metoda bere | vypiš `[c.__name__ for c in Třída.__mro__]` a hledej shora |
