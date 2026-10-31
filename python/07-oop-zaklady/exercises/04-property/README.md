# 04 — `@property`

Metoda, která se čte jako atribut: dopočítané hodnoty, validace při
zápisu, atributy jen pro čtení. V Django modelech typicky
`full_name`, `is_paid`, `price_with_vat`.

Teorie: [`docs/METHODS_AND_PROPERTIES.md`](../../../docs/METHODS_AND_PROPERTIES.md),
sekce 5–9.

## Požadavky

- `Temperature(celsius)`:
  - property `fahrenheit` (čtení i zápis): `°F = °C × 9/5 + 32`,
    zaokrouhleno na 2 místa. Zápis přepočítá a uloží `celsius`.
  - property `kelvin` jen pro čtení: `K = °C + 273.15`, 2 místa.
  - Ukládej **jen** `celsius`, ostatní se vždy dopočítají.
- `Person(first_name, last_name)`:
  - property `full_name` → `"Anna Nováková"`. Setter rozdělí text na
    jméno a příjmení podle **první** mezery (zbytek je příjmení).
  - property `initials` jen pro čtení → `"A. N."`.
- `Product(name, price)`: `price` jako property se setterem, který
  záporné číslo odmítne přes `raise ValueError("Cena nesmí být
  záporná")` a jinak cenu zaokrouhlí na 2 místa. Validace musí platit
  **i v `__init__`**. Hodnotu ukládej do `self._price`.
- **Předpověď:** co vypíše / jakou chybu vyhodí?

  ```python
  t = Temperature(25)
  print(t.fahrenheit)
  t.kelvin = 0
  ```

  ```python
  t = Temperature(25)
  t.fahrenheit()
  ```

### Příklady vstup/výstup

| Kód                                                     | Výsledek                                                          |
|---------------------------------------------------------|-------------------------------------------------------------------|
| `t = Temperature(25)`, `t.fahrenheit, t.kelvin`         | `(77.0, 298.15)`                                                  |
| `t.fahrenheit = 212`, `t.celsius`                       | `100.0`                                                           |
| `Temperature(-40).fahrenheit`                           | `-40.0`                                                           |
| `Temperature(0).fahrenheit, Temperature(0).kelvin`      | `(32.0, 273.15)`                                                  |
| `Temperature(37).fahrenheit`                            | `98.6`                                                            |
| `Temperature(-273.15).kelvin`                           | `0.0`                                                             |
| `t.kelvin = 0`                                          | `AttributeError: property 'kelvin' of 'Temperature' object has no setter` |
| `t.fahrenheit()`                                        | `TypeError: 'float' object is not callable`                       |

| Kód                                                     | Výsledek                         |
|---------------------------------------------------------|----------------------------------|
| `p = Person("Anna", "Nováková")`, `p.full_name, p.initials` | `('Anna Nováková', 'A. N.')` |
| `p.last_name = "Dvořáková"`, `p.full_name`              | `'Anna Dvořáková'`               |
| `p.full_name = "Jan Amos Komenský"`, `p.first_name, p.last_name` | `('Jan', 'Amos Komenský')` |
| …a `p.initials`                                         | `'J. A.'`                        |

| Kód                                                     | Výsledek                                     |
|---------------------------------------------------------|----------------------------------------------|
| `x = Product("Mléko", 24.999)`, `x.price`               | `25.0`                                       |
| `vars(x)`                                               | `{'name': 'Mléko', '_price': 25.0}`          |
| `x.price = 0`, `x.price`                                | `0`                                          |
| `x.price = -5`                                          | `ValueError: Cena nesmí být záporná`         |
| `Product("Chyba", -1)`                                  | `ValueError: Cena nesmí být záporná`         |

## Bonus

`cached_property` (`from functools import cached_property`). Django má
vlastní se stejným chováním: `django.utils.functional.cached_property`.

- `Report(numbers)`:
  - `total` jako `@cached_property`. Při výpočtu vypíše `počítám…`,
    takže uvidíš, kolikrát se doopravdy počítá.
  - `average` jako obyčejná `@property` (2 místa, pro prázdný seznam
    `0`), využije `total`.
- **Předpověď:** co vypíše?

  ```python
  r = Report([10, 20, 30, 45])
  print(r.total)
  print(r.total)
  print(r.average)
  r.numbers.append(100)
  print(r.total)
  del r.total
  print(r.total)
  ```

  Proč je čtvrtý výpis „špatně“? Kdy je to v pořádku a kdy je to
  chyba? Kam se vlastně hodnota uložila? (`vars(r)`)

### Příklady vstup/výstup (bonus)

| Kód                                    | Výsledek                       |
|----------------------------------------|--------------------------------|
| `Report([10, 20, 30, 45]).total`       | vypíše `počítám…`, vrátí `105` |
| `Report([10, 20, 30, 45]).average`     | `26.25`                        |
| `Report([]).average`                   | `0`                            |
