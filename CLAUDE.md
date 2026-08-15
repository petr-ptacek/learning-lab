# learning-lab

Osobní repo na učení programovacích jazyků a frameworků napříč jedním místem
(místo samostatného repa pro každou technologii). Hlavní cíl: **praxe** —
skutečné příklady k řešení, ne jen teorie.

## Struktura repa

```
<téma>/                 # např. vue, react, python, django
├── CLAUDE.md           # specifika daného tématu (verze, styl, konvence)
├── theory/
│   └── 01-nazev-konceptu.md   # jeden koncept = jeden soubor
├── resources/
│   └── 01-nazev-konceptu.md   # odkazy k danému konceptu (viz theory/)
└── exercises/
    └── 01-nazev-ukolu/
        ├── README.md   # zadání úkolu
        └── solution/   # řešení (kód)

projects/               # větší cvičné projekty, klidně napříč tématy
_template/               # šablona pro založení nového tématu
```

Nové téma = zkopírovat `_template/` a přejmenovat.

## Jak mi pomáhat (pokyny pro Claude)

- Když mě žádáš o cvičení k tématu, **generuj reálné praktické zadání**
  (ne jen popis teorie) a založ ho do `exercises/NN-nazev/README.md` podle
  vzoru výše. Obtížnost cvičení v rámci tématu ať postupně roste.
- Zadání a řešení drž oddělené — řešení až do `solution/`, ať si úkol
  můžu nejdřív zkusit sám.
- Do `theory/` a `resources/` piš stručně a věcně, jeden koncept = jeden
  soubor, s odkazy na oficiální dokumentaci (preferuj oficiální docs před
  blogy).
- Nepřidávej abstrakce/tooling navíc (CI, linters, package manager configy),
  pokud o to výslovně nepožádám — je to učební repo, ne produkční projekt.
- Odpovídej a piš obsah česky, kód a technické termíny normálně anglicky.
- Commit zprávy piš podle [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md).
