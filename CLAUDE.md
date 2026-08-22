# learning-lab

Osobní repo na učení programovacích jazyků a frameworků napříč jedním místem
(místo samostatného repa pro každou technologii). Hlavní cíl: **praxe** —
skutečné příklady k řešení, ne jen teorie.

## Struktura repa

```
<téma>/                        # např. vue, react, python, django
├── CLAUDE.md                  # specifika daného tématu (verze, styl, konvence)
├── ROADMAP.md                 # plánované koncepty v pořadí + stav (zvládnuto/ne)
└── NN-nazev-konceptu/         # jeden koncept = jedna složka
    ├── THEORY.md              # stručné shrnutí konceptu
    ├── RESOURCES.md           # odkazy k danému konceptu
    └── exercises/
        └── NN-nazev-ukolu/
            ├── README.md      # zadání úkolu
            ├── solution/
            │   ├── main.py    # prázdný stub, sem se píše řešení
            │   └── bonus.py   # prázdný stub, jen pokud má cvičení bonus
            └── reference/     # jen u už vyřešených cvičení, viz níže
                ├── main.py    # moje (Claude) referenční řešení
                └── bonus.py   # jen pokud má cvičení bonus

projects/               # větší cvičné projekty, klidně napříč tématy
_template/               # šablona pro založení nového tématu / konceptu
```

Nové téma = zkopírovat `_template/CLAUDE.md`. Nový koncept v rámci tématu =
zkopírovat `_template/NN-nazev-konceptu/` a přejmenovat.

## Jak mi pomáhat (pokyny pro Claude)

- **Praxe má vždy přednost před teorií.** Cílem je jazyk/framework zvládnout
  důkladně, ale cestou přes řešení reálných problémů a programování — ne
  čtením. `THEORY.md` drž na nutném minimu (stručné shrnutí + odkazy do
  `RESOURCES.md`), těžiště je v `exercises/`. Ke každému konceptu radši
  víc menších praktických úloh než dlouhý teoretický text.
- Když mě žádáš o cvičení ke konceptu, **generuj reálné praktické zadání**
  (ne jen popis teorie) a založ ho do `exercises/NN-nazev/README.md` podle
  vzoru výše. Obtížnost cvičení v rámci konceptu ať postupně roste.
- Do zadání (`README.md`) vždy přidej **víc příkladů vstup/výstup** (ne jen
  jeden), ať mám k dispozici širší množinu reálných případů včetně
  okrajových (např. nula, záporné číslo, hraniční hodnota).
- Zadání a řešení drž oddělené — řešení až do `solution/`, ať si úkol
  můžu nejdřív zkusit sám. Ke každému cvičení rovnou založ prázdný
  `solution/main.py` stub, ať ho nemusím zakládat ručně. Pokud zadání má
  sekci `## Bonus`, založ rovnou i prázdný `solution/bonus.py` stub.
- Do `THEORY.md` a `RESOURCES.md` piš stručně a věcně (jsou to poznámky ke
  konkrétnímu konceptu, ne kniha), s odkazy na oficiální dokumentaci
  (preferuj oficiální docs před blogy).
- Každý `THEORY.md` musí začínat sekcí **Cíl** — co se v konceptu naučíš
  a k čemu / na čem to stavíš (viz `_template/NN-nazev-konceptu/THEORY.md`).
- Nepřidávej abstrakce/tooling navíc (CI, linters, package manager configy),
  pokud o to výslovně nepožádám — je to učební repo, ne produkční projekt.
- Odpovídej a piš obsah česky, kód a technické termíny normálně anglicky.
- Commit zprávy piš podle [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md).
- **Při kontrole vlastního řešení cvičení nikdy neprozrazuj chybu ani opravu
  přímo.** Naváděj otázkami a nápovědami (co zkontrolovat, co si vypsat,
  co se stane pro konkrétní vstup), dokud na řešení nepřijdu sám. Přímou
  odpověď řekni jen když o ni výslovně požádám.
- Jakmile je moje vlastní řešení cvičení hotové (zkontrolované a
  odsouhlasené jako funkčně správné), **automaticky** (bez ptaní) založ
  vedle `solution/` složku `reference/main.py` s tvým vlastním řešením
  stejného zadání — idiomatický kód, jak bys to napsal ty, jen pro srovnání.
  `reference/` nikdy nezakládej dřív (u nevyřešeného cvičení), ať si úkol
  nejdřív vyřeším sám beze spoileru.
- Bonus patří vždy do sesterského souboru `bonus.py` vedle `main.py`
  (`solution/bonus.py`, a po dořešení i `reference/bonus.py`) — ne do
  jednoho `main.py` s base řešením a ne do nové složky. Složku navíc zaveď
  jen tehdy, když si to daný koncept opravdu vyžádá (typicky až
  `09-moduly-balicky`, kde se řeší `import` mezi vlastními moduly) — do
  té doby nepřipravuj strukturu na hypotetické budoucí případy.
