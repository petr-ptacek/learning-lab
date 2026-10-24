# 04 — Řazení

`sorted` s parametry `key` a `reverse`, řazení podle víc kritérií.

## Požadavky

- V kódu měj seznam:

  ```python
  words = ["kocka", "Pes", "slon", "auto", "Zebra", "mys"]
  ```

- Napiš tyto funkce (každá jedno volání `sorted`):
  - `sort_alpha(words)` — abecedně **bez ohledu na velikost písmen**.
  - `sort_by_length(words)` — podle délky, při stejné délce abecedně
    (bez ohledu na velikost písmen).
  - `top_n(scores, n)` — ze slovníku `jméno → body` vrátí seznam
    `n` dvojic `(jméno, body)` s nejvíc body. Při shodě bodů rozhoduje
    jméno abecedně.
- Vypiš i `sorted(words)` bez `key` a vysvětli si (komentářem), proč
  `Pes` a `Zebra` skončily na začátku.
- Ověř, že `sorted` původní seznam nezmění, a porovnej s `words.sort()`
  — co vrací?

### Příklady vstup/výstup

| Volání                   | Výsledek                                                   |
|--------------------------|------------------------------------------------------------|
| `sorted(words)`          | `['Pes', 'Zebra', 'auto', 'kocka', 'mys', 'slon']`         |
| `sort_alpha(words)`      | `['auto', 'kocka', 'mys', 'Pes', 'slon', 'Zebra']`         |
| `sort_by_length(words)`  | `['mys', 'Pes', 'auto', 'slon', 'kocka', 'Zebra']`         |
| `sort_alpha([])`         | `[]`                                                       |

Pro `scores = {"Anna": 87, "Petr": 92, "Eva": 87, "Jana": 75}`:

| Volání              | Výsledek                                                       |
|---------------------|----------------------------------------------------------------|
| `top_n(scores, 2)`  | `[('Petr', 92), ('Anna', 87)]`                                 |
| `top_n(scores, 3)`  | `[('Petr', 92), ('Anna', 87), ('Eva', 87)]`                    |
| `top_n(scores, 10)` | `[('Petr', 92), ('Anna', 87), ('Eva', 87), ('Jana', 75)]`      |
| `top_n(scores, 0)`  | `[]`                                                           |
| `top_n({}, 3)`      | `[]`                                                           |

## Bonus

- Seřaď sklad z `04-datove-struktury/10-sklad` podle kategorie
  (abecedně) a v rámci kategorie podle ceny **sestupně**. Vrať seznam
  názvů.

### Příklady vstup/výstup (bonus)

| Vstup                         | Výsledek                                              |
|-------------------------------|-------------------------------------------------------|
| `products` z `10-sklad`       | `['Šampon', 'Mýdlo', 'Káva', 'Chléb', 'Mléko']`       |
| `[]`                          | `[]`                                                  |
