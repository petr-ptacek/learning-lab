# 08 — Deskriptory: znovupoužitelná validace atributů

`@property` hlídá **jeden** atribut jedné třídy. Když chceš stejnou
kontrolu („nesmí být záporné“) na `price`, `quantity` i `weight`
v několika třídách, napíšeš ji jednou jako **deskriptor**. To je
objekt uložený jako atribut třídy, který převezme čtení a zápis
toho atributu na instancích.

Přesně tohle jsou Django pole. `title = models.CharField(max_length=200)`
je objekt na třídě a `book.title` čte hodnotu konkrétní knihy. Sama
`property` je taky deskriptor.

Teorie: [`docs/DESCRIPTORS.md`](../../../docs/DESCRIPTORS.md).

## Požadavky

- Deskriptor `PositiveNumber`:
  - `__set_name__(self, owner, name)` — zapamatuje si jméno atributu,
    pod kterým je na třídě uložený (Python ho zavolá sám při vzniku
    třídy),
  - `__get__(self, obj, objtype=None)` — když `obj is None` (čtení
    přes třídu), vrátí sám sebe. Jinak hodnotu z `obj.__dict__[self.name]`,
  - `__set__(self, obj, value)` — záporné číslo odmítne přes
    `ValueError(f"{self.name} nesmí být záporné: {value}")`, jinak
    hodnotu uloží do `obj.__dict__[self.name]`.
- Deskriptor `String(max_length)`:
  - ne-string → `TypeError(f"{self.name} musí být text, ne {typ}")`
    (`typ` je jméno typu, třeba `int`),
  - delší než `max_length` →
    `ValueError(f"{self.name} může mít nejvýš {max_length} znaků")`.
- `Product(name, price, quantity=0)` s atributy třídy
  `name = String(max_length=10)`, `price = PositiveNumber()`,
  `quantity = PositiveNumber()` a `__repr__` → `Product('Mléko', 24.9, 10)`.
  `__init__` jen přiřazuje `self.price = price` a podobně, validace
  proběhne sama.
- **Předpověď:** co vypíše?

  ```python
  p = Product("Mléko", 24.9, 10)
  print(Product.price)
  print(vars(p))
  print("price" in vars(Product), "price" in vars(p))
  p.price = -1
  ```

  `price` je teď v `vars(p)` **i** ve `vars(Product)`. Ze cvičení 02
  v `07-oop-zaklady` víš, že zápis `obj.x = ...` jde do instance. Proč
  tedy `p.price = -1` neskončí rovnou v `p.__dict__`, ale vyhodí chybu?
  Nápověda: pořadí hledání atributu, když je na třídě objekt
  s metodou `__set__`.

### Příklady vstup/výstup

| Kód                                           | Výsledek                                              |
|-----------------------------------------------|-------------------------------------------------------|
| `p = Product("Mléko", 24.9, 10)`, `p`          | `Product('Mléko', 24.9, 10)`                          |
| `vars(p)`                                     | `{'name': 'Mléko', 'price': 24.9, 'quantity': 10}`    |
| `type(Product.price).__name__, Product.price.name` | `('PositiveNumber', 'price')`                    |
| `Product.name.max_length`                     | `10`                                                  |
| `Product("Sůl", 0)`                           | `Product('Sůl', 0, 0)` (nula je v pořádku)            |
| `p.price = 30`, `p.price`                     | `30`                                                  |
| `p.price = -1`                                | `ValueError: price nesmí být záporné: -1`             |
| …a pak `p.price`                              | `30` (nic se nezměnilo)                               |
| `Product("Chléb", -5)`                        | `ValueError: price nesmí být záporné: -5`             |
| `Product("Mléko", 10, -1)`                    | `ValueError: quantity nesmí být záporné: -1`          |
| `Product("Čokoláda hořká", 50)`               | `ValueError: name může mít nejvýš 10 znaků`           |
| `Product(42, 10)`                             | `TypeError: name musí být text, ne int`               |
| `q = Product("Káva", 189.0)`, `p.price, q.price` | `(30, 189.0)` (jeden deskriptor, každá instance vlastní hodnotu) |

## Bonus

- Vlastní `cached` — deskriptor, který funguje jako
  `functools.cached_property` (`04-property` v `07-oop-zaklady`):
  - dekorátor nad metodou: `__init__(self, func)`,
  - má **jen** `__get__` (je to tzv. *non-data* deskriptor).
    Spočítá `self.func(obj)`, výsledek uloží do `obj.__dict__` pod
    svým jménem a vrátí ho.
  - **Otázka:** proč se při druhém čtení `__get__` vůbec nezavolá?
    A proč by to nefungovalo, kdyby `cached` měl i `__set__`?
- Deskriptor `Choice(*options)` — hodnota musí být jedna z možností,
  jinak `ValueError(f"{self.name} musí být jedno z: 'new', 'paid', 'shipped'")`
  (možnosti přes `repr`, oddělené čárkou). Django má totéž jako
  `choices=` u pole.

```python
class Report:
    def __init__(self, numbers):
        self.numbers = numbers

    @cached
    def total(self):
        print("počítám…")
        return sum(self.numbers)


class Order:
    status = Choice("new", "paid", "shipped")

    def __init__(self, status="new"):
        self.status = status
```

### Příklady vstup/výstup (bonus)

| Kód                                          | Výsledek                                           |
|----------------------------------------------|----------------------------------------------------|
| `r = Report([10, 20, 30])`, `r.total`        | vypíše `počítám…`, vrátí `60`                      |
| znovu `r.total`                              | `60` bez výpisu                                    |
| `vars(r)`                                    | `{'numbers': [10, 20, 30], 'total': 60}`           |
| `r.numbers.append(40)`, `r.total`            | `60` (pořád z cache)                               |
| `del r.total`, `r.total`                     | vypíše `počítám…`, vrátí `100`                     |
| `type(Report.total).__name__`                | `'cached'`                                         |
| `Order().status`                             | `'new'`                                            |
| `o.status = "paid"`, `vars(o)`               | `{'status': 'paid'}`                               |
| `o.status = "lost"`                          | `ValueError: status musí být jedno z: 'new', 'paid', 'shipped'` |
| `Order("NEW")`                               | `ValueError: status musí být jedno z: 'new', 'paid', 'shipped'` |
| `hasattr(cached, "__set__"), hasattr(Choice, "__set__")` | `(False, True)`                        |
