# 04 — Slevový kalkulátor

Vyzkoušej si oddělovače `/` a `*`, které vynucují, jak se parametr smí
předat.

## Požadavky

- Napiš funkci s touto přesnou signaturou:

  ```python
  def calculate_price(price, /, discount, *, currency="Kč"):
      ...
  ```

  - `price` — jen poziční (nejde zapsat `price=1000`)
  - `discount` — pozičně i podle jména
  - `currency` — jen podle jména, s výchozí hodnotou `"Kč"`
- Funkce vrátí cenu po slevě (`discount` je procento, např. `20` znamená
  20 %) jako text ve tvaru `"{výsledná_cena} {měna}"`.
- Načti cenu a slevu pomocí `input()` a zavolej funkci aspoň dvěma
  různými platnými způsoby (napiš oba do kódu, ať vidíš, že oba fungují) —
  jednou bez `currency` (použije se výchozí `"Kč"`) a jednou s
  `currency="EUR"`.
- Výstup např.:

```
Zadej cenu: 1000
Zadej slevu (%): 25
750.0 Kč
```

### Příklady vstup/výstup

| Cena | Sleva | Měna (pokud zadaná) | Výstup      |
|------|-------|----------------------|-------------|
| 1000 | 25    | (výchozí)            | `750.0 Kč`  |
| 500  | 10    | (výchozí)            | `450.0 Kč`  |
| 250  | 50    | `EUR`                | `125.0 EUR` |

## Bonus

- Přidej další keyword-only parametr `vat=0` (DPH v procentech), který
  se připočte k ceně **po slevě**.

### Příklady vstup/výstup (bonus)

| Cena | Sleva | DPH | Výstup       |
|------|-------|-----|--------------|
| 1000 | 25    | 21  | `907.5 Kč`   |
| 500  | 10    | 0   | `450.0 Kč`   |
