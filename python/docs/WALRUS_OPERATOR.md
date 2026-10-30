# Walrus operátor `:=`

Přiřazení uvnitř výrazu: do proměnné uloží hodnotu **a zároveň ji
vrátí**, takže ji jde hned použít v podmínce, `while` nebo
comprehensionu. Jmenuje se podle toho, že `:=` vypadá jako mrož
(walrus) z boku. Oficiálně *assignment expression*, Python 3.8+
([PEP 572](https://peps.python.org/pep-0572/),
[dokumentace](https://docs.python.org/3/reference/expressions.html#assignment-expressions)).

Všechny ukázky jsou ověřené na Pythonu 3.14.

## `=` vs. `:=`

| | `=` | `:=` |
|---|---|---|
| co to je | **příkaz** (statement) | **výraz** (expression) |
| vrací hodnotu | ne | ano, přiřazenou hodnotu |
| kde smí stát | na samostatném řádku | uvnitř jiného výrazu: `if`, `while`, argument funkce, comprehension |

```python
x = 5
print((y := x * 2), y)   # 10 10 — přiřadí a zároveň předá do print
```

JS obdoba: v JS je přiřazení výraz vždycky (`while ((x = f()) !== done)`),
Python to kvůli chybám typu `if x = 5` záměrně nedovoluje. `:=` je
výslovná, dobře viditelná výjimka.

## K čemu se používá

### 1. `while`: načti a otestuj v jednom

Nejčastější a nejčitelnější použití. Bez walrusu se načítá dvakrát,
nebo se píše `while True` s `break`:

```python
# bez walrusu
chunk = f.read(3)
while chunk:
    print(chunk)
    chunk = f.read(3)

# s walrusem
while chunk := f.read(3):
    print(chunk)
# abc
# def
# gh
```

Stejně s `next` a zarážkou (cvičení `06-generatory-iteratory/01`):

```python
while (value := next(iterator, done)) is not done:
    total += value
```

### 2. `if`: spočítej, otestuj a použij

```python
data = [3, 8, 1]
if (n := len(data)) > 2:
    print(f"moc prvků: {n}")   # moc prvků: 3
```

Typicky s regulárními výrazy, kde `re.search` vrací shodu nebo `None`:

```python
import re

if match := re.search(r"(\d+) Kč", "Cena: 249 Kč"):
    print(match.group(1))   # 249
```

### 3. Comprehension: nepočítat dvakrát

Když potřebuješ výsledek drahé funkce v podmínce **i** ve výsledku:

```python
def slow(v):
    print("  počítám", v)
    return v * 10


[slow(v) for v in [1, 2, 3] if slow(v) > 15]        # slow se volá 5×
[y for v in [1, 2, 3] if (y := slow(v)) > 15]       # slow se volá 3×
# obojí: [20, 30]
```

### 4. `any` / `all`: zjistit, **který** prvek podmínku splnil

`any` vrátí jen `True`/`False`. Walrus si zapamatuje poslední
zkoušený prvek, a protože `any` skončí u první shody, je to právě ona:

```python
words = ["kocka", "Pes", "slon"]
if any((w := word).istitle() for word in words):
    print("první s velkým:", w)   # první s velkým: Pes
```

Pozor: když shoda není, `w` obsahuje **poslední** prvek seznamu, ne
`None`. Proto `w` používej jen uvnitř `if`. Čitelnější alternativa je
často `next((word for word in words if word.istitle()), None)`.

## Pravidla a pasti

### Priorita: závorky skoro vždycky

`:=` má nejnižší prioritu ze všech operátorů. Bez závorek se přiřadí
celé porovnání:

```python
(n := get_n()) > 5    # n = 7, výsledek True
n := get_n() > 5      # SyntaxError na samostatném řádku
r = (n := get_n() > 5)
print(r, n)           # True True — do n se uložilo True, ne 7!
```

Pravidlo: `:=` obal závorkami, kromě případu, kdy je to **celá**
podmínka `if` / `while` (`while chunk := f.read(3):`).

### Kde nesmí stát

| Zápis | Výsledek |
|---|---|
| `x := 5` (samostatný řádek) | `SyntaxError: invalid syntax`, tady patří `=` |
| `def f(a := 1)` | `SyntaxError`, default se píše `a=1` |
| `(d["a"] := 1)`, `(obj.attr := 1)` | `SyntaxError: cannot use assignment expressions with subscript`, jen do jména proměnné |
| `[i := i + 1 for i in range(3)]` | `SyntaxError: ... cannot rebind comprehension iteration variable 'i'` |

### Proměnná z comprehensionu „uteče“ ven

Proměnná cyklu v comprehensionu (`v`) zůstane uvnitř. Proměnná
přiřazená walrusem (`y`, `w`) ale patří do okolní funkce a je vidět
i po skončení comprehensionu. To je záměr (proto funguje trik s `any`),
ale může překvapit a přepsat stejně pojmenovanou proměnnou.

## Kdy ho (ne)používat

Používej:

- `while x := načti():` místo `while True` + `break` nebo dvojího načítání
- `if m := re.search(...)` a podobné „vrať výsledek, nebo `None`“
- comprehension, kde by se drahá funkce volala dvakrát

Nepoužívej:

- místo obyčejného `=` jen pro kratší zápis
- víc walrusů v jednom výrazu, nebo walrus hluboko ve vnořeném výrazu
- když si kolega musí zápis číst dvakrát. Dva řádky s `=` jsou v pořádku

Ruff ani PEP 8 walrus nezakazují. V kódu ho uvidíš hlavně ve `while`
a u regulárních výrazů.
