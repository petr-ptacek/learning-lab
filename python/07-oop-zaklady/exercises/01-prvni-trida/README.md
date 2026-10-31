# 01 — První třída

Data a funkce, které s nimi pracují, v jednom typu. Položka na skladě
jako objekt místo dictu `{"name": ..., "price": ...}`.

## Požadavky

- Napiš třídu `Product` s `__init__(self, name, price, quantity=0)`,
  která uloží tři atributy instance: `name`, `price`, `quantity`.
- Metody:
  - `total_value()` — cena × množství, zaokrouhlené na 2 místa.
  - `restock(amount)` — přidá kusy na sklad. Nic nevrací.
  - `sell(amount)` — když je na skladě dost kusů, odečte je a vrátí
    `True`. Jinak nic nezmění a vrátí `False`.
- **Předpověď:** napiš si odpověď do komentáře, pak spusť:

  ```python
  a = Product("Mléko", 24.9, 10)
  b = Product("Chléb", 39.0)
  a.sell(3)
  print(a.quantity, b.quantity)
  print(a == Product("Mléko", 24.9, 7))
  print(a)
  print(Product.total_value(a) == a.total_value())
  ```

  Proč je druhý řádek `False`, i když mají oba objekty stejná data?
  Co vypíše třetí řádek? A proč čtvrtý funguje, když `total_value`
  bere parametr `self`?

### Příklady vstup/výstup

Každý řádek začíná s `p = Product("Mléko", 24.9, 10)`:

| Kód                                       | Výsledek                         |
|-------------------------------------------|----------------------------------|
| `p.total_value()`                         | `249.0`                          |
| `p.restock(5)`, pak `p.quantity`          | `15`                             |
| `p.sell(4)`, pak `p.quantity`             | `True`, `6`                      |
| `p.sell(20)`, pak `p.quantity`            | `False`, `10` (nic se nezměnilo) |
| `p.sell(10)`, pak `p.quantity`            | `True`, `0`                      |
| `p.sell(0)`                               | `True`                           |
| `Product("Sůl", 12.5).total_value()`      | `0.0`                            |
| `Product("Sůl", 12.5).quantity`           | `0`                              |
| `Product("x")`                            | `TypeError: Product.__init__() missing 1 required positional argument: 'price'` |

## Bonus

- `apply_discount(percent)` — sníží cenu o dané procento, zaokrouhlí na
  2 místa a uloží ji do `price`.
- **Předpověď:** co se stane, když v definici metody zapomeneš `self`?

  ```python
  class Broken:
      def hello():
          return "ahoj"


  Broken().hello()
  ```

  Přečti si chybovou hlášku a vysvětli ji komentářem: kdo je ten
  „1 given“ argument?

### Příklady vstup/výstup (bonus)

| Kód                                                          | Výsledek          |
|--------------------------------------------------------------|-------------------|
| `q = Product("Káva", 189.0, 3)`, `q.apply_discount(10)`, `q.price` | `170.1`     |
| …a pak `q.total_value()`                                     | `510.3`           |
| `q.apply_discount(0)`, `q.price`                             | beze změny        |
| `Product("Čaj", 59.9, 2)` se slevou `100`, `.price`          | `0.0`             |
