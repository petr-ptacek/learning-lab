# 07 — `__init_subclass__`: rodič, který ví o svých potomcích

`__init_subclass__` je metoda rodiče, kterou Python zavolá pokaždé, když
**vznikne podtřída**. Ne při vytvoření instance, ale už při definici
`class ...`. Hodí se na registr („všechny exportéry“), na kontrolu, že
podtřída má, co má mít, nebo na posbírání atributů třídy. To poslední
dělá Django s poli modelu, v bonusu si to vyzkoušíš.

Teorie: [`docs/CLASS_CREATION_AND_METACLASSES.md`](../../../docs/CLASS_CREATION_AND_METACLASSES.md).

## Požadavky

- Třída `Exporter`:
  - atribut třídy `registry = {}`: formát → třída exportéru,
  - `__init_subclass__(cls, *, format, **kwargs)`:
    - zavolá `super().__init_subclass__(**kwargs)`,
    - když už je formát v registru, vyhodí
      `ValueError(f"Formát {format!r} už je registrovaný")`,
    - jinak uloží `cls.format = format` a zapíše třídu do registru,
  - `@classmethod for_format(cls, format)` → **instance** exportéru
    pro daný formát,
  - `export(self, rows)` → `raise NotImplementedError`. Podtřídy ho
    přepíšou.
- Formát se předává v **hlavičce třídy**, jako pojmenovaný argument:

  ```python
  class CsvExporter(Exporter, format="csv"):
      ...
  ```

- `CsvExporter.export(rows)` → text: hlavička z klíčů prvního řádku
  a pak hodnoty, oddělené `;`, řádky `\n`. Pro prázdný seznam `""`.
- `JsonExporter` (`format="json"`): `json.dumps(rows, ensure_ascii=False)`.
- **Předpověď:** co se stane a **kdy**: při definici třídy, nebo až při
  jejím použití?

  ```python
  class Duplicate(Exporter, format="csv"):
      pass


  class NoFormat(Exporter):
      pass
  ```

  Má atribut `format` i samotný `Exporter`? Proč?

### Příklady vstup/výstup

`ROWS = [{"name": "Mléko", "price": 24.9}, {"name": "Chléb", "price": 39}]`

| Kód                                          | Výsledek                                           |
|----------------------------------------------|----------------------------------------------------|
| `Exporter.registry`                          | `{'csv': <class '__main__.CsvExporter'>, 'json': <class '__main__.JsonExporter'>}` |
| `CsvExporter.format, JsonExporter.format`    | `('csv', 'json')`                                  |
| `type(Exporter.for_format("json")).__name__` | `'JsonExporter'`                                   |
| `Exporter.for_format("csv").export(ROWS)`    | `'name;price\nMléko;24.9\nChléb;39'`               |
| `Exporter.for_format("json").export(ROWS)`   | `'[{"name": "Mléko", "price": 24.9}, {"name": "Chléb", "price": 39}]'` |
| `Exporter.for_format("csv").export([])`      | `''`                                               |
| `Exporter.for_format("json").export([])`     | `'[]'`                                             |
| `Exporter.for_format("xml")`                 | `KeyError: 'xml'`                                  |
| `hasattr(Exporter, "format")`                | `False`                                            |
| definice `Duplicate` (viz výše)              | `ValueError: Formát 'csv' už je registrovaný`      |
| definice `NoFormat` (viz výše)               | `TypeError: Exporter.__init_subclass__() missing 1 required keyword-only argument: 'format'` |
| `sorted(Exporter.registry)` po obou chybách  | `['csv', 'json']` (nic nepřibylo)                  |

## Bonus

Předobraz Django modelu: pole popsaná atributy třídy a rodič, který si
je při vzniku podtřídy posbírá.

- `Field(default=None)` — jen si pamatuje `default`.
- `Schema`:
  - `__init_subclass__` posbírá všechny atributy typu `Field` do
    `cls._fields` (dict jméno → `Field`), **včetně zděděných**. Pole
    rodičů jsou první, potomek může pole přepsat. Nápověda:
    `reversed(cls.__mro__)` a `vars(klass)`.
  - `__init__(self, **values)` — každé pole nastaví na zadanou
    hodnotu, nebo na `default`. Neznámé jméno →
    `TypeError("Neznámé pole: a, b")` (seřazená, oddělená čárkou).
  - `__repr__` → `Product(name='Mléko', price=24.9, in_stock=True)`
    v pořadí polí.
- **Otázka:** po `Product(name="x")` je `Product.price` pořád `Field`,
  ale `p.price` je `0`. Proč? (Cvičení 02 z `07-oop-zaklady`.)

```python
class Product(Schema):
    name = Field()
    price = Field(default=0)
    in_stock = Field(default=True)


class Food(Product):
    expires = Field()
    price = Field(default=10)
```

### Příklady vstup/výstup (bonus)

| Kód                                           | Výsledek                                                     |
|-----------------------------------------------|--------------------------------------------------------------|
| `list(Product._fields)`                       | `['name', 'price', 'in_stock']`                              |
| `list(Food._fields)`                          | `['name', 'price', 'in_stock', 'expires']`                   |
| `Product(name="Mléko", price=24.9)`           | `Product(name='Mléko', price=24.9, in_stock=True)`           |
| `Product()`                                   | `Product(name=None, price=0, in_stock=True)`                 |
| `Food(name="Jogurt", expires="2026-12-01")`   | `Food(name='Jogurt', price=10, in_stock=True, expires='2026-12-01')` |
| `vars(Product(name="x"))`                     | `{'name': 'x', 'price': 0, 'in_stock': True}`                |
| `Product(nazev="Mléko")`                      | `TypeError: Neznámé pole: nazev`                             |
| `Product(name="x", colour="red", size=1)`     | `TypeError: Neznámé pole: colour, size`                      |
| `hasattr(Schema, "_fields")`                  | `False` (sbírá se jen u podtříd)                             |
