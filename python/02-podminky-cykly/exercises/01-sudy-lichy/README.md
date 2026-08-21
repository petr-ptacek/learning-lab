# 01 — Sudý/lichý

Napiš skript, který načte celé číslo a řekne, jestli je sudé nebo liché.

## Požadavky

- Načti číslo pomocí `input()` a preveď na `int`.
- Pomocí `if`/`else` a operátoru `%` (zbytek po dělení) rozhodni, jestli je
  sudé (`cislo % 2 == 0`) nebo liché.
- Výstup např.:

```
Zadej číslo: 7
7 je liché
```

### Příklady vstup/výstup

| Vstup | Výstup |
|---|---|
| `7` | `7 je liché` |
| `4` | `4 je sudé` |
| `0` | `0 je sudé` |
| `-3` | `-3 je liché` |
| `-8` | `-8 je sudé` |

## Bonus

- Ošetři i zápornou nulu/nulu (0 je sudé) a přidej info, jestli je číslo
  kladné, záporné, nebo nula (`if`/`elif`/`else`).

### Příklady vstup/výstup (bonus)

| Vstup | Výstup |
|---|---|
| `7` | `7 je liché. 7 je kladné.` |
| `-3` | `-3 je liché. -3 je záporné.` |
| `0` | `0 je sudé. 0 je nula.` |
| `-8` | `-8 je sudé. -8 je záporné.` |
| `2` | `2 je sudé. 2 je kladné.` |
