# 03 — Účtenka

Napiš skript, který spočítá cenu nákupu jedné položky.

## Požadavky

- Načti od uživatele:
  - název položky (text)
  - cenu za kus bez DPH (desetinné číslo)
  - počet kusů (celé číslo)
- Spočítej:
  - cenu za kusy bez DPH (`cena_bez_dph * pocet`)
  - DPH (21 %)
  - celkovou cenu s DPH
- Zaokrouhli peněžní částky na 2 desetinná místa a vypiš přehlednou účtenku,
  např.:

```
--- Účtenka ---
Položka: Káva
Počet: 3 ks
Cena bez DPH: 250.00 Kč
DPH (21 %): 52.50 Kč
Celkem: 302.50 Kč
```

## Bonus

- Zarovnej hodnoty v účtence tak, aby čísla končila na stejné pozici
  (nápověda: formátovací mini-jazyk f-stringů, např. `f"{cena:>10.2f}"`).
