# 02 — Podmínky a cykly

## Cíl

Naučit se řídit tok programu: rozhodovat se podle podmínky a opakovat kód,
aniž bys ho musel psát vícekrát (jak jsi dělal u cvičení s "3x stejný
`input()`" v základech). Tohle je nástroj, který v základech chyběl a
u posledních cvičení ti očividně chyběl.

## Podmínky

```python
vek = int(input("Kolik ti je let? "))

if vek < 0:
    print("Neplatný věk")
elif vek < 18:
    print("Nezletilý")
else:
    print("Dospělý")
```

Blok patřící k podmínce se pozná podle **odsazení** (běžně 4 mezery) — Python
na rozdíl od jiných jazyků nepoužívá `{}`.

Logické operátory: `and`, `or`, `not` (místo `&&`, `||`, `!`).

```python
if vek >= 18 and vek < 65:
    print("Produktivní věk")
```

"Truthy" a "falsy" hodnoty — `if` nevyžaduje jen `bool`, kontroluje
pravdivost hodnoty. Za nepravdivé (falsy) se považuje: `0`, `0.0`, `""`
(prázdný string), `None`. Cokoliv jiného je "truthy".

## Cykly — `for`

Nejčastěji ve spojení s `range(start, stop, step)`:

```python
for i in range(1, 6):   # 1, 2, 3, 4, 5 — "stop" není zahrnuté
    print(i)
```

`for` umí procházet i přímo string (znak po znaku):

```python
for pismeno in "ahoj":
    print(pismeno)
```

## Cykly — `while`

Opakuje, dokud platí podmínka — hodí se, když předem nevíš, kolikrát se má
cyklus provést (např. dokud uživatel neuhodne číslo):

```python
pokusy = 0
while pokusy < 3:
    print("pokus")
    pokusy += 1   # bez tohohle by cyklus běžel navždy
```

## `break` a `continue`

- `break` — okamžitě cyklus ukončí
- `continue` — přeskočí zbytek aktuální iterace a pokračuje další
