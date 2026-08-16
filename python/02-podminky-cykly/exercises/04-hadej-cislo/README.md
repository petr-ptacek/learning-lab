# 04 — Hádej číslo

Napiš hru, kdy si skript "myslí" číslo (napevno v proměnné, např. `50`) a
uživatel ho hádá, dokud neuhodne.

## Požadavky

- Tajné číslo ulož napevno do proměnné na začátku skriptu.
- Použij `while` cyklus, který běží, dokud uživatel neuhodne správně.
- Po každém pokusu vypiš nápovědu — `"Víc"` (hledané číslo je vyšší) nebo
  `"Míň"` (hledané číslo je nižší).
- Počítej počet pokusů a na konci ho vypiš.
- Výstup např.:

```
Hádej číslo (1-100): 50
Míň
Hádej číslo (1-100): 25
Víc
Hádej číslo (1-100): 37
Uhodl jsi! Počet pokusů: 3
```

## Bonus

- Přidej maximální počet pokusů (např. 7) — pokud ho uživatel překročí bez
  uhodnutí, hru pomocí `break` ukonči a vypiš prohru i správné číslo.
