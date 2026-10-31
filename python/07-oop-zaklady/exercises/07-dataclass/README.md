# 07 — `@dataclass`

Třída na data bez psaní `__init__`, `__repr__` a `__eq__`. Princip
„popíšu pole na třídě, zbytek se vygeneruje“ je stejný jako u Django
modelů.

Teorie: [`docs/DATACLASSES.md`](../../../docs/DATACLASSES.md).

## Požadavky

- Přepiš `Product` jako `@dataclass`: pole `name: str`,
  `price: float`, `quantity: int = 0`, `tags: list[str]` s prázdným
  seznamem jako výchozí hodnotou. Metoda `total_value()` zůstává.
- **Předpověď:** co se stane, když napíšeš `tags: list[str] = []`?
  Zkus to a přečti chybu. Proč to dataclass zakazuje? (Vzpomeň na
  `Cart` ze cvičení 02.)
- `Point(x, y)` jako `@dataclass(frozen=True)`, metoda
  `distance_to(other)` (vzdálenost, 2 místa). Body jde dávat do setu
  a používat jako klíč dictu.
- `Version(major, minor, patch=0)` jako `@dataclass(order=True,
  frozen=True)`:
  - `@classmethod parse(cls, text)` z `"1.10.0"` nebo `"2.0"`,
  - `__str__` → `"1.10.0"`.
- `Email(address)` jako `@dataclass`. V `__post_init__` adresu očisti
  (`strip`, malá písmena). Property `domain` → část za `@`.

### Příklady vstup/výstup

| Kód                                              | Výsledek                                                     |
|--------------------------------------------------|--------------------------------------------------------------|
| `Product("Mléko", 24.9, 10)`                     | `Product(name='Mléko', price=24.9, quantity=10, tags=[])`    |
| `Product("Mléko", 24.9, 10).total_value()`       | `249.0`                                                      |
| `Product("Mléko", 24.9) == Product("Mléko", 24.9)` | `True`                                                     |
| `Product("Mléko", 24.9) == Product("Mléko", 25)` | `False`                                                      |
| `b = Product("Chléb", 39.0)`, `b.tags.append("pečivo")`, pak `Product("Sůl", 12.5).tags` | `[]`              |

| Kód                                              | Výsledek                                         |
|--------------------------------------------------|--------------------------------------------------|
| `Point(0, 0).distance_to(Point(3, 4))`           | `5.0`                                            |
| `p = Point(0, 0)`, `p.x = 5`                     | `FrozenInstanceError: cannot assign to field 'x'`|
| `len({Point(0, 0), Point(1, 2), Point(0, 0)})`   | `2`                                              |
| `{Point(0, 0): "start"}[Point(0, 0)]`            | `'start'`                                        |
| `{Product("x", 1)}`                              | `TypeError: cannot use 'Product' as a set element (unhashable type: 'Product')` |

| Kód                                                     | Výsledek                                       |
|---------------------------------------------------------|------------------------------------------------|
| `str(Version.parse("1.10.0"))`                          | `'1.10.0'`                                     |
| `Version.parse("2.0")`                                  | `Version(major=2, minor=0, patch=0)`           |
| `Version.parse("1.10.0") > Version.parse("1.9.3")`      | `True`                                         |
| `"1.10.0" > "1.9.3"`                                    | `False` (proč?)                                |
| seřazené `["1.10.0", "1.2.3", "1.9.3", "0.9"]` jako stringy přes `str` | `['0.9.0', '1.2.3', '1.9.3', '1.10.0']` |
| `Version(1, 2) == Version(1, 2, 0)`                     | `True`                                         |

| Kód                                                     | Výsledek                                        |
|---------------------------------------------------------|-------------------------------------------------|
| `Email("  Anna.Novakova@Example.CZ ")`                  | `Email(address='anna.novakova@example.cz')`     |
| `Email("  Anna.Novakova@Example.CZ ").domain`           | `'example.cz'`                                  |
| `Email("A@B.cz") == Email("a@b.CZ ")`                   | `True`                                          |

## Bonus

- `asdict` a JSON: převeď `Product("Káva", 189.0, 3, ["bio"])` na dict
  a pak na JSON string (viz `docs/JSON.md`, české znaky bez escapování).
- `replace`: z kávy vyrob novou instanci s cenou `169.0`. Původní
  zůstane beze změny.
- `User(username, password, is_active=True)`. Heslo se nesmí objevit
  v `repr` (`field(repr=False)`).

### Příklady vstup/výstup (bonus)

| Kód                                                  | Výsledek                                                              |
|------------------------------------------------------|-----------------------------------------------------------------------|
| `asdict(Product("Káva", 189.0, 3, ["bio"]))`         | `{'name': 'Káva', 'price': 189.0, 'quantity': 3, 'tags': ['bio']}`    |
| JSON z toho                                          | `{"name": "Káva", "price": 189.0, "quantity": 3, "tags": ["bio"]}`    |
| `c = Product("Káva", 189.0, 3)`, `d = replace(c, price=169.0)`, `c.price, d.price` | `(189.0, 169.0)`                    |
| `User("anna", "tajne123")`                           | `User(username='anna', is_active=True)`                               |
| `User("anna", "tajne123").password`                  | `'tajne123'`                                                          |
