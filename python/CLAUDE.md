# python

Specifika tohoto tématu — doplnit při založení:

- verze jazyka/frameworku, se kterou pracujeme
- preferovaný styl/konvence (pokud je jiný než obecný default)
- odkaz zpět na kořenový [`CLAUDE.md`](../CLAUDE.md) pro obecná pravidla repa

## Docs

Průřezová vysvětlení jsou v `docs/` — v `THEORY.md` na ně odkazuj místo
opakování.

Ke každému novému konceptu kromě `THEORY.md` napiš i **podrobný výtah
z toho, na co odkazuje `RESOURCES.md`** (hlavně články Real Python,
které jsou na čtení dlouhé, a oficiální docs, ve kterých se špatně
hledá): samostatné soubory v `docs/`, prolinkované navzájem
a odkázané z `THEORY.md`, `RESOURCES.md` i odsud. Prakticky, česky,
s ověřenými ukázkami (každou spustit). `THEORY.md` zůstává přehled
konceptu, hloubka patří do `docs/`.

Seznam:

- formátovací mini-jazyk (šířka, zarovnání, fill, oddělovače, přesnost,
  typy) v [`STRING_FORMATTING.md`](docs/STRING_FORMATTING.md)
- `*args` / `**kwargs`, rozbalování při volání, v literálech a při
  přiřazení (obdoba JS rest/spread) v
  [`ARGS_KWARGS_AND_UNPACKING.md`](docs/ARGS_KWARGS_AND_UNPACKING.md)
- velikost písmen (`lower` / `upper` / `casefold` / `title` …),
  porovnávání bez ohledu na velikost písmen a diakritiku v
  [`STRING_CASE_AND_COMPARISON.md`](docs/STRING_CASE_AND_COMPARISON.md)
- generátory a iterátory do hloubky (protokol, pasti, vzory z praxe,
  výkon) v [`GENERATORS_AND_ITERATORS.md`](docs/GENERATORS_AND_ITERATORS.md)
- modul `itertools` s příklady v [`ITERTOOLS.md`](docs/ITERTOOLS.md)
- typové anotace (`Iterable` vs. `list`, `Callable`, generika `[T]`,
  `Iterator` / `Generator`, `TypedDict`, srovnání s TS) v
  [`TYPE_HINTS.md`](docs/TYPE_HINTS.md)
- walrus operátor `:=` (přiřazení ve výrazu, kdy ano / ne, pasti
  s prioritou) v [`WALRUS_OPERATOR.md`](docs/WALRUS_OPERATOR.md)
- modul `json` (`dumps` / `loads` / `dump` / `load`, převod typů,
  `ensure_ascii`, `default`, `JSONDecodeError`) v
  [`JSON.md`](docs/JSON.md)
