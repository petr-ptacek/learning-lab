# 04 — Slevový kalkulátor

Vyzkoušej si oddělovače `/` a `*`, které vynucují, jak se parametr smí
předat.

## Požadavky

- Napiš funkci s touto přesnou signaturou:

  ```python
  def vypocitej_cenu(cena, /, sleva, *, mena="Kč"):
      ...
  ```

  - `cena` — jen poziční (nejde zapsat `cena=1000`)
  - `sleva` — pozičně i podle jména
  - `mena` — jen podle jména, s výchozí hodnotou `"Kč"`
- Funkce vrátí cenu po slevě (`sleva` je procento, např. `20` znamená
  20 %) jako text ve tvaru `"{výsledná_cena} {měna}"`.
- Načti `cena` a `sleva` pomocí `input()` a zavolej funkci aspoň dvěma
  různými platnými způsoby (napiš oba do kódu, ať vidíš, že oba fungují) —
  jednou bez `mena` (použije se výchozí `"Kč"`) a jednou s `mena="EUR"`.
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

- Přidej další keyword-only parametr `dph=0` (DPH v procentech), který
  se připočte k ceně **po slevě**.

### Příklady vstup/výstup (bonus)

| Cena | Sleva | DPH | Výstup       |
|------|-------|-----|--------------|
| 1000 | 25    | 21  | `907.5 Kč`   |
| 500  | 10    | 0   | `450.0 Kč`   |
