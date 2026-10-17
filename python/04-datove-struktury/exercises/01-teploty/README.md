# 01 — Týdenní teploty

Základy `list` — indexování, záporné indexy, slicing, `len()` a ruční
průchod cyklem.

## Požadavky

- Napiš funkci `print_stats(temps)`, která pro seznam teplot vypíše:
  - první a poslední měření (záporný index),
  - poslední dvě měření (slicing),
  - počet měření,
  - minimum, maximum a průměr (zaokrouhlený na 2 desetinná místa),
  - kolik měření je **nad** průměrem.
- Minimum, maximum a součet spočítej **vlastním cyklem** — bez `min()`,
  `max()` a `sum()` (ty přijdou v `05-vestavene-funkce`).
- Pro prázdný seznam vypiš jen `Žádná data` (a nespadni na dělení nulou
  ani na `IndexError`).
- Zavolej funkci pro všechny seznamy z tabulky níže.
- Výstup např. pro `[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]`:

```
První: 12.5, poslední: 16.5
Poslední dvě: [11.0, 16.5]
Počet měření: 7
Min: 9.5, max: 18.0, průměr: 13.86
Nad průměrem: 4
```

### Příklady vstup/výstup

| `temps`                                       | první / poslední | poslední dvě    | počet | min / max / průměr       | nad průměrem |
|-----------------------------------------------|------------------|-----------------|-------|--------------------------|--------------|
| `[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]`   | `12.5` / `16.5`  | `[11.0, 16.5]`  | `7`   | `9.5` / `18.0` / `13.86` | `4`          |
| `[5.0]`                                       | `5.0` / `5.0`    | `[5.0]`         | `1`   | `5.0` / `5.0` / `5.0`    | `0`          |
| `[-3.0, -1.5, -7.0]`                          | `-3.0` / `-7.0`  | `[-1.5, -7.0]`  | `3`   | `-7.0` / `-1.5` / `-3.83`| `2`          |
| `[20.0, 20.0]`                                | `20.0` / `20.0`  | `[20.0, 20.0]`  | `2`   | `20.0` / `20.0` / `20.0` | `0`          |
| `[]`                                          | —                | —               | —     | —                        | `Žádná data` |

## Bonus

- Přidej druhý parametr `days` — seznam názvů dnů stejně dlouhý jako
  `temps` (např. `["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]`) — a vypiš,
  **ve který den** bylo nejtepleji a nejchladněji. Při shodě vyhrává
  první výskyt.

### Příklady vstup/výstup (bonus)

| `temps`                                     | `days`                                    | Výstup navíc                          |
|---------------------------------------------|-------------------------------------------|---------------------------------------|
| `[12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5]` | `["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]` | `Nejtepleji: Čt, nejchladněji: St` |
| `[20.0, 20.0]`                              | `["So", "Ne"]`                            | `Nejtepleji: So, nejchladněji: So`    |
| `[-3.0, -1.5, -7.0]`                        | `["Po", "Út", "St"]`                      | `Nejtepleji: Út, nejchladněji: St`    |
