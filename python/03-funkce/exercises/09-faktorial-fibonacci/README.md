# 09 — Faktoriál a Fibonacci

Vyzkoušej si rekurzi — funkci, která volá sama sebe.

## Požadavky

- Napiš rekurzivní funkci `faktorial(n)` — vrátí `n!` (`1` pro `n <= 1`,
  jinak `n * faktorial(n - 1)`).
- Napiš rekurzivní funkci `fibonacci(n)` — vrátí n-tý člen Fibonacciho
  posloupnosti (`fibonacci(0) = 0`, `fibonacci(1) = 1`, jinak
  `fibonacci(n - 1) + fibonacci(n - 2)`).
- Načti číslo `n` a vypiš obě hodnoty.
- Výstup např.:

```
Zadej n: 5
5! = 120
fibonacci(5) = 5
```

### Příklady vstup/výstup

| n | Výstup                              |
|---|--------------------------------------|
| 5 | `5! = 120, fibonacci(5) = 5`         |
| 0 | `0! = 1, fibonacci(0) = 0`           |
| 6 | `6! = 720, fibonacci(6) = 8`         |
| 1 | `1! = 1, fibonacci(1) = 1`           |

## Bonus

- Pomocí globální proměnné a `global` počítej, kolikrát se `faktorial`
  za jedno spuštění rekurzivně zavolal (včetně prvního zavolání), a vypiš
  to.

### Příklady vstup/výstup (bonus)

| n | Výstup navíc          |
|---|-------------------------|
| 5 | `Počet volání: 6`       |
| 0 | `Počet volání: 1`       |
