# 05 — Faktura

Navazuje na `03-uctenka`, tentokrát s víc položkami a slevou. Napiš skript,
který načte 3 položky faktury a vypíše zarovnanou fakturu se slevou.

## Požadavky

- Pro každou ze 3 položek načti název, cenu za kus a počet kusů (opět 3x
  samostatně, bez cyklu).
- Spočítej mezisoučet (součet cena × počet za všechny položky).
- Načti procento slevy (celé číslo, např. `10`) a spočítej slevu i finální
  částku k úhradě.
- Výstup zarovnej do sloupců a použij tisícový oddělovač u peněžních částek,
  např.:

```
--- Faktura ---
Položka          Ks   Cena/ks       Celkem
Klávesnice         1   1290.00      1290.00
Monitor            2   4990.00      9980.00
Myš                1    390.00       390.00
------------------------------------------------
Mezisoučet:                       11660.00
Sleva (10%):                       1166.00
Celkem k úhradě:                   10494.00
```

## Požadavky na formátování

- Název položky: doleva, pevná šířka (`<`).
- Počet kusů, cena/ks, celkem: doprava, pevná šířka (`>`).
- Peněžní částky: tisícový oddělovač + 2 desetinná místa (`,.2f`).
- Sleva v záhlaví řádku "Sleva (X %)": zkus si vyzkoušet i formát `.0%`
  na hodnotě `sleva_procento / 100` místo ručního psaní `%` za číslo.

## Bonus

- Pokud je sleva 0, řádek se slevou úplně vynech (bude potřeba `if`, což už
  z předchozího cvičení znáš).
