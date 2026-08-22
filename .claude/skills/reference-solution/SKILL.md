---
name: reference-solution
description: Use this immediately — without being asked — every time you tell the user their own exercises/NN-*/solution/ code in this learning-lab (programming-school) repo is functionally correct. It creates the reference/ solution alongside solution/ so the user can compare. Trigger on any confirmation of correctness ("je to v pořádku", "sedí to", "logika je správná", "hotovo", etc.) for a solution/main.py or solution/bonus.py review — do not wait for the user to ask "ukaž mi tvé řešení" again; that should never be necessary.
---

# Reference solution

Po každém potvrzení, že uživatelovo řešení cvičení je funkčně správné,
založ (nebo aktualizuj, pokud se zadání/přístup od poslední verze změnil)
`reference/main.py` — a `reference/bonus.py`, pokud `README.md` cvičení má
sekci `## Bonus` — se svým vlastním idiomatickým řešením stejného zadání.

Tohle není otázka na uživatele. Založ soubor(y) ve stejné odpovědi, kde
potvrzuješ správnost, bez čekání na výslovné "ukaž mi své řešení".

## Kdy NE

- Nikdy nezakládej `reference/` u cvičení, které uživatel ještě nevyřešil
  nebo jehož řešení jsi právě odmítl jako chybné — to by byl spoiler.
  `reference/` patří výhradně k už schválenému řešení.

## Jak psát reference řešení

- Idiomatický, čistý Python — jak bys to napsal ty, ne kopie uživatelova
  přístupu.
- Drž se nástrojů, které daný koncept už zavedl (viz `THEORY.md` toho
  konceptu). Nepředbíhej — např. v `02-podminky-cykly` nepoužívej `list`,
  `dict`, funkce (`def`) ani built-in funkce jako `max()`/`sorted()`,
  pokud ten koncept ještě nebyl na řadě (viz `python/ROADMAP.md`).
- Pokud zadání popisuje konkrétní techniku (např. "použij `while` a dva
  indexy"), reference řešení tuhle techniku respektuje.
- Žádné komentáře navíc, žádné zbytečné abstrakce — jen krátký, čitelný
  skript odpovídající rozsahu cvičení.

## Struktura

```
NN-nazev-ukolu/
├── solution/
│   ├── main.py
│   └── bonus.py      # jen pokud existuje bonus
└── reference/
    ├── main.py        # Claudovo řešení základu
    └── bonus.py        # jen pokud existuje bonus
```

Viz i kořenový [`CLAUDE.md`](../../../CLAUDE.md) — tahle konvence je tam
zapsaná jako trvalé pravidlo, tento skill jen zajišťuje, že se skutečně
pokaždé provede.
