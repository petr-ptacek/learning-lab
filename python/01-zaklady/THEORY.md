# 01 — Základy

## Cíl

Naučit se základní stavební kameny Pythonu, bez kterých se nedá napsat ani
jednoduchý skript: jak Python spustit, jak si uložit hodnotu do proměnné,
jaké jsou základní datové typy a jak se s uživatelem "bavit" přes vstup a
výstup. Vše ostatní (podmínky, cykly, funkce, ...) na tomhle staví.

## Spuštění

- `python3 --version` — ověření, že máš Python nainstalovaný
- `python3 soubor.py` — spuštění skriptu
- `python3` — interaktivní konzole (REPL), dobré na rychlé zkoušení

## Proměnné

Python je dynamicky typovaný — typ se neuvádí, odvodí se z hodnoty.

```python
jmeno = "Petr"
vek = 30
vyska = 178.5
je_student = False
```

## Základní datové typy

| Typ     | Příklad        | Poznámka                       |
|---------|----------------|--------------------------------|
| `int`   | `42`           | celé číslo                     |
| `float` | `3.14`         | desetinné číslo                |
| `str`   | `"ahoj"`       | řetězec, `'` i `"` jsou stejné |
| `bool`  | `True`/`False` | pozor na velké první písmeno   |

Zjištění typu: `type(vek)`.

## Vstup a výstup

```python
jmeno = input("Jak se jmenuješ? ")  # input() vrací vždy str
print(f"Ahoj, {jmeno}!")  # f-string — vkládání proměnných do textu
```

`input()` vrací vždy string — pokud potřebuješ číslo, je nutná konverze:

```python
vek = int(input("Kolik ti je let? "))
```

## Formátovací mini-jazyk

Uvnitř `{}` ve f-stringu můžeš za hodnotu přidat `:` a specifikaci formátu:
`{hodnota:zarovnání šířka .přesnost typ}`.

```python
f"{'Kelvin:':<12}"     # doleva, doplní mezerami na šířku 12
f"{cislo:>10.1f}"      # doprava, šířka 10, 1 desetinné místo
f"{cislo:^10}"         # na střed, šířka 10
f"{cena:,.2f}"         # tisícový oddělovač + 2 desetinná místa
f"{podil:.0%}"         # zobrazí jako procenta, 0 desetinných míst
```

Výchozí zarovnání: čísla doprava, text doleva. Bez specifikace šířky se nic
nedoplňuje — zarovnání má smysl, jen když je šířka pole pevná.

## Konverze typů

- `int("42")` → `42`
- `float("3.14")` → `3.14`
- `str(42)` → `"42"`

Konverze selže (vyhodí `ValueError`), pokud text není platné číslo — s tím se
zatím nemusíš zabývat, na výjimky dojde v pozdějším tématu.

## Operátory

- aritmetické: `+ - * /` (dělení vrací vždy `float`), `//` (celočíselné dělení),
  `%` (zbytek po dělení), `**` (mocnina)
- porovnávací: `== != < > <= >=`
- řetězce: `+` (spojení), `*` (opakování — `"ab" * 3` → `"ababab"`)

## Komentáře

```python
# jednořádkový komentář
```
