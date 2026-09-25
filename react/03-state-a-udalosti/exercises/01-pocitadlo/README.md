# 01 — Počítadlo

První interaktivní komponenta — procvič si `useState` a event handlery.

## Požadavky

- Napiš komponentu `Counter`, která si přes `useState` drží číslo (počáteční hodnota `0`).
- Zobraz aktuální hodnotu a tři tlačítka: `+1`, `-1`, `Reset`.
- `+1`/`-1` mění hodnotu o 1 (použij funkcionální update, viz `THEORY.md`).
- `Reset` vrátí hodnotu zpět na `0`.
- V `App` vykresli `Counter`.

### Příklady akcí → zobrazená hodnota

| Akce (v pořadí)                    | Zobrazená hodnota |
|------------------------------------|-------------------|
| (start)                            | `0`               |
| klik `+1`, klik `+1`               | `2`               |
| klik `+1`, klik `+1`, klik `-1`    | `1`               |
| klik `+1`, klik `+1`, klik `Reset` | `0`               |
| klik `-1`, klik `-1`               | `-2`              |

## Bonus

- Přidej controlled input pro **krok** (výchozí hodnota `1`), kterým se tlačítka `+1`/`-1` řídí — přejmenuj je na
  `+krok`/`-krok`.
- `Reset` vrátí na `0` jen počítadlo, krok nechá beze změny.

### Příklady akcí → zobrazená hodnota (bonus)

| Akce (v pořadí)                                | Zobrazená hodnota (počítadlo) |
|------------------------------------------------|-------------------------------|
| (start), krok = `1`                            | `0`                           |
| nastav krok na `5`, klik `+krok`               | `5`                           |
| klik `+krok` (krok pořád `5`)                  | `10`                          |
| klik `-krok`, klik `-krok`                     | `0`                           |
| nastav krok na `3`, klik `+krok`, klik `Reset` | `0` (krok zůstává `3`)        |
