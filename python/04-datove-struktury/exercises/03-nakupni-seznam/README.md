# 03 — Nákupní seznam

Metody seznamu (`append`, `remove`, …) v interaktivním programu — seznam
se mění za běhu podle toho, co uživatel zadá.

## Požadavky

- Hlavní smyčka (`while True`) s menu:
  - `p` — **přidej** položku. Pokud už v seznamu je, nepřidávej ji a vypiš
    `Už v seznamu`.
  - `o` — **odeber** položku. Pokud v seznamu není, vypiš `Není v seznamu`
    (program nesmí spadnout na `ValueError`).
  - `v` — **vypiš** seznam očíslovaně od 1 (bez `enumerate`). Prázdný
    seznam → `Seznam je prázdný`.
  - `k` — konec.
  - cokoliv jiného → `Neznámá volba`.
- Výstup např.:

```
Volba (p/o/v/k): p
Položka: mléko
Volba (p/o/v/k): p
Položka: chleba
Volba (p/o/v/k): p
Položka: mléko
Už v seznamu
Volba (p/o/v/k): v
1. mléko
2. chleba
Volba (p/o/v/k): o
Položka: máslo
Není v seznamu
Volba (p/o/v/k): o
Položka: mléko
Volba (p/o/v/k): v
1. chleba
Volba (p/o/v/k): k
```

### Příklady vstup/výstup

| Seznam před      | Volba + položka | Výstup             | Seznam po        |
|------------------|-----------------|--------------------|------------------|
| `[]`             | `p` `mléko`     | —                  | `['mléko']`      |
| `['mléko']`      | `p` `mléko`     | `Už v seznamu`     | `['mléko']`      |
| `['mléko']`      | `o` `máslo`     | `Není v seznamu`   | `['mléko']`      |
| `['mléko', 'chleba']` | `o` `mléko` | —                 | `['chleba']`     |
| `[]`             | `v`             | `Seznam je prázdný`| `[]`             |
| `['a', 'b']`     | `x`             | `Neznámá volba`    | `['a', 'b']`     |

## Bonus

- `n` — **vlož** položku na zadanou pozici (číslováno od 1, jako výpis).
  Pozice větší než délka seznamu → vloží se na konec (zjisti, jak se
  k tomu chová `insert`). Duplicitu hlídej stejně jako u `p`.
- `x` — **vyprázdni** celý seznam.

### Příklady vstup/výstup (bonus)

| Seznam před          | Volba + vstupy  | Seznam po                    |
|----------------------|-----------------|------------------------------|
| `['mléko', 'chleba']` | `n` `máslo` `1` | `['máslo', 'mléko', 'chleba']` |
| `['mléko', 'chleba']` | `n` `máslo` `2` | `['mléko', 'máslo', 'chleba']` |
| `['mléko']`          | `n` `máslo` `10`| `['mléko', 'máslo']`         |
| `['mléko', 'chleba']` | `x`            | `[]`                         |
