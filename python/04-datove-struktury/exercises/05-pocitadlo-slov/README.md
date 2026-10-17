# 05 — Počítadlo slov

První `dict` — klíč je slovo, hodnota počet výskytů. Typický vzor
`counts[key] = counts.get(key, 0) + 1`.

Na rozdělení textu potřebuješ dvě metody řetězce, které podrobně přijdou
až v `07-stringy`: `text.lower()` (malá písmena) a `text.split()`
(rozdělí podle mezer na seznam slov).

## Požadavky

- Napiš funkci `count_words(text)`, která vrátí dict `slovo → počet`.
  Velikost písmen nerozhoduje (`Pes` = `pes`).
- Napiš funkci `most_common(counts)`, která vrátí tuple `(slovo, počet)`
  nejčastějšího slova. Při shodě vyhrává slovo, které se v textu objevilo
  **dřív**. Pro prázdný dict vrať `None`. Bez `max()`.
- Načti text přes `input()` a vypiš každé slovo na samostatný řádek
  (`slovo: počet`) v pořadí prvního výskytu, pak nejčastější slovo.
- Výstup např.:

```
Text: jedna dva tri dva jedna jedna
jedna: 3
dva: 2
tri: 1
Nejčastější: jedna (3×)
```

### Příklady vstup/výstup

| Text                              | `count_words(text)`                     | `most_common(...)` |
|-----------------------------------|-----------------------------------------|--------------------|
| `a b a`                           | `{'a': 2, 'b': 1}`                      | `('a', 2)`         |
| `Pes pes PES kocka`               | `{'pes': 3, 'kocka': 1}`                | `('pes', 3)`       |
| `jedna dva tri dva jedna jedna`   | `{'jedna': 3, 'dva': 2, 'tri': 1}`      | `('jedna', 3)`     |
| `kolo auto kolo vlak auto`        | `{'kolo': 2, 'auto': 2, 'vlak': 1}`     | `('kolo', 2)`      |
| (prázdný text)                    | `{}`                                    | `None`             |

U prázdného textu vypiš místo nejčastějšího slova `Žádná slova`.

## Bonus

- Napiš funkci `group_by_length(text)`, která vrátí dict
  `délka slova → seznam unikátních slov té délky` (v pořadí prvního
  výskytu). Hodnotou je tedy **list uvnitř dictu**.

### Příklady vstup/výstup (bonus)

| Text                              | `group_by_length(text)`                |
|-----------------------------------|----------------------------------------|
| `a b a`                           | `{1: ['a', 'b']}`                      |
| `Pes pes PES kocka`               | `{3: ['pes'], 5: ['kocka']}`           |
| `jedna dva tri dva jedna jedna`   | `{5: ['jedna'], 3: ['dva', 'tri']}`    |
| `kolo auto kolo vlak auto`        | `{4: ['kolo', 'auto', 'vlak']}`        |
| (prázdný text)                    | `{}`                                   |
