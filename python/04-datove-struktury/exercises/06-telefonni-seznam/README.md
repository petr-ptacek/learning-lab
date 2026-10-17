# 06 — Telefonní seznam

`dict` jako úložiště, ve kterém se hledá podle klíče — přidání, úprava,
hledání a mazání (CRUD).

## Požadavky

- Telefonní seznam je dict `jméno → číslo`.
- Hlavní smyčka s menu:
  - `p` — **přidej** kontakt (jméno, číslo). Pokud jméno už existuje,
    číslo přepiš a vypiš `Aktualizováno`, jinak `Přidáno`.
  - `h` — **hledej** podle jména → vypiš číslo, nebo `Nenalezeno`.
    Použij `.get()` s výchozí hodnotou, ne `if ... in`.
  - `s` — **smaž** kontakt → `Smazáno`, nebo `Nenalezeno` (bez
    `KeyError`).
  - `v` — **vypiš** všechny kontakty jako `jméno: číslo` (přes
    `.items()`). Prázdný seznam → `Seznam je prázdný`.
  - `k` — konec.
- Výstup např.:

```
Volba (p/h/s/v/k): p
Jméno: Anna
Číslo: 777 111 222
Přidáno
Volba (p/h/s/v/k): p
Jméno: Anna
Číslo: 603 999 888
Aktualizováno
Volba (p/h/s/v/k): h
Jméno: Anna
603 999 888
Volba (p/h/s/v/k): h
Jméno: Petr
Nenalezeno
Volba (p/h/s/v/k): v
Anna: 603 999 888
Volba (p/h/s/v/k): k
```

### Příklady vstup/výstup

| Seznam před                     | Volba + vstupy        | Výstup             | Seznam po                       |
|---------------------------------|-----------------------|--------------------|---------------------------------|
| `{}`                            | `p` `Anna` `777 111 222` | `Přidáno`       | `{'Anna': '777 111 222'}`       |
| `{'Anna': '777 111 222'}`       | `p` `Anna` `603 999 888` | `Aktualizováno` | `{'Anna': '603 999 888'}`       |
| `{'Anna': '777 111 222'}`       | `h` `Petr`            | `Nenalezeno`       | beze změny                      |
| `{'Anna': '777 111 222'}`       | `s` `Anna`            | `Smazáno`          | `{}`                            |
| `{}`                            | `s` `Anna`            | `Nenalezeno`       | `{}`                            |
| `{}`                            | `v`                   | `Seznam je prázdný`| `{}`                            |

## Bonus

- `c` — **hledej podle části jména** a vypiš všechny shody (`"an" in
  "Anna".lower()`), bez ohledu na velikost písmen. Žádná shoda →
  `Nenalezeno`.
- `r` — **zpětné hledání**: zadáš číslo, program vypíše jméno (nebo
  `Nenalezeno`). Zamysli se, proč je tohle pomalejší než hledání podle
  jména.

### Příklady vstup/výstup (bonus)

Seznam: `{'Anna': '777 111 222', 'Jana': '603 999 888', 'Petr': '731 000 111'}`

| Volba + vstup     | Výstup                                    |
|-------------------|-------------------------------------------|
| `c` `an`          | `Anna: 777 111 222` a `Jana: 603 999 888` |
| `c` `PETR`        | `Petr: 731 000 111`                       |
| `c` `x`           | `Nenalezeno`                              |
| `r` `603 999 888` | `Jana`                                    |
| `r` `000`         | `Nenalezeno`                              |
