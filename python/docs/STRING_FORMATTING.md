# Formátovací mini-jazyk

Shrnutí a příklady toho, co se dá napsat za `:` uvnitř `{}` ve f-stringu.
Základ je v [`01-zaklady/THEORY.md`](../01-zaklady/THEORY.md#formátovací-mini-jazyk),
tady je kompletní přehled. Výstupy jsou ověřené na Pythonu 3.14.

Oficiální docs:
[Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language),
[f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

## Syntaxe

```
{hodnota:[[fill]align][sign][z][#][0][width][grouping][.precision][type]}
```

Všechny části jsou volitelné, ale **pořadí je pevné**. Nejčastější
kombinace jsou `width`, `align`, `.precision` a `type`, třeba
`{x:>10.2f}`.

| Část        | Hodnoty                      | Význam                                  |
|-------------|------------------------------|-----------------------------------------|
| `fill`      | libovolný znak               | čím doplnit volné místo (výchozí mezera) |
| `align`     | `<` `>` `^` `=`              | doleva / doprava / na střed / za znaménko |
| `sign`      | `+` `-` ` `                  | jak zobrazit znaménko                   |
| `z`         | `z`                          | `-0.00` → `0.00`                        |
| `#`         | `#`                          | prefix `0b` / `0o` / `0x`               |
| `0`         | `0`                          | doplnit nulami (u čísel)                |
| `width`     | číslo                        | **minimální** šířka pole                |
| `grouping`  | `,` `_`                      | oddělovač tisíců                        |
| `.precision`| `.` + číslo                  | desetinná místa / max. délka textu      |
| `type`      | `d` `f` `e` `%` `g` `b` `x` … | jak hodnotu vypsat                      |

Ve všech příkladech níže platí:

```python
name = "Petr"
n = 42
neg = -7
pi = 3.14159265
price = 1234567.891
share = 0.256
```

## Šířka (délka pole)

`width` je **minimální** šířka. Delší hodnota se nikdy neořízne, jen
přeteče.

```python
f"[{name:10}]"   # '[Petr      ]'  text je ve výchozím stavu vlevo
f"[{n:10}]"      # '[        42]'  číslo je ve výchozím stavu vpravo
f"[{name:3}]"    # '[Petr]'        nic se neořízne, šířka 3 je jen minimum
```

Pro text ořízne délku `.precision`:

```python
f"[{name:.2}]"   # '[Pe]'          max. 2 znaky
f"[{name:5.2}]"  # '[Pe   ]'       ořízni na 2, pak doplň na šířku 5
```

## Zarovnání a centrování

```python
f"[{name:<10}]"  # '[Petr      ]'  doleva
f"[{name:>10}]"  # '[      Petr]'  doprava
f"[{name:^10}]"  # '[   Petr   ]'  na střed
f"[{name:^9}]"   # '[  Petr   ]'   lichý zbytek jde doprava
f"[{neg:=6}]"    # '[-    7]'      znaménko vlevo, číslo vpravo (jen čísla)
```

Bez `width` zarovnání nic nedělá. Není kam zarovnávat.

## Fill (výplňový znak)

Znak **těsně před** zarovnáním:

```python
f"[{name:*<10}]" # '[Petr******]'
f"[{name:->10}]" # '[------Petr]'
f"[{name:.^10}]" # '[...Petr...]'
f"{'':=^20}"     # '===================='  oddělovací čára
```

`fill` jde použít **jen spolu s `align`**. Zápis `f"{name:*10}"` vyhodí
`ValueError: Invalid format specifier`.

### Doplnění nulami: `0` vs. `0>`

```python
f"{n:05}"        # '00042'
f"{neg:05}"      # '-0007'  nuly za znaménkem (správně)
f"{neg:0>5}"     # '000-7'  nula jako obyčejný fill (špatně u záporných)
f"{n:+08.2f}"    # '+0042.00'
```

Na čísla používej `05`. Zápis `0>5` je jen text doplněný nulami zleva.

## Oddělovače tisíců

```python
f"{1234567:,}"       # '1,234,567'
f"{price:,}"         # '1,234,567.891'
f"{price:_}"         # '1_234_567.891'
f"{price:,.2f}"      # '1,234,567.89'
f"{0xFFFFFFFF:_x}"   # 'ffff_ffff'   u b/o/x seskupuje po 4 číslicích
f"{pi:.6_f}"         # '3.141_593'   od 3.14 i v desetinné části
```

Mini-jazyk zná jen `,` a `_`. **Český formát** (mezera a desetinná čárka)
přímo neumí. Nejjednodušší je ho nahradit:

```python
f"{price:,.2f}".replace(",", " ").replace(".", ",")   # '1 234 567,89'
```

Alternativa je `locale` + typ `n`. Ten ale závisí na nastavení systému,
takže pro výuku stačí `replace`.

## Přesnost a typy čísel

```python
f"{pi:.2f}"      # '3.14'        f = pevný počet desetinných míst
f"{n:.2f}"       # '42.00'       funguje i na int
f"{pi:.0f}"      # '3'
f"{2.5:.0f}"     # '2'           banker's rounding: .5 se zaokrouhlí k sudé
f"{pi:.3}"       # '3.14'        bez typu: 3 PLATNÉ číslice, ne desetinná místa
f"{price:.3e}"   # '1.235e+06'   vědecký zápis
f"{1/3:g}"       # '0.333333'    g = "chytrý" formát, zvolí f nebo e
f"{1e-7:g}"      # '1e-07'
```

### Procenta

`%` vynásobí hodnotu stem a přidá `%`:

```python
f"{share:.1%}"   # '25.6%'
f"{share:.0%}"   # '26%'
f"{share:%}"     # '25.600000%'  výchozí přesnost je 6
```

### Znaménko

```python
f"{n:+}"         # '+42'         vždy zobraz znaménko
f"{neg:+}"       # '-7'
f"[{n: }]"       # '[ 42]'       mezera místo +, aby kladná a záporná lícovala
f"{-0.0001:.2f}" # '-0.00'
f"{-0.0001:z.2f}"# '0.00'        z = zahodit záporné nuly
```

### Celá čísla v jiných soustavách

```python
f"{n:d}"         # '42'          desítková
f"{n:b}"         # '101010'      binární
f"{n:o}"         # '52'          osmičková
f"{n:x}"         # '2a'          šestnáctková
f"{n:X}"         # '2A'
f"{n:#b}"        # '0b101010'    # = přidej prefix
f"{n:#x}"        # '0x2a'
f"{n:08b}"       # '00101010'    8 bitů
f"{n:#010b}"     # '0b00101010'  šířka 10 počítá i prefix 0b
f"{255:#06x}"    # '0x00ff'
```

## Další triky ve f-stringu

Tohle už nepatří k samotnému mini-jazyku, ale ve f-stringu se to hodí.

```python
f"{n=}"          # 'n=42'          debug výpis: jméno i hodnota
f"{n = }"        # 'n = 42'        mezery se zachovají
f"{pi=:.2f}"     # 'pi=3.14'       debug + formát
f"{name!r}"      # "'Petr'"        repr() místo str(), vidíš uvozovky
f"{{n}} = {n}"   # '{n} = 42'      {{ }} = doslovné závorky
```

### Dynamická šířka / fill

Specifikace může obsahovat další `{}`:

```python
fill = "~"
width = 12
f"[{name:{fill}^{width}}]"   # '[~~~~Petr~~~~]'
```

Hodí se, když se šířka sloupce počítá podle nejdelší položky.

### Datum a čas

Objekty `datetime` mají vlastní formátovací jazyk (`strftime` kódy):

```python
from datetime import datetime
f"{datetime(2026, 10, 17, 9, 5):%d.%m.%Y %H:%M}"   # '17.10.2026 09:05'
```

Přehled kódů:
[strftime() and strptime() Format Codes](https://docs.python.org/3/library/datetime.html#format-codes).

## Příklad: tabulka

```python
items = [("Rohlík", 12, 2.9), ("Máslo", 1, 64.9), ("Káva zrnková", 2, 289.0)]

print(f"{'Položka':<14}{'Ks':>4}{'Cena':>10}")
print("-" * 28)
for name, qty, price in items:
    print(f"{name:<14}{qty:>4}{qty * price:>10,.2f}")
print("=" * 28)
total = sum(qty * price for _, qty, price in items)
print(f"{'Celkem':<14}{total:>14,.2f}")
```

```
Položka         Ks      Cena
----------------------------
Rohlík          12     34.80
Máslo            1     64.90
Káva zrnková     2    578.00
============================
Celkem                677.70
```

Pravidlo: **text doleva, čísla doprava**, u peněz pevný počet desetinných
míst. Jinak desetinné tečky pod sebou nelícují.

## Časté chyby

| Zápis               | Problém                                                 |
|---------------------|---------------------------------------------------------|
| `f"{name:*10}"`     | `fill` bez `align`, chybí `<`/`>`/`^`                   |
| `f"{name:d}"`       | `d` je jen pro čísla (`Unknown format code 'd'`)        |
| `f"{n:,s}"`         | oddělovač tisíců na textu nedává smysl                  |
| `f"{pi:.3}"`        | čekáš 3 desetinná místa, dostaneš 3 platné číslice (`.3f`) |
| `f"{neg:0>5}"`      | nuly před znaménkem (`000-7`), použij `05`              |
| `f"{text:>5}"`      | delší text se neořízne, šířka je minimum                |

## Starší zápisy (pro čtení cizího kódu)

Stejný mini-jazyk používá i `str.format()` a `format()`. Starý `%` styl
má vlastní, podobnou syntaxi:

```python
format(n, ">5")                  # '   42'
"{:>5}|{:.2f}".format(n, pi)     # '   42|3.14'
"%5d|%.2f" % (n, pi)             # '   42|3.14'  printf styl, v novém kódu nepoužívej
```

V novém kódu piš f-stringy.
