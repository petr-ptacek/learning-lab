# 01 — Osobní vizitka

Napiš skript, který se uživatele zeptá na:

- jméno
- věk
- město, kde bydlí

A vypíše formátovanou vizitku, např.:

```
Jak se jmenuješ? Petr
Kolik ti je let? 30
Kde bydlíš? Praha

--- Vizitka ---
Jméno: Petr
Věk: 30 let
Bydliště: Praha
Rok narození (přibližně): 1996
```

## Požadavky

- Použij `input()` pro načtení hodnot.
- Věk převeď na `int` a spočítej z něj přibližný rok narození (aktuální rok
  si napevno ulož do proměnné, např. `aktualni_rok = 2026`).
- Výstup formátuj pomocí f-stringů.

## Bonus

- Zkus vizitku "orámovat" pomocí `=` nebo `-` znaků o stejné délce jako text.
