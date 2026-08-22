# 02 — Přivítání

Vyzkoušej si parametr s výchozí hodnotou.

## Požadavky

- Napiš funkci `pozdrav(jmeno, text="Ahoj")` — druhý parametr má výchozí
  hodnotu `"Ahoj"`.
- Funkce vrátí (nevypisuje!) zprávu ve tvaru `"{text}, {jmeno}!"`.
- Zavolej funkci jednou jen se jménem (použije se výchozí `text`) a jednou
  se jménem i vlastním textem — obojí na základě `input()` (prázdný vstup
  u `text` = použij výchozí hodnotu).
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

- Přidej třetí volitelný parametr `pocet_vykricniku=1`, který určí, kolik
  vykřičníků se má na konci zprávy vypsat místo jednoho.

### Příklady vstup/výstup (bonus)

| Jméno | Text      | Počet vykřičníků | Výstup             |
|-------|-----------|-------------------|---------------------|
| Petr  | (prázdné) | 3                 | `Ahoj, Petr!!!`     |
| Eva   | `Čau`     | 1                 | `Čau, Eva!`         |
