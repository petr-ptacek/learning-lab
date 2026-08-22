# 05 — Sečti vše

Vyzkoušej si `*args` — libovolný počet pozičních argumentů.

## Požadavky

- Napiš funkci `sum_all(*numbers)`, která vrátí součet libovolného počtu čísel, se kterými byla zavolána (i nulového).
- Načti tři čísla `a`, `b`, `c` pomocí `input()`.
- Zavolej funkci třikrát, s různým počtem argumentů, a vypiš všechny tři výsledky:
    - `sum_all(a)`
    - `sum_all(a, b)`
    - `sum_all(a, b, c)`
- Výstup např.:

```
Zadej a: 2
Zadej b: 3
Zadej c: 5
sum_all(a) = 2
sum_all(a, b) = 5
sum_all(a, b, c) = 10
```

### Příklady vstup/výstup

| a | b | c | Výstup                                                     |
|---|---|---|------------------------------------------------------------|
| 2 | 3 | 5 | `sum_all(a) = 2, sum_all(a, b) = 5, sum_all(a, b, c) = 10` |
| 1 | 1 | 1 | `sum_all(a) = 1, sum_all(a, b) = 2, sum_all(a, b, c) = 3`  |
| 0 | 0 | 0 | `sum_all(a) = 0, sum_all(a, b) = 0, sum_all(a, b, c) = 0`  |

## Bonus

- Napiš i funkci `average(*numbers)`, která znovu využije `sum_all`
  (zavolá ji uvnitř sebe) a vrátí průměr. Pro nulový počet čísel (`average()`) vrať `0`, ať nedojde k dělení nulou.

### Příklady vstup/výstup (bonus)

| Volání             | Výstup                                |
|--------------------|---------------------------------------|
| `average(2, 3, 5)` | `3.33` (zaokrouhleno na 2 des. místa) |
| `average(1, 1, 1)` | `1.0`                                 |
| `average()`        | `0`                                   |
