# 06 — Součet bez násobků

Napiš skript, který sečte čísla od 1 do `n`, ale přeskočí (pomocí
`continue`) čísla dělitelná zadaným číslem `k`.

## Požadavky

- Načti horní hranici `n` a číslo `k` (dělitel, který se vynechává).
- Použij `for` cyklus s `range()`.
- Pro každé číslo dělitelné `k` použij `continue`, ať se nepřičte k součtu.
- Počítej, kolik čísel bylo přeskočeno.
- Na konci vypiš výsledný součet a počet přeskočených čísel.
- Výstup např.:

```
Zadej n: 10
Zadej k (vynechávané číslo): 3
Součet: 37
Přeskočeno: 3 čísel
```

### Příklady vstup/výstup

| n | k | Výstup |
|---|---|---|
| 10 | 3 | `Součet: 37, přeskočeno: 3 čísel` |
| 10 | 5 | `Součet: 40, přeskočeno: 2 čísel` |
| 15 | 4 | `Součet: 96, přeskočeno: 3 čísel` |
| 5 | 1 | `Součet: 0, přeskočeno: 5 čísel` |

## Bonus

- Uprav skript, ať uživatel může zadat **dvě** čísla `k1` a `k2` — přeskočí
  se čísla dělitelná `k1` **nebo** `k2` (použij `or`).

### Příklady vstup/výstup (bonus)

| n | k1 | k2 | Výstup |
|---|---|---|---|
| 15 | 3 | 5 | `Součet: 60, přeskočeno: 7 čísel` |
| 10 | 2 | 5 | `Součet: 20, přeskočeno: 6 čísel` |
