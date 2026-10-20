# 01 — Katalog knih

Read-only API nad seznamem knih: výpis s filtrováním přes query parametry
a detail podle ID. Data jsou zatím v obyčejném Python seznamu, databázi
nahradí v konceptu 03.

## Část 1 — Kostra projektu

Kostru zakládáš **sám**, stejně jako v cvičení
[`01-prvni-projekt`](../../../01-projekt-a-request-cyklus/exercises/01-prvni-projekt/README.md),
tentokrát bez návodu krok za krokem. `solution/` obsahuje jen `.gitkeep`.

- uv projekt s Pythonem 3.14, `django` jako závislost, `ruff` jako dev
  závislost a konfigurace Ruffu z [`RUFF.md`](../../../docs/RUFF.md)
- Django projekt s konfigurační složkou `config` přímo v `solution/`
- appka `books`, zaregistrovaná v `INSTALLED_APPS`
- všechny URL appky `books` pod prefixem `api/books/` (přes `include()`)
- PyCharm: interpreter a Sources Root přepni na tohle cvičení, viz
  [`UV.md`](../../../docs/UV.md#nastavení-pycharmu)

## Část 2 — Data

Vytvoř `books/data.py` a vlož do něj:

```python
BOOKS = [
    {"id": 1, "title": "Krakatit", "author": "Karel Čapek", "year": 1924},
    {"id": 2, "title": "Válka s mloky", "author": "Karel Čapek", "year": 1936},
    {"id": 3, "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942},
    {"id": 4, "title": "Babička", "author": "Božena Němcová", "year": 1855},
    {"id": 5, "title": "Osudy dobrého vojáka Švejka", "author": "Jaroslav Hašek", "year": 1921},
    {"id": 6, "title": "Spalovač mrtvol", "author": "Ladislav Fuks", "year": 1967},
]
```

Seznam ve views jen čti, nic do něj nezapisuj.

## Část 3 — API

| Metoda + URL | Jméno routy | View |
|---|---|---|
| `GET /api/books/` | `books:list` | `book_list` |
| `GET /api/books/<id>/` | `books:detail` | `book_detail` |

### Požadavky

- **Detail** vrací knihu se všemi poli + pole `url`. Neexistující ID
  vrací **JSON** `{"error": "Kniha nenalezena"}` se statusem 404, ne
  Djangovu HTML stránku.
- ID v cestě je celé číslo. Převod a odmítnutí nečíselné hodnoty nech na
  routeru (path converter), ne na `int()` ve view.
- **Výpis** vrací `{"count": <počet>, "results": [<knihy>]}`. Každá kniha
  ve výpisu má stejný tvar jako detail, včetně `url`. Pořadí podle `id`.
- Pole `url` **nesmí být složené ručně** (`f"/api/books/{...}/"`). Generuj
  ho z jména routy. Ověř si to: změň dočasně prefix v `config/urls.py` na
  `api/v2/books/` a `url` se musí změnit samo.
- **Filtry** ve výpisu (query parametry, všechny volitelné, dají se
  kombinovat):
  - `author`: část jména autora, bez ohledu na velikost písmen
    (`čapek`, `ČAPEK` i `Čapek` najdou Čapka, diakritika ale musí sedět)
  - `year_from`: rok vydání **od** (včetně)
  - `year_to`: rok vydání **do** (včetně)
- Prázdný parametr (`?year_from=`) se chová, jako by chyběl. Neznámé
  parametry se ignorují.
- Nečíselný `year_from` / `year_to` vrací **400** s
  `{"error": "Parametr year_from musí být celé číslo"}` (resp. `year_to`).
  Když jsou špatně oba, stačí ohlásit `year_from`.
- Diakritika v JSONu musí být v surové odpovědi čitelná
  (`"Karel Čapek"`, ne `"Karel Čapek"`). Ověř v Postmanu v záložce
  *Raw* nebo přes `curl`. Nápověda v `THEORY.md`.
- `uv run ruff format --check .` a `uv run ruff check .` projdou.

### Příklady request → response

Všechny URL jsou relativní k `http://127.0.0.1:8000`. U výpisů je pro
přehlednost uvedeno jen `count` a ID knih v `results`.

**Detail**

| Request | Status | Body |
|---|---|---|
| `GET /api/books/3/` | 200 | `{"id": 3, "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942, "url": "/api/books/3/"}` |
| `GET /api/books/99/` | 404 | `{"error": "Kniha nenalezena"}` |
| `GET /api/books/0/` | 404 | `{"error": "Kniha nenalezena"}` (0 je platné číslo, jen taková kniha není) |
| `GET /api/books/abc/` | 404 | **HTML** stránka, routa nesedí, view se nezavolá |
| `GET /api/books/-1/` | 404 | **HTML** stránka (proč? viz `THEORY.md`) |
| `GET /api/books/3` | 301 | přesměrování na `/api/books/3/` |

**Výpis a filtry**

| Request | Status | `count` | ID v `results` |
|---|---|---|---|
| `GET /api/books/` | 200 | 6 | 1, 2, 3, 4, 5, 6 |
| `GET /api/books/?author=čapek` | 200 | 2 | 1, 2 |
| `GET /api/books/?author=ČAPEK` | 200 | 2 | 1, 2 |
| `GET /api/books/?author=capek` | 200 | 0 | — (bez diakritiky nesedí, to je v pořádku) |
| `GET /api/books/?author=xyz` | 200 | 0 | — (prázdný seznam, ne 404) |
| `GET /api/books/?year_from=1930` | 200 | 3 | 2, 3, 6 |
| `GET /api/books/?year_from=1900&year_to=1940` | 200 | 3 | 1, 2, 5 |
| `GET /api/books/?year_from=1924&year_to=1924` | 200 | 1 | 1 (hranice včetně) |
| `GET /api/books/?author=čapek&year_from=1930` | 200 | 1 | 2 |
| `GET /api/books/?year_from=2000&year_to=1900` | 200 | 0 | — |
| `GET /api/books/?year_from=` | 200 | 6 | 1–6 (prázdný parametr = bez filtru) |
| `GET /api/books/?foo=bar` | 200 | 6 | 1–6 (neznámý parametr se ignoruje) |
| `GET /api/books/?year_from=abc` | 400 | — | `{"error": "Parametr year_from musí být celé číslo"}` |
| `GET /api/books/?year_to=1.5` | 400 | — | `{"error": "Parametr year_to musí být celé číslo"}` |

Tvar odpovědi výpisu (zkráceně):

```json
{
  "count": 2,
  "results": [
    {"id": 1, "title": "Krakatit", "author": "Karel Čapek", "year": 1924, "url": "/api/books/1/"},
    {"id": 2, "title": "Válka s mloky", "author": "Karel Čapek", "year": 1936, "url": "/api/books/2/"}
  ]
}
```

### Otázky k zamyšlení

1. Proč `GET /api/books/abc/` vrací HTML a `GET /api/books/99/` JSON, když
   jsou obě 404? Kdo každou z nich vrací?
2. Co by se stalo, kdybys v routě napsal `<book_id>` místo
   `<int:book_id>`? Jak by se změnilo porovnání ID ve view?
3. Proč `?author=xyz` vrací 200 s prázdným seznamem, a ne 404?
4. Kde všude by se musel kód změnit, kdyby se prefix změnil na
   `api/v2/books/` a `url` bys skládal ručně?

## Bonus

Podle konvence tématu jde bonus do appky `bonus` ve stejném projektu
pod prefixem `bonus/`. Data a pomocné funkce smí importovat z appky
`books`.

**Stránkování:** `GET /bonus/books/` vrací knihy po stránkách, podobně
jako to dělá DRF (koncept 15).

- Query parametry `page` (výchozí 1) a `page_size` (výchozí 2, povoleno
  1 až 5).
- Odpověď obsahuje `count` (počet všech knih), `page`, `num_pages`,
  `next` a `previous` (URL sousední stránky, nebo `null`) a `results`.
- `next` / `previous` generuj z jména routy (`bonus:books`) a query string
  sestav přes standardní knihovnu, ne ručním lepením řetězců.
- Nečíselný `page` / `page_size` → 400
  `{"error": "page a page_size musí být celá čísla"}`.
- `page_size` mimo 1–5 → 400 `{"error": "page_size musí být 1 až 5"}`.
- Stránka mimo rozsah → 404 `{"error": "Stránka neexistuje"}`.

| Request | Status | `page` / `num_pages` | `next` | `previous` | ID v `results` |
|---|---|---|---|---|---|
| `GET /bonus/books/` | 200 | 1 / 3 | `/bonus/books/?page=2&page_size=2` | `null` | 1, 2 |
| `GET /bonus/books/?page=2` | 200 | 2 / 3 | `/bonus/books/?page=3&page_size=2` | `/bonus/books/?page=1&page_size=2` | 3, 4 |
| `GET /bonus/books/?page=3&page_size=2` | 200 | 3 / 3 | `null` | `/bonus/books/?page=2&page_size=2` | 5, 6 |
| `GET /bonus/books/?page=2&page_size=4` | 200 | 2 / 2 | `null` | `/bonus/books/?page=1&page_size=4` | 5, 6 |
| `GET /bonus/books/?page_size=5` | 200 | 1 / 2 | `/bonus/books/?page=2&page_size=5` | `null` | 1–5 |
| `GET /bonus/books/?page=4` | 404 | — | — | — | `{"error": "Stránka neexistuje"}` |
| `GET /bonus/books/?page=0` | 404 | — | — | — | `{"error": "Stránka neexistuje"}` |
| `GET /bonus/books/?page=x` | 400 | — | — | — | `{"error": "page a page_size musí být celá čísla"}` |
| `GET /bonus/books/?page_size=10` | 400 | — | — | — | `{"error": "page_size musí být 1 až 5"}` |
| `GET /bonus/books/?page_size=0` | 400 | — | — | — | `{"error": "page_size musí být 1 až 5"}` |
