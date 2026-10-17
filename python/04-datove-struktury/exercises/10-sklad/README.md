# 10 — Sklad

Seznam dictů — nejběžnější tvar dat v praxi (řádky z databáze, JSON
z API). Kombinuje všechno z tohoto konceptu.

## Požadavky

- V kódu měj sklad:

  ```python
  products = [
      {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
      {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
      {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
      {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
      {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
  ]
  ```

- Napiš tyto funkce:
  - `total_value(products)` — celková hodnota skladu (součet
    `price * qty`).
  - `low_stock(products, limit=5)` — seznam **názvů** produktů, kterých
    je méně než `limit` kusů.
  - `by_category(products)` — dict `kategorie → seznam názvů`.
  - `print_report(products)` — tabulka (název, kategorie, cena, kusy,
    hodnota) a pod ní celková hodnota. Formátování viz
    [`STRING_FORMATTING.md`](../../../docs/STRING_FORMATTING.md).
- Všechny funkce musí fungovat i pro prázdný sklad `[]`.

`print_report(products)`, např.:

```
Název     Kategorie       Cena   Ks   Hodnota
Mléko     potraviny      24.90   10    249.00
Chléb     potraviny      39.00    3    117.00
Mýdlo     drogerie       19.50    0      0.00
Šampon    drogerie       89.00    4    356.00
Káva      potraviny     149.00    6    894.00
Celkem                                1616.00
```

### Příklady vstup/výstup

| Volání                         | Výsledek                                                         |
|--------------------------------|------------------------------------------------------------------|
| `total_value(products)`        | `1616.0`                                                         |
| `total_value([])`              | `0`                                                              |
| `low_stock(products)`          | `['Chléb', 'Mýdlo', 'Šampon']`                                   |
| `low_stock(products, 1)`       | `['Mýdlo']`                                                      |
| `low_stock(products, 0)`       | `[]`                                                             |
| `by_category(products)`        | `{'potraviny': ['Mléko', 'Chléb', 'Káva'], 'drogerie': ['Mýdlo', 'Šampon']}` |
| `by_category([])`              | `{}`                                                             |

## Bonus

- `restock(products, name, amount)` — přidá `amount` kusů produktu
  s daným názvem (**změní** dict v seznamu na místě) a vrátí `True`.
  Neexistující produkt → vrať `False` a nic neměň.
- `cheapest_by_category(products)` — dict `kategorie → název
  nejlevnějšího produktu` (bez `min()`). Při shodě ceny vyhrává první.

### Příklady vstup/výstup (bonus)

| Volání                                   | Výsledek                                         |
|------------------------------------------|--------------------------------------------------|
| `restock(products, "Mýdlo", 20)`         | `True`, Mýdlo má pak `qty` `20`                  |
| `restock(products, "Pivo", 5)`           | `False`, sklad beze změny                        |
| `cheapest_by_category(products)`         | `{'potraviny': 'Mléko', 'drogerie': 'Mýdlo'}`    |
| `cheapest_by_category([])`               | `{}`                                             |
