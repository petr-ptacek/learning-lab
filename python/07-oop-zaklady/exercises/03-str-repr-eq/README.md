# 03 — `__str__`, `__repr__`, `__eq__`

Jak se objekt vypíše a kdy jsou dva objekty „stejné“. V Djangu je
`__str__` to, co vidíš v adminu a ve formulářích místo `Book object (1)`.

Teorie: [`docs/DUNDER_METHODS.md`](../../../docs/DUNDER_METHODS.md),
sekce 1–3 a 5.

## Požadavky

- Napiš třídu `Money` s `__init__(self, amount, currency="CZK")`.
- `__str__` → částka na 2 desetinná místa a měna: `249.90 CZK`.
- `__repr__` → zápis, kterým se objekt vyrobí: `Money(249.9, 'CZK')`.
  Použij `!r` ve f-stringu.
- `__eq__` → stejná částka **a** stejná měna. Pro jiný typ než
  `Money` vrať `NotImplemented`.
- `__add__` → nová `Money` se součtem (zaokrouhleným na 2 místa).
  Jen pro stejnou měnu, jinak `NotImplemented`.
- **Předpověď:** před napsáním dunder metod spusť s prázdnou třídou
  (jen `__init__`) a pak s hotovou. Co se změní?

  ```python
  m = Money(249.9)
  print(m)
  print([m, Money(10, "EUR")])
  print(f"Celkem: {m}, ladění: {m!r}")
  print(m == Money(249.9))
  ```

  Proč seznam nepoužije `__str__`?

### Příklady vstup/výstup

| Kód                                         | Výsledek                                                    |
|---------------------------------------------|-------------------------------------------------------------|
| `str(Money(249.9))`                         | `'249.90 CZK'`                                              |
| `str(Money(0, "EUR"))`                      | `'0.00 EUR'`                                                |
| `str(Money(1234567.5))`                     | `'1234567.50 CZK'`                                          |
| `repr(Money(249.9))`                        | `"Money(249.9, 'CZK')"`                                     |
| `[Money(10, "EUR")]`                        | `[Money(10, 'EUR')]`                                        |
| `Money(10, "EUR") == Money(10, "EUR")`      | `True`                                                      |
| `Money(10, "EUR") == Money(10, "CZK")`      | `False`                                                     |
| `Money(10) == 10`                           | `False`                                                     |
| `Money(10) != Money(11)`                    | `True` (bez psaní `__ne__`)                                 |
| `Money(249.9) + Money(0.1)`                 | `Money(250.0, 'CZK')`                                       |
| `Money(0.1) + Money(0.2)`                   | `Money(0.3, 'CZK')`                                         |
| `Money(1) + Money(1, "EUR")`                | `TypeError: unsupported operand type(s) for +: 'Money' and 'Money'` |
| `Money(1) + 5`                              | `TypeError: unsupported operand type(s) for +: 'Money' and 'int'`   |

## Bonus

- **Předpověď:** co udělá `{Money(1), Money(1)}`? Spusť a vysvětli
  chybu. Pak doplň `__hash__`, aby objekty s `==` měly stejný hash.
- `__lt__` (jen stejná měna) → funguje `sorted`, `min`, `max`.
- `__bool__` → nulová částka je `False`.
- `__radd__` → aby fungovalo `sum(seznam_peněz)` bez druhého argumentu.
  Proč bez ní `sum` spadne? (Nápověda: od čeho `sum` začíná sčítat?)

### Příklady vstup/výstup (bonus)

`prices = [Money(30), Money(10.5), Money(20)]`

| Kód                                       | Výsledek                                                     |
|-------------------------------------------|--------------------------------------------------------------|
| `len({Money(1), Money(1), Money(2, "EUR")})` | `2`                                                       |
| `sorted(prices)`                          | `[Money(10.5, 'CZK'), Money(20, 'CZK'), Money(30, 'CZK')]`   |
| `str(max(prices)), str(min(prices))`      | `('30.00 CZK', '10.50 CZK')`                                 |
| `Money(5) > Money(3)`                     | `True`                                                       |
| `Money(1) < Money(1, "EUR")`              | `TypeError: '<' not supported between instances of 'Money' and 'Money'` |
| `bool(Money(0)), bool(Money(0.01))`       | `(False, True)`                                              |
| `str(sum(prices))`                        | `'60.50 CZK'`                                                |
| `sum([])`                                 | `0`                                                          |
