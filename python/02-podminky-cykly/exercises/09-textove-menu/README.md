# 09 — Textové menu

Napiš jednoduché textové menu, které se pořád dokola ptá, co má uživatel udělat, dokud nezadá konec. Cvičení spojuje
většinu nástrojů z tohoto konceptu do jednoho celku.

## Požadavky

- Použij `while True` jako hlavní smyčku programu (běží "navždy").
- Na začátku každé iterace vypiš menu, např.:

```
1 - spočítej samohlásky ve slově
2 - obrať pořadí znaků slova
0 - konec
```

- Načti volbu uživatele a podle ní (`if`/`elif`/`else`) udělej:
    - **`1`** — načti slovo a pomocí `for znak in slovo` spočítej, kolik obsahuje samohlásek (`a, e, i, o, u, y`, bez
      ohledu na velikost písmen, diakritiku neřeš). Vypiš počet.
    - **`2`** — načti slovo a pomocí cyklu (ne `[::-1]` ani `reversed()`)
      vypiš ho obráceně.
    - **`0`** — vypiš rozloučení a `break` hlavní smyčku.
    - **jinak** — vypiš, že volba neexistuje, a menu se ukáže znovu.
- Výstup např.:

```
1 - spočítej samohlásky ve slově
2 - obrať pořadí znaků slova
0 - konec
Zadej volbu: 1
Zadej slovo: malina
Počet samohlásek: 3
```

### Příklady vstup/výstup

| Volba | Slovo    | Výstup                          |
|-------|----------|---------------------------------|
| `1`   | `malina` | `Počet samohlásek: 3`           |
| `1`   | `slunce` | `Počet samohlásek: 2`           |
| `1`   | `krk`    | `Počet samohlásek: 0`           |
| `2`   | `kolo`   | `olok`                          |
| `2`   | `python` | `nohtyp`                        |
| `2`   | `a`      | `a`                             |
| `3`   | —        | `Neznámá volba`                 |
| `0`   | —        | `Konec, ahoj!` (a konec smyčky) |

## Bonus

- Počítej, kolik akcí (voleb `1`/`2`) uživatel za běh programu provedl, a při volbě `0` to vypiš spolu s rozloučením.

### Příklady vstup/výstup (bonus)

| Průběh (volby v pořadí) | Výstup při `0`                     |
|-------------------------|------------------------------------|
| `1, 2, 0`               | `Konec, ahoj! Provedl jsi 2 akcí.` |
| `2, 2, 2, 0`            | `Konec, ahoj! Provedl jsi 3 akcí.` |
| `0`                     | `Konec, ahoj! Provedl jsi 0 akcí.` |
