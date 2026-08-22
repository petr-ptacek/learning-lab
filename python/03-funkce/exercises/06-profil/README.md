# 06 — Profil

Vyzkoušej si `**kwargs` — libovolný počet keyword argumentů.

## Požadavky

- Napiš funkci `print_profile(**info)`, která vypíše každý předaný keyword argument na vlastním řádku ve tvaru
  `"{klíč}: {hodnota}"`
  (pomocí `for key in info: ...`).
- Zavolej ji v kódu natvrdo dvakrát s různými klíči, např.:
    - `print_profile(name="Petr", age=30)`
    - `print_profile(city="Brno", occupation="programátor", age=25)`
- Výstup např.:

```
name: Petr
age: 30
```

### Příklady vstup/výstup

| Volání                                                         | Výstup                                               |
|----------------------------------------------------------------|------------------------------------------------------|
| `print_profile(name="Petr", age=30)`                           | `name: Petr` / `age: 30`                             |
| `print_profile(city="Brno", occupation="programátor", age=25)` | `city: Brno` / `occupation: programátor` / `age: 25` |
| `print_profile()`                                              | (nic — žádný klíč, žádný řádek)                      |

## Bonus

- Napiš i funkci `data_count(**info)`, která vrátí, kolik klíčů bylo předáno (`len(info)`), a vypiš to za profilem.

### Příklady vstup/výstup (bonus)

| Volání                                                      | Výstup navíc     |
|-------------------------------------------------------------|------------------|
| `data_count(name="Petr", age=30)`                           | `Počet údajů: 2` |
| `data_count(city="Brno", occupation="programátor", age=25)` | `Počet údajů: 3` |
