# 06 — Profil

Vyzkoušej si `**kwargs` — libovolný počet keyword argumentů.

## Požadavky

- Napiš funkci `vypis_profil(**udaje)`, která vypíše každý předaný
  keyword argument na vlastním řádku ve tvaru `"{klíč}: {hodnota}"`
  (pomocí `for klic in udaje: ...`).
- Zavolej ji v kódu natvrdo dvakrát s různými klíči, např.:
  - `vypis_profil(jmeno="Petr", vek=30)`
  - `vypis_profil(mesto="Brno", povolani="programátor", vek=25)`
- Výstup např.:

```
jmeno: Petr
vek: 30
```

### Příklady vstup/výstup

| Volání                                                        | Výstup                                              |
|-----------------------------------------------------------------|------------------------------------------------------|
| `vypis_profil(jmeno="Petr", vek=30)`                             | `jmeno: Petr` / `vek: 30`                             |
| `vypis_profil(mesto="Brno", povolani="programátor", vek=25)`     | `mesto: Brno` / `povolani: programátor` / `vek: 25`   |
| `vypis_profil()`                                                 | (nic — žádný klíč, žádný řádek)                       |

## Bonus

- Napiš i funkci `pocet_udaju(**udaje)`, která vrátí, kolik klíčů bylo
  předáno (`len(udaje)`), a vypiš to za profilem.

### Příklady vstup/výstup (bonus)

| Volání                                                       | Výstup navíc      |
|------------------------------------------------------------------|--------------------|
| `pocet_udaju(jmeno="Petr", vek=30)`                               | `Počet údajů: 2`   |
| `pocet_udaju(mesto="Brno", povolani="programátor", vek=25)`       | `Počet údajů: 3`   |
