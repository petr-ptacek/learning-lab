# 01 — Katalog v databázi

Katalog knih z konceptu 02, tentokrát nad databází. Navrhneš model,
vytvoříš migrace, nahraješ data z fixture, vyzkoušíš si CRUD v shellu
a read-only API přepíšeš na ORM. Nakonec model změníš a uvidíš, jak
migrace přenesou změnu i na existující data.

Teorie: [`../../THEORY.md`](../../THEORY.md). Prakticky:
[`MODELS_AND_FIELDS.md`](../../../docs/MODELS_AND_FIELDS.md),
[`MIGRATIONS.md`](../../../docs/MIGRATIONS.md),
[`ORM_BASICS.md`](../../../docs/ORM_BASICS.md),
[`DATABASE.md`](../../../docs/DATABASE.md).

## Část 1 — Kostra projektu

Nový projekt v `solution/` (obsahuje jen `.gitkeep`), stejné požadavky
jako dřív:

- uv projekt s Pythonem 3.14, `django`, `ruff` jako dev závislost
  a konfigurace Ruffu z [`RUFF.md`](../../../docs/RUFF.md)
- konfigurační složka `config`, appka `books` **v `INSTALLED_APPS`**
  (teď už to bez ní nepůjde, proč viz `THEORY.md`, sekce 2)
- URL appky `books` pod prefixem `api/books/`
- PyCharm: interpreter (typ uv) a Sources Root na tohle cvičení

## Část 2 — Model, migrace, data

V `books/models.py` vytvoř model `Book`:

| Pole | Typ a pravidla |
|---|---|
| `title` | text, max. 200 znaků, povinný |
| `author` | text, max. 100 znaků, povinný |
| `year` | kladné celé číslo (rok), povinný |
| `available` | ano/ne, výchozí `True` |
| `created_at` | datum a čas vytvoření, nastaví se samo |

- `id` nepiš, přidá ho Django.
- `str(book)` vrací `"Krakatit (1924)"`.
- Vytvoř migraci, prohlédni si ji a podívej se i na SQL, které spustí
  (`sqlmigrate`). Pak ji aplikuj.

**Data:** zkopíruj [`fixtures/books.json`](fixtures/books.json) do
`solution/books/fixtures/books.json` a nahraj ho přes `loaddata`.
Ověř v shellu, že `Book.objects.count()` vrátí `6`.

Fixture obsahuje i `created_at`. Proč, když se pole „nastaví samo“? Viz
[`DATABASE.md`](../../../docs/DATABASE.md#testovací-data-fixtures).

**Podívej se do DB:** otevři `db.sqlite3` v PyCharm *Database* panelu
(postup v [`DATABASE.md`](../../../docs/DATABASE.md#jak-se-do-databáze-podívat)).
Najdi tabulku `books_book` a `django_migrations`. Co je v té druhé?

## Část 3 — CRUD v shellu

Napiš skript `solution/shell_tasks.py` a spusť ho takhle:

```bash
uv run manage.py shell < shell_tasks.py
```

Shell model importuje sám, `from books.models import Book` psát nemusíš
(ale můžeš). Skript spouštěj **na čerstvě nahraná data** (viz konec
části). Každý krok vypíše řádek s číslem kroku a výsledkem. Výstup musí
být přesně tenhle:

| # | Úkol | Výstup |
|---|---|---|
| 1 | počet knih | `1 6` |
| 2 | kniha s `pk` 3 | `2 Saturnin (1942)` |
| 3 | názvy knih Karla Čapka seřazené podle roku, jako seznam stringů | `3 ['Krakatit', 'Válka s mloky']` |
| 4 | knihy vydané před rokem 1930, seřazené podle roku | `4 <QuerySet [<Book: Babička (1855)>, <Book: Osudy dobrého vojáka Švejka (1921)>, <Book: Krakatit (1924)>]>` |
| 5 | existuje kniha, jejíž autor obsahuje „hrabal“? | `5 False` |
| 6 | vytvoř knihu *R.U.R.*, Karel Čapek, 1920. Vypiš její `pk` a `available` | `6 7 True` |
| 7 | změň jí rok na 1921 tak, aby se uložil **jen** sloupec `year`. Ověř **novým načtením z DB** | `7 1921` |
| 8 | **jedním dotazem** nastav `available=False` všem knihám Karla Čapka, vypiš počet změněných | `8 3` |
| 9 | počet dostupných knih | `9 4` |
| 10 | vypiš `available` objektu R.U.R. z kroku 6, pak ho obnov z DB a vypiš znovu | `10 True False` |
| 11 | zkus načíst přes `get()` „knihu Karla Čapka“, chyť výjimku a vypiš název její třídy | `11 MultipleObjectsReturned` |
| 12 | smaž R.U.R., vypiš návratovou hodnotu | `12 (1, {'books.Book': 1})` |
| 13 | vytvoř (neukládej!) knihu s prázdným názvem, autorem Jan Neruda, rokem 1878, zvaliduj ji a vypiš chyby | `13 {'title': ['This field cannot be blank.']}` |

Návrat do výchozího stavu (smaže data a nahraje je znovu):

```bash
uv run manage.py flush --noinput && uv run manage.py loaddata books
```

Otázky ke kroku 10 a 13 jsou dole v *Otázkách k zamyšlení*.

## Část 4 — API nad databází

Přepiš API z konceptu 02 tak, aby četlo z databáze. Jen čtení, žádný
`POST` ani `DELETE` (přijdou v dalším cvičení).

| Metoda + URL | Jméno routy | View |
|---|---|---|
| `GET /api/books/` | `books:list` | `book_list` |
| `GET /api/books/<id>/` | `books:detail` | `book_detail` |

**Požadavky:**

- Tvar knihy v odpovědi:
  `{"id", "title", "author", "year", "available", "url"}`. `url` přes
  `reverse()`. `created_at` do odpovědi nedávej.
- Výpis `{"count": …, "results": […]}`, **seřazený podle `id`**.
- Filtry `author`, `year_from`, `year_to` jako v 02, ale **filtruje
  databáze** (`filter()` s lookupy), ne Python. Ověř si to: `print(qs.query)`
  musí obsahovat `WHERE`.
  - `author` hledá část jména bez ohledu na velikost písmen. Pozor na
    diakritiku v SQLite, viz
    [`ORM_BASICS.md`](../../../docs/ORM_BASICS.md#lookupy-podmínky-v-filter),
    a tabulku níže.
  - Nečíselný `year_from` / `year_to` → 400
    `{"error": "Parametr year_from musí být celé číslo"}`.
  - Prázdný parametr = bez filtru, neznámé parametry se ignorují.
- Detail neexistující knihy → 404 `{"error": "Kniha nenalezena"}` (JSON).
- Diakritika v JSONu čitelná.
- Ruff projde.

Příklady pro výchozí data (6 knih). Aktuální stav po změnách v části 5
je v tabulce tam.

| Request | Status | `count` | ID |
|---|---|---|---|
| `GET /api/books/` | 200 | 6 | 1–6 |
| `GET /api/books/?author=Čapek` | 200 | 2 | 1, 2 |
| `GET /api/books/?author=karel` | 200 | 2 | 1, 2 |
| `GET /api/books/?author=ČAPEK` | 200 | 2 | 1, 2 |
| `GET /api/books/?author=čapek` | 200 | 0 | — (SQLite: `č` ≠ `Č`, v PostgreSQL by našel 2) |
| `GET /api/books/?year_from=1930` | 200 | 3 | 2, 3, 6 |
| `GET /api/books/?year_from=1900&year_to=1940` | 200 | 3 | 1, 2, 5 |
| `GET /api/books/?year_from=abc` | 400 | — | `{"error": "Parametr year_from musí být celé číslo"}` |
| `GET /api/books/3/` | 200 | — | `{"id": 3, "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942, "available": true, "url": "/api/books/3/"}` |
| `GET /api/books/99/` | 404 | — | `{"error": "Kniha nenalezena"}` |

## Část 5 — Změna modelu

Přidej do modelu dvě pole:

| Pole | Typ a pravidla |
|---|---|
| `genre` | výčet `novel` / `drama` / `poetry` s popisky Román / Drama / Poezie, výchozí `novel` |
| `pages` | kladné celé číslo, **nepovinné** (u některých knih počet stran neznáme) |

- Vytvoř a aplikuj migraci **na DB, ve které už jsou data**. Zeptal se
  `makemigrations` na něco? Proč ne? (Otázky dole.)
- Nahraj [`fixtures/books_v2.json`](fixtures/books_v2.json) (zkopíruj
  vedle první fixture): doplní žánry a stránky ke stávajícím knihám
  a přidá dvě nové (*R.U.R.*, *Kytice*).
- Rozšiř tvar knihy v API o `genre`, `genre_label` (popisek, např.
  `"Drama"`) a `pages`.
- Nový filtr `genre`: přesná hodnota (`novel`, `drama`, `poetry`).
  Neznámá hodnota → 400 `{"error": "Neznámý žánr"}`. Povolené hodnoty
  ber z modelu, nepiš je ve view znovu.

Příklady po nahrání `books_v2` (8 knih):

| Request | Status | `count` | ID |
|---|---|---|---|
| `GET /api/books/` | 200 | 8 | 1–8 |
| `GET /api/books/?author=Čapek` | 200 | 3 | 1, 2, 7 |
| `GET /api/books/?author=karel` | 200 | 4 | 1, 2, 7, 8 (i Karel Jaromír Erben) |
| `GET /api/books/?year_to=1900` | 200 | 2 | 4, 8 |
| `GET /api/books/?year_from=1900&year_to=1940` | 200 | 4 | 1, 2, 5, 7 |
| `GET /api/books/?genre=drama` | 200 | 1 | 7 |
| `GET /api/books/?genre=poetry` | 200 | 1 | 8 |
| `GET /api/books/?genre=novel` | 200 | 6 | 1–6 |
| `GET /api/books/?author=Čapek&genre=novel` | 200 | 2 | 1, 2 |
| `GET /api/books/?genre=` | 200 | 8 | 1–8 (prázdný = bez filtru) |
| `GET /api/books/?genre=xyz` | 400 | — | `{"error": "Neznámý žánr"}` |
| `GET /api/books/?genre=DRAMA` | 400 | — | `{"error": "Neznámý žánr"}` (hodnota je `drama`) |

Detaily:

```json
GET /api/books/7/
{"id": 7, "title": "R.U.R.", "author": "Karel Čapek", "year": 1920, "genre": "drama", "genre_label": "Drama", "pages": 100, "available": true, "url": "/api/books/7/"}

GET /api/books/8/
{"id": 8, "title": "Kytice", "author": "Karel Jaromír Erben", "year": 1853, "genre": "poetry", "genre_label": "Poezie", "pages": null, "available": true, "url": "/api/books/8/"}
```

Po části 5 krok 1 až 13 v `shell_tasks.py` pořád funguje s `books.json`
(stará fixture nová pole nemá, dostanou výchozí hodnoty).

## Část 6 (volitelná) — Admin

Vyzkoušej si admin, pořádně ho probereme v konceptu 06:

1. Zaregistruj `Book` v `books/admin.py`.
2. Vytvoř si uživatele: `uv run manage.py createsuperuser`.
3. Přihlas se na `http://127.0.0.1:8000/admin/` a prohlédni si knihy.
4. Zkus přidat knihu s prázdným názvem, žánrem a rokem `-5`. Co admin
   udělá? A co by udělal `Book.objects.create(...)` se stejnými daty?
5. Uprav v adminu knihu a ověř změnu přes `GET /api/books/<id>/`.

Kdo je v adminu přihlášený, se ukládá do tabulky `auth_user`, kterou
vytvořila první `migrate`. Najdi ho v PyCharm Database panelu.

## Otázky k zamyšlení

1. Proč `makemigrations` při přidání `genre` a `pages` nic nechtěl, i když
   v tabulce už byla data? Co by se stalo, kdyby `genre` neměl `default`?
2. Krok 10: proč objekt `rur` vypíše `True`, i když v DB už je `False`?
   Kdy na tohle v reálném kódu narazíš?
3. Krok 13: co by se stalo, kdybys místo `full_clean()` zavolal `save()`?
   Kterou vrstvu validace z `THEORY.md`, sekce 5, tím obejdeš?
4. Proč se `pages` dělá jako `null=True`, ale nepovinný text by se dělal
   jako `blank=True` bez `null`?
5. Kolik SQL dotazů pošle `GET /api/books/?author=Čapek&genre=novel`?
   A kolik by jich bylo, kdybys filtroval v Pythonu přes list
   comprehension nad `Book.objects.all()`? Co je pro tisíc knih lepší?
6. `?author=čapek` v SQLite nic nenajde. Jak bys to řešil, kdyby to bylo
   v produkci důležité? (Stačí nápad, ne implementace.)

## Bonus

**Slug a datová migrace.** Knihy chceme v URL i podle názvu:
`/bonus/books/valka-s-mloky/`.

- Přidej do modelu pole `slug`: max. 220 znaků, **povinné a unikátní**.
- Existující knihy musí slug dostat **migrací** z názvu přes
  `django.utils.text.slugify` (`"Válka s mloky"` → `"valka-s-mloky"`).
  Ruční vyplnění v shellu nebo adminu se nepočítá. Musí to fungovat na
  databázi kolegy, který jen udělá `git pull` a `migrate`.
  Nápověda: povinné unikátní pole nejde přidat k existujícím řádkům jedním
  krokem. [`MIGRATIONS.md`](../../../docs/MIGRATIONS.md#datová-migrace-runpython).
- Appka `bonus` pod prefixem `bonus/`, routa `bonus:detail`
  `GET /bonus/books/<slug>/` vrací stejný tvar knihy jako `/api/books/<id>/`
  (`url` vede na detail podle ID). Použij path converter `slug`.
- Po migraci stará fixture nepůjde nahrát do čisté DB. Ověř si to
  (smaž `db.sqlite3`, `migrate`, `loaddata books_v2`) a vytvoř
  `books_v3.json` přes `dumpdata`, která už slugy obsahuje.

| Request | Status | Odpověď |
|---|---|---|
| `GET /bonus/books/valka-s-mloky/` | 200 | kniha 2 |
| `GET /bonus/books/osudy-dobreho-vojaka-svejka/` | 200 | kniha 5 |
| `GET /bonus/books/rur/` | 200 | kniha 7 (`slugify` tečky zahodí) |
| `GET /bonus/books/babicka/` | 200 | kniha 4 |
| `GET /bonus/books/Valka-s-mloky/` | 404 | `{"error": "Kniha nenalezena"}` (converter projde, slug v DB nesedí) |
| `GET /bonus/books/válka/` | 404 | HTML, converter `slug` nepovolí `á` |
| `GET /bonus/books/neexistuje/` | 404 | `{"error": "Kniha nenalezena"}` |
