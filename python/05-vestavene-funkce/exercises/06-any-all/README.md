# 06 — Any a all

`any` / `all` s generátorovým výrazem — „platí to pro některý / pro
všechny prvky?“ bez ručního cyklu a příznaku `found`.

## Požadavky

- Napiš funkci `is_valid_password(password)`, která vrátí `True`, pokud
  heslo:
  - má aspoň 8 znaků,
  - obsahuje **aspoň jednu** číslici (`c.isdigit()`),
  - obsahuje **aspoň jedno** velké písmeno (`c.isupper()`),
  - **neobsahuje žádnou** mezeru.

  Každé pravidlo kromě délky jedním `any` nebo `all`.
- Napiš funkce `all_passed(scores, limit=50)` a `any_failed(scores,
  limit=50)` — prošli všichni (body `>= limit`)? / neprošel aspoň jeden?
- Rozmysli si (komentářem), proč `all_passed([])` vrací `True`.

### Příklady vstup/výstup

| `password`      | `is_valid_password` | Proč                   |
|-----------------|---------------------|------------------------|
| `Heslo123`      | `True`              |                        |
| `HESLOHESLO1`   | `True`              |                        |
| `heslo123`      | `False`             | chybí velké písmeno    |
| `Heslohes`      | `False`             | chybí číslice          |
| `Heslo1`        | `False`             | krátké                 |
| `Hes lo123`     | `False`             | mezera                 |

| `scores`         | `all_passed` | `any_failed` |
|------------------|--------------|--------------|
| `[80, 65, 90]`   | `True`       | `False`      |
| `[80, 45, 90]`   | `False`      | `True`       |
| `[50]`           | `True`       | `False`      |
| `[]`             | `True`       | `False`      |

## Bonus

- `is_sorted(numbers)` — je seznam seřazený vzestupně (stejné hodnoty
  smí být vedle sebe)? Jedním `all` se `zip` sousedních prvků.
- `has_duplicates(numbers)` — obsahuje seznam nějakou hodnotu víckrát?
  Jedním řádkem bez cyklu (nápověda: `set`).

### Příklady vstup/výstup (bonus)

| `numbers`        | `is_sorted` | `has_duplicates` |
|------------------|-------------|------------------|
| `[1, 2, 2, 3]`   | `True`      | `True`           |
| `[1, 3, 2]`      | `False`     | `False`          |
| `[3, 1]`         | `False`     | `False`          |
| `[5]`            | `True`      | `False`          |
| `[]`             | `True`      | `False`          |
