# 07 — Pokladna

Vyzkoušej si rozsah platnosti proměnných (scope) a klíčové slovo
`global`.

## Požadavky

- Nastav globální proměnnou `zustatek = 0`.
- Napiš funkci `pripočti(castka)`, která pomocí `global` zvýší
  `zustatek` o `castka`.
- Napiš funkci `odecti(castka)`, která pomocí `global` sníží `zustatek`
  o `castka`.
- Napiš hlavní smyčku (`while True` + `break`, jako v minulém konceptu) —
  menu s volbami:
  - `p` — načti částku, zavolej `pripočti`, vypiš aktuální `zustatek`
  - `o` — načti částku, zavolej `odecti`, vypiš aktuální `zustatek`
  - `k` — vypiš konečný `zustatek` a `break`
- Výstup např.:

```
Zadej volbu (p/o/k): p
Zadej částku: 100
Zůstatek: 100
Zadej volbu (p/o/k): k
Konec, zůstatek: 100
```

### Příklady vstup/výstup

| Průběh (volby v pořadí)             | Výstup po každém kroku                          |
|---------------------------------------|--------------------------------------------------|
| `p 100`, `p 50`, `o 30`, `k`           | `100` → `150` → `120` → `Konec, zůstatek: 120`   |
| `o 20`, `k`                            | `-20` → `Konec, zůstatek: -20`                   |

## Bonus

- Přidej volbu `n` — zavolá funkci `vynuluj()` (opět přes `global`), která
  nastaví `zustatek` zpátky na `0`, a vypíše to.

### Příklady vstup/výstup (bonus)

| Průběh (volby v pořadí)         | Výstup po posledním kroku |
|-----------------------------------|-----------------------------|
| `p 100`, `n`, `k`                  | `Zůstatek vynulován: 0` → `Konec, zůstatek: 0` |
