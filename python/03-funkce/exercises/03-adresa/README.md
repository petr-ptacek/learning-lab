# 03 — Adresa

Vyzkoušej si volání funkce pomocí keyword argumentů (podle jména
parametru, ne podle pořadí).

## Požadavky

- Napiš funkci `format_address(street, number, city, zip_code)`, která
  vrátí adresu naformátovanou jako `"{street} {number}, {zip_code} {city}"`.
- Načti všechny čtyři údaje pomocí `input()`.
- Zavolej funkci pomocí **keyword argumentů** a v **jiném pořadí**, než
  jsou parametry definované (např. nejdřív `city=`, pak `street=`...) —
  ukaž si, že na pořadí keyword argumentů nezáleží.
- Vypiš, co funkce vrátila.
- Výstup např.:

```
Zadej ulici: Hlavní
Zadej číslo: 12
Zadej město: Praha
Zadej PSČ: 11000
Hlavní 12, 11000 Praha
```

### Příklady vstup/výstup

| Ulice   | Číslo | Město | PSČ     | Výstup                     |
|---------|-------|-------|---------|-----------------------------|
| Hlavní  | 12    | Praha | 11000   | `Hlavní 12, 11000 Praha`    |
| Dlouhá  | 5     | Brno  | 60200   | `Dlouhá 5, 60200 Brno`      |

## Bonus

- Přidej pátý, volitelný keyword parametr `orientation_number=None`.
  Pokud je zadaný (není `None`), přidej ho do formátu za lomeno:
  `"{street} {number}/{orientation_number}, {zip_code} {city}"`.

### Příklady vstup/výstup (bonus)

| Ulice  | Číslo | Č. orientační | Město | PSČ   | Výstup                       |
|--------|-------|----------------|-------|-------|-------------------------------|
| Hlavní | 12    | 3              | Praha | 11000 | `Hlavní 12/3, 11000 Praha`    |
| Dlouhá | 5     | (prázdné)      | Brno  | 60200 | `Dlouhá 5, 60200 Brno`        |
