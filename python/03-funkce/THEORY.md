# 03 — Funkce

## Cíl

Naučit se organizovat kód do vlastních funkcí — jak je definovat, volat,
předávat jim vstupy a dostávat výsledek zpátky — a projít i flexibilitu,
kterou Python při volání funkcí nabízí (keyword argumenty, `*args`/`**kwargs`,
positional/keyword-only oddělovače, `lambda`). Staví na
[`02-podminky-cykly`](../02-podminky-cykly/THEORY.md) — funkce běžně
obsahují `if`/`for`/`while`. Bez funkcí by šel kód jen těžko udržet, takže
je to jeden z nejdůležitějších konceptů vůbec.

## Definice funkce

```python
def add(a, b):
    return a + b

result = add(2, 3)  # 5
```

- `def` + jméno + `()` s parametry + `:`, tělo odsazené (stejně jako
  u `if`/`for`)
- `return` vrátí hodnotu a funkci **okamžitě** ukončí; bez `return` funkce
  vrátí `None`
- `return a, b` vrátí víc hodnot najednou (technicky jde o tuple — víc
  u datových struktur, tady stačí umět si to zapsat/rozbalit)

## Parametry s výchozí hodnotou

```python
def greet(name, greeting="Ahoj"):
    print(f"{greeting}, {name}!")

greet("Petr")             # Ahoj, Petr!
greet("Petr", "Zdravím")   # Zdravím, Petr!
```

## Keyword argumenty

Argument lze při volání předat podle jména parametru — pak nezáleží na
pořadí:

```python
greet(name="Petr", greeting="Čau")
greet(greeting="Čau", name="Petr")  # stejný výsledek
```

## Oddělovače `/` a `*`

Umožňují vynutit, **jak** se parametr smí předat:

```python
def f(a, b, /, c, d, *, e, g):
    ...
```

- `a`, `b` (před `/`) — jen pozičně, nejdou zadat jako `a=1`
- `c`, `d` (mezi `/` a `*`) — pozičně i podle jména
- `e`, `g` (za `*`) — jen podle jména, nejdou zadat pozičně

## `*args` a `**kwargs`

Když dopředu nevíš, kolik argumentů přijde:

```python
def sum_all(*numbers):
    total = 0
    for number in numbers:
        total += number
    return total

sum_all(1, 2, 3)  # 6

def print_info(**info):
    for key in info:
        print(f"{key}: {info[key]}")

print_info(name="Petr", age=30)
```

`**kwargs` je uvnitř funkce dict (slovník) — podrobně se probere u
datových struktur, tady stačí umět s ním takhle základně pracovat.

## Rozsah platnosti (scope)

Proměnná definovaná uvnitř funkce je **lokální** — mimo funkci neexistuje.
Číst globální proměnnou uvnitř funkce jde bez problému, ale pro **zápis**
do ní potřebuješ `global`:

```python
count = 0

def increment():
    global count
    count += 1
```

## Lambda výrazy

Anonymní (bezejmenná) jednořádková funkce — jen jeden výraz, žádný
`return`, žádné víceřádkové tělo:

```python
square = lambda x: x ** 2
square(5)  # 25
```

Hodí se pro krátké, jednorázové funkce — víc se to ukáže u `map`/`filter`/
`sorted(key=...)` v konceptu vestavěných funkcí.

## Rekurze

Funkce, která volá sama sebe. Potřebuje **základní případ** (base case),
kdy se přestane volat znovu — jinak poběží navždy (respektive do
`RecursionError`):

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
