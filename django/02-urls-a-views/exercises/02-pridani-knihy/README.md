# 02 — Přidání a smazání knihy

Katalog knih z cvičení `01` se rozšíří o zápis: `POST` vytvoří knihu
z JSON body, `DELETE` ji smaže. Hlavní práce je ve **validaci vstupu**:
klient může poslat cokoliv a API na to musí odpovědět rozumným statusem
a hláškou, nikdy ne 500.

Data jsou pořád v Python seznamu v paměti. Každý restart serveru (i
automatický po uložení souboru) je vrátí do výchozího stavu. Pro tohle
cvičení je to výhoda, databáze přijde v konceptu 03.

Teorie: `THEORY.md`, sekce 5, podsekce *Metoda a JSON body*.

## Část 1 — Kostra projektu

Nový samostatný projekt v `solution/` (obsahuje jen `.gitkeep`), stejné
požadavky jako v cvičení
[`01-katalog-knih`](../01-katalog-knih/README.md):

- uv projekt s Pythonem 3.14, `django`, `ruff` jako dev závislost
  a konfigurace Ruffu z [`RUFF.md`](../../../docs/RUFF.md)
- konfigurační složka `config`, appka `books` v `INSTALLED_APPS`
- URL appky `books` pod prefixem `api/books/`
- PyCharm: interpreter (typ uv) a Sources Root přepni na tohle cvičení

## Část 2 — Data

`books/data.py`, stejná data jako v `01`:

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

Tentokrát do seznamu **zapisuješ** (přidáváš a mažeš).

## Část 3 — API

| Metoda + URL | Jméno routy | View | Status úspěchu |
|---|---|---|---|
| `GET /api/books/` | `books:list` | `book_list` | 200 |
| `POST /api/books/` | `books:list` | `book_list` | 201 |
| `GET /api/books/<id>/` | `books:detail` | `book_detail` | 200 |
| `DELETE /api/books/<id>/` | `books:detail` | `book_detail` | 204 |

Dvě routy, dvě view. Metody se rozlišují **uvnitř view**, ne v `urls.py`.

### Požadavky

**Čtení (převezmi z `01`, klidně zkopíruj):**

- Výpis `{"count": …, "results": […]}` a detail se stejným tvarem knihy
  včetně `url` generovaného přes `reverse()`. Filtry z `01` tu **nejsou
  potřeba**.
- Neexistující ID → 404 `{"error": "Kniha nenalezena"}`.
- Diakritika v JSONu čitelná.

**Metody a CSRF:**

- Výpis přijímá jen `GET` a `POST`, detail jen `GET` a `DELETE`. Jiná
  metoda → **405** s hlavičkou `Allow` (body může být prázdné). Nepiš to
  ručně přes `if`, použij dekorátor.
- Obě view mají `@csrf_exempt`, jinak by `POST` a `DELETE` z Postmanu
  skončily 403. Nad view dej krátký komentář, proč tam je a že
  v aplikaci s přihlášením by tam být neměl.

**Vytvoření (`POST /api/books/`):**

- Body je JSON objekt s poli `title`, `author`, `year`.
- Body, které není validní JSON (včetně prázdného) → **400**
  `{"error": "Tělo requestu není platný JSON"}`.
- Validní JSON, který není objekt (`[]`, `"text"`, `42`) → **400**
  `{"error": "Tělo requestu musí být JSON objekt"}`.
- Validace polí. Chyby se **sbírají ze všech polí najednou** a vrací se
  **400** `{"errors": {"<pole>": "<hláška>", …}}`, v odpovědi jsou jen
  pole s chybou:

  | Pole | Pravidlo | Hláška |
  |---|---|---|
  | každé | chybí v body | `Povinné pole` |
  | `title`, `author` | musí být string, po oříznutí mezer neprázdný | `Musí být neprázdný text` |
  | `year` | musí být celé číslo (ne string, ne desetinné, ne `true`/`false`) | `Musí být celé číslo` |
  | `year` | nesmí být větší než aktuální rok | `Rok nesmí být v budoucnosti` |

- `title` a `author` se ukládají **oříznuté** o mezery na krajích.
- Neznámá pole se ignorují. `id` ani `url` z body se **nepoužijí**,
  `id` přiděluje server: o 1 vyšší než **nejvyšší** existující ID
  (prázdný seznam → 1).
- Úspěch → **201**, v body nová kniha ve stejném tvaru jako detail
  a hlavička `Location` s URL detailu nové knihy. Obojí přes `reverse()`.

**Smazání (`DELETE /api/books/<id>/`):**

- Úspěch → **204** s prázdným body. Kniha zmizí z výpisu i detailu.
- Neexistující ID → 404 `{"error": "Kniha nenalezena"}`.

**Obecně:**

- Žádný vstup nesmí skončit 500.
- `uv run ruff format --check .` a `uv run ruff check .` projdou.

### Postman

U `POST` nastav v záložce *Body* volbu **raw** a typ **JSON**. Postman
pak sám přidá hlavičku `Content-Type: application/json`. Hlavičky
odpovědi (`Location`, `Allow`) najdeš v záložce *Headers* odpovědi.

Pro rychlou kontrolu z terminálu:

```bash
curl -i -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "R.U.R.", "author": "Karel Čapek", "year": 1920}'
```

### Příklady request → response

URL jsou relativní k `http://127.0.0.1:8000`. **Každý řádek předpokládá
čerstvě spuštěný server** (6 výchozích knih), pokud není řečeno jinak.

**Vytvoření, úspěch**

| Body | Status | Odpověď |
|---|---|---|
| `{"title": "R.U.R.", "author": "Karel Čapek", "year": 1920}` | 201 | `{"id": 7, "title": "R.U.R.", "author": "Karel Čapek", "year": 1920, "url": "/api/books/7/"}`, hlavička `Location: /api/books/7/` |
| `{"title": "  Bílá nemoc ", "author": " Karel Čapek", "year": 1937}` | 201 | `"title": "Bílá nemoc"`, `"author": "Karel Čapek"` (oříznuté) |
| `{"title": "Hordubal", "author": "Karel Čapek", "year": 1933, "id": 99, "isbn": "123"}` | 201 | `"id": 7`, `isbn` v odpovědi není |
| `{"title": "Rok nula", "author": "Někdo", "year": 0}` | 201 | `0` je platné celé číslo a není v budoucnosti |

Po prvním `POST` vrátí `GET /api/books/` `count: 7`
a `GET /api/books/7/` novou knihu.

**Vytvoření, chyby celého body**

| Body | Status | Odpověď |
|---|---|---|
| *(prázdné)* | 400 | `{"error": "Tělo requestu není platný JSON"}` |
| `{"title": "R.U.R.",}` | 400 | `{"error": "Tělo requestu není platný JSON"}` (čárka navíc) |
| `[1, 2]` | 400 | `{"error": "Tělo requestu musí být JSON objekt"}` |
| `"R.U.R."` | 400 | `{"error": "Tělo requestu musí být JSON objekt"}` |

**Vytvoření, chyby polí**

| Body | Status | `errors` |
|---|---|---|
| `{}` | 400 | `{"title": "Povinné pole", "author": "Povinné pole", "year": "Povinné pole"}` |
| `{"title": "R.U.R.", "author": "Karel Čapek"}` | 400 | `{"year": "Povinné pole"}` |
| `{"title": "   ", "author": "Karel Čapek", "year": 1920}` | 400 | `{"title": "Musí být neprázdný text"}` |
| `{"title": 123, "author": null, "year": 1920}` | 400 | `{"title": "Musí být neprázdný text", "author": "Musí být neprázdný text"}` |
| `{"title": "R.U.R.", "author": "Karel Čapek", "year": "1920"}` | 400 | `{"year": "Musí být celé číslo"}` |
| `{"title": "R.U.R.", "author": "Karel Čapek", "year": 1920.5}` | 400 | `{"year": "Musí být celé číslo"}` |
| `{"title": "R.U.R.", "author": "Karel Čapek", "year": true}` | 400 | `{"year": "Musí být celé číslo"}` |
| `{"title": "R.U.R.", "author": "Karel Čapek", "year": 2999}` | 400 | `{"year": "Rok nesmí být v budoucnosti"}` |
| `{"title": "", "author": "Karel Čapek", "year": "abc"}` | 400 | `{"title": "Musí být neprázdný text", "year": "Musí být celé číslo"}` |

Po chybném `POST` se výpis nesmí změnit, pořád `count: 6`.

**Smazání**

| Request | Status | Body |
|---|---|---|
| `DELETE /api/books/3/` | 204 | *(prázdné)* |
| `DELETE /api/books/3/` podruhé | 404 | `{"error": "Kniha nenalezena"}` |
| `GET /api/books/3/` po smazání | 404 | `{"error": "Kniha nenalezena"}` |
| `GET /api/books/` po smazání | 200 | `count: 5`, ID 1, 2, 4, 5, 6 |
| `DELETE /api/books/99/` | 404 | `{"error": "Kniha nenalezena"}` |
| `DELETE /api/books/6/`, pak `POST` R.U.R. | 201 | `"id": 6` (nejvyšší zbylé ID je 5) |
| `DELETE /api/books/3/`, pak `POST` R.U.R. | 201 | `"id": 7` (nejvyšší zbylé ID je 6, ne počet knih + 1) |

**Metody a lomítko**

| Request | Status | Poznámka |
|---|---|---|
| `PUT /api/books/` | 405 | `Allow: GET, POST` |
| `DELETE /api/books/` | 405 | mazat celou kolekci nejde |
| `POST /api/books/3/` | 405 | `Allow: GET, DELETE` |
| `PATCH /api/books/3/` | 405 | `Allow: GET, DELETE` |
| `POST /api/books` (bez lomítka) | 500 | `RuntimeError` z `APPEND_SLASH`, POST nejde přesměrovat. Tohle **neopravuj**, jen si všimni proč |

### Otázky k zamyšlení

1. Proč nepovolená metoda vrací 405 a ne 404, když pro `PUT` žádné
   view nemáš?
2. Představ si, že by API mělo přihlášení přes session cookie a view
   by pořád mělo `@csrf_exempt`. Co by se stalo, kdyby cizí stránka
   poslala `POST` z prohlížeče přihlášeného uživatele? Který middleware
   by to bez `@csrf_exempt` zastavil (a proč ne kontrola přihlášení)?
   A proč `@csrf_exempt` v tomhle cvičení nevadí?
3. Smazání knihy 6 a nový `POST` přidělí zase ID 6. Jaký problém by to
   způsobilo klientovi, který si uložil odkaz `/api/books/6/`? Jak to
   řeší databáze (koncept 03)?
4. Proč se chyby polí vrací všechny najednou, a ne jen první? Jak to
   souvisí s formulářem na FE?
5. Proč `{"year": "1920"}` odmítáme, když `?year_from=1920` v `01`
   jsme na číslo převáděli?

## Bonus

Podle konvence tématu jde bonus do appky `bonus` ve stejném projektu
pod prefixem `bonus/`. Data a pomocné funkce smí importovat z appky
`books` (data musí být **tentýž** seznam, ne kopie).

**Částečná úprava:** `PATCH /bonus/books/<id>/` (routa `bonus:detail`)
změní jen pole, která jsou v body.

- Detail přijímá jen `GET` a `PATCH`, jiná metoda → 405.
- Stejné chyby body jako u `POST` (nevalidní JSON, ne-objekt).
- Pole v body se validují **stejnými pravidly** jako u `POST`, chybějící
  pole ale **není** chyba. Validační logiku nekopíruj, uprav ji v `books`
  tak, aby šla použít v obou režimech.
- Prázdný objekt `{}` → 200, kniha beze změny.
- `id` a neznámá pole se ignorují.
- Úspěch → **200** s celou upravenou knihou (`url` vede na detail
  v `books`). Neexistující ID → 404.
- Při chybě se nesmí změnit **žádné** pole, ani to, které bylo validní.

| Request | Body | Status | Odpověď |
|---|---|---|---|
| `PATCH /bonus/books/1/` | `{"year": 1925}` | 200 | `{"id": 1, "title": "Krakatit", "author": "Karel Čapek", "year": 1925, "url": "/api/books/1/"}` |
| `PATCH /bonus/books/1/` | `{"title": " Krakatit II "}` | 200 | `"title": "Krakatit II"`, ostatní beze změny |
| `PATCH /bonus/books/1/` | `{}` | 200 | kniha beze změny |
| `PATCH /bonus/books/1/` | `{"id": 99, "year": 1930}` | 200 | `"id": 1`, `"year": 1930` |
| `PATCH /bonus/books/1/` | `{"title": "", "year": 1930}` | 400 | `{"errors": {"title": "Musí být neprázdný text"}}`, `year` zůstane 1924 |
| `PATCH /bonus/books/1/` | `{"year": null}` | 400 | `{"errors": {"year": "Musí být celé číslo"}}` |
| `PATCH /bonus/books/1/` | `[1]` | 400 | `{"error": "Tělo requestu musí být JSON objekt"}` |
| `PATCH /bonus/books/99/` | `{"year": 1930}` | 404 | `{"error": "Kniha nenalezena"}` |
| `PUT /bonus/books/1/` | | 405 | `Allow: GET, PATCH` |
| `GET /api/books/1/` po prvním `PATCH` | | 200 | `"year": 1925` (stejná data) |
