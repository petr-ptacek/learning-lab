# 05 — Trojúhelník

Napiš skript, který načte délky tří stran (`a`, `b`, `c`) a ověří, jestli z
nich lze vůbec sestavit trojúhelník, a pokud ano, jaký typ.

## Požadavky

- Načti tři čísla `a`, `b`, `c`.
- Nejdřív ověř **trojúhelníkovou nerovnost** — součet libovolných dvou stran
  musí být větší než strana třetí (musí platit pro všechny tři kombinace).
  Pokud neplatí, vypiš, že trojúhelník nelze sestavit, a skript skonči.
- Pokud lze, urči typ trojúhelníku pomocí `if`/`elif`/`else` a operátorů
  `and`/`or`:
  - **rovnostranný** — všechny tři strany stejné
  - **rovnoramenný** — právě dvě strany stejné
  - **obecný** — všechny strany různé
- Výstup např.:

```
Zadej stranu a: 3
Zadej stranu b: 3
Zadej stranu c: 3
Trojúhelník: rovnostranný
```

### Příklady vstup/výstup

| a | b | c | Výstup |
|---|---|---|---|
| 3 | 3 | 3 | `Trojúhelník: rovnostranný` |
| 3 | 3 | 5 | `Trojúhelník: rovnoramenný` |
| 3 | 4 | 5 | `Trojúhelník: obecný` |
| 1 | 1 | 5 | `Trojúhelník nelze sestavit` |
| 0 | 4 | 4 | `Trojúhelník nelze sestavit` |

## Bonus

- Pokud je trojúhelník obecný, ověř navíc, jestli je **pravoúhlý**
  (Pythagorova věta: druhá mocnina nejdelší strany se rovná součtu druhých
  mocnin zbylých dvou stran).

### Příklady vstup/výstup (bonus)

| a | b | c | Výstup |
|---|---|---|---|
| 3 | 4 | 5 | `Trojúhelník: obecný, pravoúhlý` |
| 5 | 6 | 7 | `Trojúhelník: obecný` |
| 6 | 8 | 10 | `Trojúhelník: obecný, pravoúhlý` |
