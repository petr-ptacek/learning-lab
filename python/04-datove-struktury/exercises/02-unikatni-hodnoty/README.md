# 02 — Unikátní hodnoty

Vytváření nového seznamu cyklem, operátor `in` a rozdíl mezi „vrátit nový
seznam“ a „změnit původní“.

## Požadavky

- Napiš funkci `unique(items)`, která vrátí **nový** seznam bez duplicit
  a zachová pořadí prvního výskytu. Použij `in` (ne `set` — ten pořadí
  nezaručuje).
- Napiš funkci `reverse(items)`, která vrátí nový, obrácený seznam.
  Postav ho **cyklem** — bez `[::-1]` a bez `.reverse()`. Výsledek pak
  porovnej s `items[::-1]` (`==`) a vypiš, jestli sedí.
- Původní seznam se ani u jedné funkce **nesmí změnit** — ověř to
  výpisem po zavolání.
- Vyzkoušej všechny seznamy z tabulky.

### Příklady vstup/výstup

| `items`            | `unique(items)` | `reverse(items)`    |
|--------------------|-----------------|---------------------|
| `[1, 2, 2, 3, 1]`  | `[1, 2, 3]`     | `[1, 3, 2, 2, 1]`   |
| `[]`               | `[]`            | `[]`                |
| `["a", "A", "a"]`  | `['a', 'A']`    | `['a', 'A', 'a']`   |
| `[5, 5, 5]`        | `[5]`           | `[5, 5, 5]`         |
| `[3, 1, 2]`        | `[3, 1, 2]`     | `[2, 1, 3]`         |

## Bonus

- Napiš funkci `duplicates(items)`, která vrátí hodnoty, které se
  v seznamu vyskytují **víc než jednou** — každou jen jednou, v pořadí
  prvního výskytu. Můžeš použít metodu `.count()`.

### Příklady vstup/výstup (bonus)

| `items`           | `duplicates(items)` |
|-------------------|---------------------|
| `[1, 2, 2, 3, 1]` | `[1, 2]`            |
| `[3, 1, 2]`       | `[]`                |
| `["a", "A", "a"]` | `['a']`             |
| `[5, 5, 5]`       | `[5]`               |
| `[]`              | `[]`                |
