# 08 — Kalkulátor s lambdami

Vyzkoušej si `lambda` výrazy — anonymní jednořádkové funkce přiřazené do
proměnné.

## Požadavky

- Vytvoř čtyři proměnné s lambda výrazy, každá přijímá dva parametry
  `a`, `b` a vrátí výsledek dané operace: `add`, `subtract`,
  `multiply`, `divide`.
- Napiš hlavní smyčku (`while True` + `break`) — menu, které se zeptá na
  operaci (`+`, `-`, `*`, `/`) a dvě čísla `a`, `b`.
- Podle zvolené operace (`if`/`elif`, ne slovník) zavolej odpovídající
  lambdu a vypiš výsledek.
- Pro `/` s `b == 0` vypiš `"Nelze dělit nulou"` a lambdu nevolej.
- Volba `k` skončí smyčku.
- Výstup např.:

```
Zadej operaci (+ - * / k): +
Zadej a: 3
Zadej b: 4
Výsledek: 7
```

### Příklady vstup/výstup

| Operace | a  | b | Výstup                  |
|---------|----|---|--------------------------|
| `+`     | 3  | 4 | `Výsledek: 7`            |
| `*`     | 5  | 6 | `Výsledek: 30`           |
| `/`     | 10 | 0 | `Nelze dělit nulou`      |
| `/`     | 10 | 5 | `Výsledek: 2.0`          |

## Bonus

- Přidej pátou lambdu `power = lambda a, b: a ** b` pro operaci `^`
  (umocnění).

### Příklady vstup/výstup (bonus)

| Operace | a | b | Výstup       |
|---------|---|---|--------------|
| `^`     | 2 | 5 | `Výsledek: 32` |
| `^`     | 3 | 0 | `Výsledek: 1`  |
