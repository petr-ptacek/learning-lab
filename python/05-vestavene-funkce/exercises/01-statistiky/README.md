# 01 — Statistiky podruhé

V `04-datove-struktury/01-teploty` jsi min, max a součet počítal cyklem.
Teď totéž vestavěnými funkcemi — `min`, `max`, `sum`, `len`, `round`
a poprvé parametr `key`.

## Požadavky

- Napiš funkci `stats(numbers)`, která vrátí tuple
  `(minimum, maximum, součet, průměr, rozpětí)` — průměr zaokrouhlený na
  2 desetinná místa, rozpětí = maximum − minimum. Pro prázdný seznam vrať
  `None`. **Žádný cyklus** — jen vestavěné funkce.
- Napiš funkci `closest_to_zero(numbers)`, která vrátí číslo nejblíž
  nule. Jedním voláním `min` s parametrem `key` (nápověda: `abs`). Při
  shodě vyhrává první výskyt. Pro prázdný seznam vrať `None` — bez `if`,
  přes parametr `default`.

### Příklady vstup/výstup

| `numbers`                                    | `stats(numbers)`                          |
|----------------------------------------------|-------------------------------------------|
| `[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]`  | `(9.5, 18.0, 97.0, 13.86, 8.5)`           |
| `[5.0]`                                      | `(5.0, 5.0, 5.0, 5.0, 0.0)`               |
| `[-3.0, -1.5, -7.0]`                         | `(-7.0, -1.5, -11.5, -3.83, 5.5)`         |
| `[]`                                         | `None`                                    |

| `numbers`          | `closest_to_zero(numbers)` |
|--------------------|----------------------------|
| `[5, -2, 3, 2]`    | `-2`                       |
| `[-4, 4]`          | `-4`                       |
| `[0, 7]`           | `0`                        |
| `[]`               | `None`                     |

## Bonus

- `normalize(numbers)` — převede čísla na škálu 0 až 1:
  `(x - min) / (max - min)`, zaokrouhleno na 2 místa. Pokud jsou všechna
  čísla stejná (dělení nulou), vrať samé `0.0`. Výsledek jako
  comprehension.
- `count_above_average(numbers)` — kolik čísel je nad průměrem, jedním
  `sum(...)` s generátorovým výrazem (viz `THEORY.md`). Prázdný seznam → `0`.

### Příklady vstup/výstup (bonus)

| `numbers`            | `normalize(numbers)`        |
|----------------------|-----------------------------|
| `[10, 15, 20]`       | `[0.0, 0.5, 1.0]`           |
| `[-5, 0, 5, 10]`     | `[0.0, 0.33, 0.67, 1.0]`    |
| `[3, 3, 3]`          | `[0.0, 0.0, 0.0]`           |
| `[]`                 | `[]`                        |

| `numbers`                                    | `count_above_average(numbers)` |
|----------------------------------------------|--------------------------------|
| `[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]`  | `4`                            |
| `[5.0]`                                      | `0`                            |
| `[]`                                         | `0`                            |
