# 08 — Prvočíslo

Napiš skript, který zjistí, jestli je zadané číslo prvočíslo.

## Požadavky

- Načti číslo `n`.
- Čísla menší než 2 nejsou prvočísla — ošetři to jako speciální případ.
- Použij `for` cyklus, který zkouší dělitele od 2 do `n - 1`, a `break`, jakmile najdeš dělitele, který `n` dělí beze
  zbytku.
- Pomocí příznakové proměnné (`bool`) rozliš, jestli byl dělitel nalezen, a podle toho vypiš výsledek.
- Výstup např.:

```
Zadej číslo: 7
7 je prvočíslo
```

### Příklady vstup/výstup

| Vstup | Výstup             |
|-------|--------------------|
| `7`   | `7 je prvočíslo`   |
| `8`   | `8 není prvočíslo` |
| `2`   | `2 je prvočíslo`   |
| `1`   | `1 není prvočíslo` |
| `97`  | `97 je prvočíslo`  |

## Bonus

- Vypiš všechna prvočísla od 2 do `n` (test z hlavní části použij uvnitř dalšího `for` cyklu).

### Příklady vstup/výstup (bonus)

| Vstup | Výstup                       |
|-------|------------------------------|
| `20`  | `2, 3, 5, 7, 11, 13, 17, 19` |
| `10`  | `2, 3, 5, 7`                 |
