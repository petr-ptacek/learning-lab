# 07 — Pokladna

Vyzkoušej si rozsah platnosti proměnných (scope) a klíčové slovo
`global`.

## Požadavky

- Nastav globální proměnnou `balance = 0`.
- Napiš funkci `deposit(amount)`, která pomocí `global` zvýší `balance`
  o `amount`.
- Napiš funkci `withdraw(amount)`, která pomocí `global` sníží `balance`
  o `amount`.
- Napiš hlavní smyčku (`while True` + `break`, jako v minulém konceptu) — menu s volbami:
    - `p` — načti částku, zavolej `deposit`, vypiš aktuální `balance`
    - `o` — načti částku, zavolej `withdraw`, vypiš aktuální `balance`
    - `k` — vypiš konečný `balance` a `break`
- Výstup např.:

```
Zadej volbu (p/o/k): p
Zadej částku: 100
Zůstatek: 100
Zadej volbu (p/o/k): k
Konec, zůstatek: 100
```

### Příklady vstup/výstup

| Průběh (volby v pořadí)      | Výstup po každém kroku                         |
|------------------------------|------------------------------------------------|
| `p 100`, `p 50`, `o 30`, `k` | `100` → `150` → `120` → `Konec, zůstatek: 120` |
| `o 20`, `k`                  | `-20` → `Konec, zůstatek: -20`                 |

## Bonus

- Přidej volbu `n` — zavolá funkci `reset_balance()` (opět přes
  `global`), která nastaví `balance` zpátky na `0`, a vypíše to.

### Příklady vstup/výstup (bonus)

| Průběh (volby v pořadí) | Výstup po posledním kroku                      |
|-------------------------|------------------------------------------------|
| `p 100`, `n`, `k`       | `Zůstatek vynulován: 0` → `Konec, zůstatek: 0` |
