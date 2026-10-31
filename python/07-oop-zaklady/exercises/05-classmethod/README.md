# 05 — `@classmethod` a `@staticmethod`

Alternativní konstruktory (`from_dict`, `from_csv_line`) a funkce, které
patří ke třídě. V bonusu si napíšeš mini verzi Django
`Book.objects.create(...)` / `.filter(...)`.

Teorie: [`docs/METHODS_AND_PROPERTIES.md`](../../../docs/METHODS_AND_PROPERTIES.md),
sekce 1–4.

## Požadavky

- Třída `Product(name, price, quantity=0)` s `__repr__` ve tvaru
  `Product('Mléko', 24.9, 10)`.
- `@classmethod from_csv_line(cls, line)` — řádek `"název;cena;počet"`,
  okolní mezery u názvu odstraň, cenu převeď na `float`, počet na `int`.
- `@classmethod from_dict(cls, data)` — dict s klíči `name`, `price`
  a volitelným `quantity`.
- `@staticmethod is_valid_code(code)` — kód zboží je platný, když má
  přesně 8 znaků a všechny jsou číslice.
- Obě classmethod vyrábí instanci přes `cls(...)`, ne `Product(...)`.
  Komentářem vysvětli proč. Nápověda: `cls` je třída, přes kterou se
  metoda zavolala. V `08-oop-dedicnost` to může být podtřída.
- **Předpověď:** funguje volání přes instanci? Co vypíše?

  ```python
  p = Product("x", 1)
  print(p.is_valid_code("12345678"))
  print(p.from_csv_line("A;1;1"))
  print(type(Product.from_dict), type(Product.is_valid_code))
  ```

### Příklady vstup/výstup

| Kód                                                              | Výsledek                        |
|------------------------------------------------------------------|---------------------------------|
| `Product.from_csv_line("Mléko;24.9;10")`                         | `Product('Mléko', 24.9, 10)`    |
| `Product.from_csv_line(" Chléb ;39;0")`                          | `Product('Chléb', 39.0, 0)`     |
| `Product.from_dict({"name": "Káva", "price": 189.0, "quantity": 3})` | `Product('Káva', 189.0, 3)` |
| `Product.from_dict({"name": "Sůl", "price": 12.5})`              | `Product('Sůl', 12.5, 0)`       |
| `Product.is_valid_code("12345678")`                              | `True`                          |
| `Product.is_valid_code("1234567")`                               | `False`                         |
| `Product.is_valid_code("1234567a")`                              | `False`                         |
| `Product.is_valid_code("123456789")`                             | `False`                         |
| `Product.is_valid_code("")`                                      | `False`                         |

## Bonus

Mini „manager“ ve stylu Djanga: třída si pamatuje všechny instance
vytvořené přes `create`.

- Třída `Book(title, author, year)` s `__repr__` → `Book('R.U.R.')`.
- Atribut třídy `objects = []`. **Tady** je sdílený seznam záměr:
  registr všech knih.
- `@classmethod`:
  - `create(cls, **fields)` — vytvoří instanci, uloží ji do `objects`
    a vrátí ji,
  - `all(cls)` — **kopie** seznamu všech knih (ať volající nemůže
    rozbít registr),
  - `filter(cls, **conditions)` — knihy, u kterých **všechny** zadané
    atributy mají danou hodnotu. Nápověda: `getattr` a `all`,
  - `count(cls)` — počet knih.
- Kniha vytvořená přímo přes `Book(...)` se do registru nedostane.
  Stejně jako v Djangu, kde `Book(...)` bez `.save()` není v DB.

### Příklady vstup/výstup (bonus)

Po vytvoření:

```python
Book.create(title="R.U.R.", author="Čapek", year=1920)
Book.create(title="Krakatit", author="Čapek", year=1924)
Book.create(title="Saturnin", author="Jirotka", year=1942)
```

| Kód                                          | Výsledek                                                  |
|----------------------------------------------|-----------------------------------------------------------|
| `Book.count()`                               | `3`                                                       |
| `Book.all()`                                 | `[Book('R.U.R.'), Book('Krakatit'), Book('Saturnin')]`    |
| `Book.filter(author="Čapek")`                | `[Book('R.U.R.'), Book('Krakatit')]`                      |
| `Book.filter(author="Čapek", year=1924)`     | `[Book('Krakatit')]`                                      |
| `Book.filter(author="Hašek")`                | `[]`                                                      |
| `Book.filter()`                              | všechny tři                                               |
| `Book("Mimo", "X", 2000)`, pak `Book.count()` | `3`                                                      |
| `Book.all().clear()`, pak `Book.count()`     | `3`                                                       |
