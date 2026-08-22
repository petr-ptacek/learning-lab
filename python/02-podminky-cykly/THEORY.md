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

## Vnořené cykly

Cyklus může obsahovat další cyklus (typicky pro tabulky/mřížky — např.
násobilka). Vnitřní cyklus se provede celý pro každou jednu iteraci
vnějšího:

```python
for radek in range(1, 4):
    for sloupec in range(1, 4):
        print(f"{radek}x{sloupec}", end=" ")
    print()  # nový řádek po dokončení vnitřního cyklu
```

`break`/`continue` uvnitř vnitřního cyklu ovlivní jen ten vnitřní, ne ten
vnější.

## `else` u `for`/`while`

Málo známá, ale užitečná vlastnost — `else` u cyklu se provede, pokud
cyklus doběhl **bez** `break`u. Hodí se místo příznakové (`bool`)
proměnné, když něco hledáš:

```python
for cislo in range(2, n):
    if n % cislo == 0:
        print("Není prvočíslo")
        break
else:
    print("Je prvočíslo")
```

## Ternární výraz (podmínka na jeden řádek)

Zkrácený zápis `if`/`else`, když jen vybíráš mezi dvěma hodnotami:

```python
stav = "dospělý" if vek >= 18 else "nezletilý"
```

Vhodné pro jednoduché přiřazení, ne pro víc větví nebo delší logiku —
tam pořád patří normální `if`/`elif`/`else`.

## `while True` + `break`

Časté v hrách/menu — cyklus, který běží "navždy", dokud ho nezastavíš
podmínkou uvnitř (viz cvičení "Hádej číslo"):

```python
while True:
    pokus = input("Zadej: ")
    if pokus == "konec":
        break
```
