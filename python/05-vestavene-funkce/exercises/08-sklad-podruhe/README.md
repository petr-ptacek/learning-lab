# 08 — Sklad podruhé

Vrať se ke skladu z `04-datove-struktury/10-sklad` a přepiš jeho funkce
s vestavěnými funkcemi — ideálně každá funkce jeden `return`.

## Požadavky

- Použij stejný `products` jako v `10-sklad`.
- Napiš tyto funkce, **bez klasického `for` cyklu s `append`**:
  - `total_value(products)` — `sum` s generátorovým výrazem.
  - `most_valuable(products)` — **název** produktu s nejvyšší hodnotou
    `price * qty` (`max` s `key`). Prázdný sklad → `None`.
  - `sorted_by_value(products)` — názvy seřazené podle hodnoty sestupně.
  - `categories(products)` — abecedně seřazený seznam kategorií bez
    duplicit.
  - `any_out_of_stock(products)` — je některý produkt vyprodaný
    (`qty == 0`)?

### Příklady vstup/výstup

| Volání                          | Výsledek                                           |
|---------------------------------|----------------------------------------------------|
| `total_value(products)`         | `1616.0`                                           |
| `total_value([])`               | `0`                                                |
| `most_valuable(products)`       | `'Káva'`                                           |
| `most_valuable([])`             | `None`                                             |
| `sorted_by_value(products)`     | `['Káva', 'Šampon', 'Mléko', 'Chléb', 'Mýdlo']`    |
| `categories(products)`          | `['drogerie', 'potraviny']`                        |
| `categories([])`                | `[]`                                               |
| `any_out_of_stock(products)`    | `True`                                             |
| `any_out_of_stock([])`          | `False`                                            |

## Bonus

- `cheapest_by_category(products)` — dict `kategorie → název
  nejlevnějšího`, jako dict comprehension přes `categories(products)`
  s `min` a `key` uvnitř.
- `price_stats(products)` — tuple `(nejnižší cena, nejvyšší cena,
  průměrná cena)`, průměr zaokrouhlený na 2 místa. Prázdný sklad →
  `None`.

### Příklady vstup/výstup (bonus)

| Volání                             | Výsledek                                         |
|------------------------------------|--------------------------------------------------|
| `cheapest_by_category(products)`   | `{'drogerie': 'Mýdlo', 'potraviny': 'Mléko'}`    |
| `cheapest_by_category([])`         | `{}`                                             |
| `price_stats(products)`            | `(19.5, 149.0, 64.28)`                           |
| `price_stats([])`                  | `None`                                           |
