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

Uprav skript, ať zvládne převod z libovolné jednotky (uživatel zadá i
jednotku, např. `C`, `F` nebo `K`) na zbylé dvě. Podle zadané jednotky použij
odpovídající vzorce:

**Znám C:**
- `F = C * 9/5 + 32`
- `K = C + 273.15`

**Znám F:**
- `C = (F - 32) * 5/9`
- `K = (F - 32) * 5/9 + 273.15`

**Znám K:**
- `C = K - 273.15`
- `F = (K - 273.15) * 9/5 + 32`
