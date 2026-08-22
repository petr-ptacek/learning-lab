# 05 — Sečti vše

Vyzkoušej si `*args` — libovolný počet pozičních argumentů.

## Požadavky

- Napiš funkci `secti_vse(*cisla)`, která vrátí součet libovolného počtu
  čísel, se kterými byla zavolána (i nulového).
- Načti tři čísla `a`, `b`, `c` pomocí `input()`.
- Zavolej funkci třikrát, s různým počtem argumentů, a vypiš všechny tři
  výsledky:
  - `secti_vse(a)`
  - `secti_vse(a, b)`
  - `secti_vse(a, b, c)`
- Výstup např.:

```
Zadej a: 2
Zadej b: 3
Zadej c: 5
secti_vse(a) = 2
secti_vse(a, b) = 5
secti_vse(a, b, c) = 10
```

### Příklady vstup/výstup

| a | b | c | Výstup                                                    |
|---|---|---|------------------------------------------------------------|
| 2 | 3 | 5 | `secti_vse(a) = 2, secti_vse(a, b) = 5, secti_vse(a, b, c) = 10` |
| 1 | 1 | 1 | `secti_vse(a) = 1, secti_vse(a, b) = 2, secti_vse(a, b, c) = 3`  |
| 0 | 0 | 0 | `secti_vse(a) = 0, secti_vse(a, b) = 0, secti_vse(a, b, c) = 0`  |

## Bonus

- Napiš i funkci `prumer(*cisla)`, která znovu využije `secti_vse` (zavolá
  ji uvnitř sebe) a vrátí průměr. Pro nulový počet čísel (`prumer()`)
  vrať `0`, ať nedojde k dělení nulou.

### Příklady vstup/výstup (bonus)

| Volání              | Výstup |
|----------------------|--------|
| `prumer(2, 3, 5)`    | `3.33` (zaokrouhleno na 2 des. místa) |
| `prumer(1, 1, 1)`    | `1.0`  |
| `prumer()`           | `0`    |
