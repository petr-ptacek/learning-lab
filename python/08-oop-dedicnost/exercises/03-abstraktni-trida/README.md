# 03 — Abstraktní třída

Základ, ze kterého se nedá vyrobit instance. Jen předepisuje, co musí
každá podtřída umět, a nabízí společný kód. Podobně fungují Django
abstraktní modely (`class Meta: abstract = True`) a hlavně class-based
views: rodič má hotový postup (`get` → `get_queryset` →
`get_context_data`) a ty doplníš jen kousky.

Teorie: [`docs/ABSTRACT_BASE_CLASSES.md`](../../../docs/ABSTRACT_BASE_CLASSES.md).

## Požadavky

- `Shape(ABC)` (`from abc import ABC, abstractmethod`):
  - abstraktní metody `area()` a `perimeter()`,
  - konkrétní `describe()` → `"Circle: obsah 78.54, obvod 31.42"`
    (jméno třídy přes `type(self).__name__`, čísla na 2 místa).
    Napíšeš ji **jednou** v `Shape` a funguje pro všechny tvary,
    i když `Shape` sama obsah spočítat neumí.
  - `__lt__` podle obsahu (pro jiný typ `NotImplemented`). Díky tomu
    fungují `sorted`, `min`, `max` pro libovolné tvary dohromady.
- `Circle(radius)`, `Rectangle(width, height)`.
- `Square(side)` jako podtřída **`Rectangle`**: jen `__init__`, který
  zavolá `super().__init__(side, side)`. Obsah ani obvod nepiš znovu.
- **Předpověď:** co se stane?

  ```python
  Shape()


  class Triangle(Shape):
      def __init__(self, a):
          self.a = a

      def area(self):
          return self.a


  Triangle(3)
  ```

  Kdy přesně Python chybu ohlásí: při definici `class Triangle`, nebo
  až při vytvoření instance? Proč je to lepší, než kdyby `Shape`
  obsahovala `perimeter`, která jen tak vrátí `0`?

### Příklady vstup/výstup

| Kód                                          | Výsledek                                    |
|----------------------------------------------|---------------------------------------------|
| `Circle(5).describe()`                       | `'Circle: obsah 78.54, obvod 31.42'`        |
| `Rectangle(3, 4).describe()`                 | `'Rectangle: obsah 12.00, obvod 14.00'`     |
| `Square(2).describe()`                       | `'Square: obsah 4.00, obvod 8.00'`          |
| `Circle(0).describe()`                       | `'Circle: obsah 0.00, obvod 0.00'`          |
| `Square(3).width, Square(3).height`          | `(3, 3)`                                    |
| `isinstance(Square(1), Rectangle), isinstance(Square(1), Shape)` | `(True, True)`          |
| `[c.__name__ for c in Square.__mro__]`       | `['Square', 'Rectangle', 'Shape', 'ABC', 'object']` |
| `Shape()`                                    | `TypeError: Can't instantiate abstract class Shape without an implementation for abstract methods 'area', 'perimeter'` |
| `Triangle(3)` (z předpovědi)                 | `TypeError: Can't instantiate abstract class Triangle without an implementation for abstract method 'perimeter'` |
| `Circle(1) < Square(2)`, `Square(2) < Circle(1)` | `(True, False)`                         |
| `Circle(1) > Square(1)`                      | `True` (bez psaní `__gt__`)                 |
| `[type(s).__name__ for s in sorted([Circle(1), Square(3), Rectangle(1, 2)])]` | `['Rectangle', 'Circle', 'Square']` |
| `max([Circle(1), Square(3), Rectangle(1, 2)]).describe()` | `'Square: obsah 9.00, obvod 12.00'` |
| `Circle(1) < 5`                              | `TypeError: '<' not supported between instances of 'Circle' and 'int'` |

## Bonus

Vzor **template method**: rodič má hotový postup a volá v něm metody,
které doplní podtřída. Přesně takhle je postavené Django `ListView`.

- `Report(ABC)`:
  - konkrétní `render(rows)` → string: řádek z `header()`, pak jeden
    řádek z `format_row(row)` pro každý záznam, nakonec `footer(rows)`,
    **jen pokud** není prázdný. Řádky spoj `"\n"`.
  - abstraktní `header()` a `format_row(row)`,
  - `footer(rows)` je **háček** (hook): v `Report` vrací `""`, podtřída
    ho smí, ale nemusí přepsat.
- `CsvReport`: hlavička `name;price`, řádek `Mléko;24.9`. Patičku nemá.
- `MarkdownReport`: hlavička jako tabulka v Markdownu, řádek
  `| Mléko | 24.9 |`, patička `"\nCelkem položek: 2"`.
- **Otázka:** kolik řádků kódu by se opakovalo, kdyby si každý report
  psal celé `render` sám? Kterou metodu bys přepsal, kdybys chtěl report,
  který řádky čísluje?

### Příklady vstup/výstup (bonus)

`ROWS = [{"name": "Mléko", "price": 24.9}, {"name": "Chléb", "price": 39.0}]`

| Kód                              | Výsledek                                                                          |
|----------------------------------|-----------------------------------------------------------------------------------|
| `CsvReport().render(ROWS)`       | `'name;price\nMléko;24.9\nChléb;39.0'`                                            |
| `CsvReport().render([])`         | `'name;price'`                                                                    |
| `MarkdownReport().render(ROWS)`  | `'\| Název \| Cena \|\n\|---\|---\|\n\| Mléko \| 24.9 \|\n\| Chléb \| 39.0 \|\n\nCelkem položek: 2'` |
| `MarkdownReport().render([])`    | `'\| Název \| Cena \|\n\|---\|---\|\n\nCelkem položek: 0'`                        |
| `Report()`                       | `TypeError: Can't instantiate abstract class Report without an implementation for abstract methods 'format_row', 'header'` |

`print(MarkdownReport().render(ROWS))` vypíše:

```
| Název | Cena |
|---|---|
| Mléko | 24.9 |
| Chléb | 39.0 |

Celkem položek: 2
```
