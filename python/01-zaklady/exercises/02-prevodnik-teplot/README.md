# 02 — Převodník teplot

Napiš skript, který načte teplotu ve stupních Celsia a vypíše ji převedenou
na Fahrenheity a Kelviny.

Vzorce:

- `F = C * 9/5 + 32`
- `K = C + 273.15`

## Požadavky

- Teplotu načti pomocí `input()` a preveď na `float`.
- Výsledky zaokrouhli na 1 desetinné místo (funkce `round()`).
- Výstup např.:

```
Zadej teplotu ve °C: 21
21.0 °C = 69.8 °F = 294.1 K
```

## Bonus

- Uprav skript, ať zvládne i opačný převod (ze zadaných Fahrenheitů na
  Celsia a Kelviny) — např. podle toho, jaké písmeno uživatel zadá jako
  jednotku.
