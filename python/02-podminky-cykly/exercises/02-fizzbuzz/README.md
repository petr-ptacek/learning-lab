# 02 — FizzBuzz

Klasika. Napiš skript, který načte horní hranici `n` a vypíše čísla od 1 do
`n`, přičemž:

- pokud je číslo dělitelné 3, vypiš `Fizz` místo čísla
- pokud je dělitelné 5, vypiš `Buzz` místo čísla
- pokud je dělitelné 3 i 5 zároveň, vypiš `FizzBuzz`
- jinak vypiš číslo samotné

## Požadavky

- Použij `for` cyklus s `range()`.
- Pořadí podmínek v `if`/`elif` promysli tak, aby `FizzBuzz` (dělitelné oběma)
  nikdy nezapadlo pod samostatnou podmínku pro 3 nebo pro 5.
- Výstup pro `n = 15` např.:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

## Bonus

- Uprav skript, ať čísla, na kterých se testuje dělitelnost (3 a 5), i slova
  (`Fizz`, `Buzz`) může uživatel sám zadat na vstupu.
