# 02 — Přivítání

Vyzkoušej si parametr s výchozí hodnotou.

## Požadavky

- Napiš funkci `greet(name, greeting="Ahoj")` — druhý parametr má výchozí
  hodnotu `"Ahoj"`.
- Funkce vrátí (nevypisuje!) zprávu ve tvaru `"{greeting}, {name}!"`.
- Zavolej funkci jednou jen se jménem (použije se výchozí `greeting`) a
  jednou se jménem i vlastním pozdravem — obojí na základě `input()`
  (prázdný vstup u pozdravu = použij výchozí hodnotu).
- Výstup např.:

```
Zadej jméno: Petr
Zadej pozdrav (nebo nic pro výchozí): 
Ahoj, Petr!
```

### Příklady vstup/výstup

| Jméno | Text (vstup) | Výstup           |
|-------|--------------|------------------|
| Petr  | (prázdné)    | `Ahoj, Petr!`    |
| Petr  | `Zdravím`    | `Zdravím, Petr!` |
| Eva   | `Čau`        | `Čau, Eva!`      |

## Bonus

- Přidej třetí volitelný parametr `exclamation_count=1`, který určí,
  kolik vykřičníků se má na konci zprávy vypsat místo jednoho.

### Příklady vstup/výstup (bonus)

| Jméno | Text      | Počet vykřičníků | Výstup             |
|-------|-----------|-------------------|---------------------|
| Petr  | (prázdné) | 3                 | `Ahoj, Petr!!!`     |
| Eva   | `Čau`     | 1                 | `Čau, Eva!`         |
