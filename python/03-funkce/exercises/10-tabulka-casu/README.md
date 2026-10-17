# 10 — Tabulka časů

Souhrnné cvičení k funkcím. Kombinuje to, co už znáš (parametry,
keyword-only `*`, lambdy, volání jedné funkce z druhé), se třemi věcmi,
které zatím zazněly jen okrajově:

- **vrácení více hodnot** — `return a, b` vrátí dvojici a volající ji
  rozbalí do proměnných: `q, r = divide(7, 2)`;
- **funkce jako argument** — funkci (i lambdu) jde předat jako běžnou
  hodnotu a uvnitř ji zavolat: `func(x)`;
- **docstring** — řetězec v `"""..."""` hned na prvním řádku těla funkce,
  popisuje, co funkce dělá. Přečteš ho přes `help(funkce)` nebo
  `funkce.__doc__`.

Na výpis se hodí [`STRING_FORMATTING.md`](../../../docs/STRING_FORMATTING.md).

## Požadavky

- Napiš funkci `split_time(seconds)`, která rozdělí počet sekund na hodiny,
  minuty a sekundy a **vrátí všechny tři hodnoty najednou**. Použij `//`
  a `%`. Hodiny se nepřetáčí přes 24 (`90061` → 25 hodin).
- Napiš funkci `format_time(seconds)`, která **zavolá `split_time`**
  a vrátí řetězec ve tvaru `H:MM:SS` (minuty a sekundy vždy dvouciferně).
- Napiš funkci `print_table(func, start, end, *, step=1)`, která pro každé
  `x` od `start` do `end` **včetně** (po kroku `step`) vypíše řádek
  `x | func(x)`. Obě hodnoty zarovnej doprava na šířku 8. `step` musí jít
  předat jen jménem (`step=1800`), ne pozičně.
- Každá ze tří funkcí má docstring.
- V hlavní části programu:
  1. vypiš docstring funkce `split_time`,
  2. zavolej `print_table` s **lambdou**, která vrací druhou mocninu,
     pro `x` od `1` do `5`,
  3. zavolej `print_table` s funkcí `format_time` (bez závorek!) pro
     `0` až `7200` po `1800`.

### Příklady — `split_time` a `format_time`

| `seconds` | `split_time(seconds)` | `format_time(seconds)` |
|-----------|-----------------------|------------------------|
| `3661`    | `(1, 1, 1)`           | `1:01:01`              |
| `0`       | `(0, 0, 0)`           | `0:00:00`              |
| `59`      | `(0, 0, 59)`          | `0:00:59`              |
| `3600`    | `(1, 0, 0)`           | `1:00:00`              |
| `86399`   | `(23, 59, 59)`        | `23:59:59`             |
| `90061`   | `(25, 1, 1)`          | `25:01:01`             |

### Příklady — `print_table`

`print_table(lambda x: x ** 2, 1, 5)`:

```
       1 |        1
       2 |        4
       3 |        9
       4 |       16
       5 |       25
```

`print_table(format_time, 0, 7200, step=1800)`:

```
       0 |  0:00:00
    1800 |  0:30:00
    3600 |  1:00:00
    5400 |  1:30:00
    7200 |  2:00:00
```

Okrajové případy:

| Volání                                  | Výstup                          |
|-----------------------------------------|---------------------------------|
| `print_table(lambda x: x, 5, 3)`        | nic (`start > end`)             |
| `print_table(lambda x: x, 4, 4)`        | jeden řádek `       4 \|        4` |
| `print_table(format_time, 0, 7200, 1800)` | `TypeError` — `step` jen jménem |

## Bonus

- `format_time` umí i **záporné** sekundy — znaménko dá před hodiny
  a zbytek spočítá z kladné hodnoty (`split_time` nech beze změny).
- `print_table` dostane další keyword-only parametr `width` s výchozí
  hodnotou `8`, kterým jde šířku sloupců změnit.

### Příklady vstup/výstup (bonus)

| Volání                | Výstup      |
|-----------------------|-------------|
| `format_time(-5)`     | `-0:00:05`  |
| `format_time(-3661)`  | `-1:01:01`  |
| `format_time(0)`      | `0:00:00`   |

`print_table(lambda x: x * 10, -2, 2, width=4)`:

```
  -2 |  -20
  -1 |  -10
   0 |    0
   1 |   10
   2 |   20
```
