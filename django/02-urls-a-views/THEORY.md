# 02 — URLs a views

## Cíl

Naučit se z requestu vytáhnout všechno, co view potřebuje:

- **parametry z cesty** (`/api/books/3/`)
- **query parametry** (`?author=čapek&year_from=1930`)
- **metodu a JSON body** (`POST` s `{"title": …}`)

A naopak URL **neskládat ručně**, ale generovat je z pojmenovaných rout
přes `reverse()`. Na konci bys měl umět napsat jednoduché JSON API
s detailem, výpisem, filtry, vytvořením a smazáním záznamu a správnými
statusy. Je to ruční verze toho, co později udělá DRF (koncepty 12–13).

Staví na `01-projekt-a-request-cyklus` (view, `urls.py`, `include()`,
`JsonResponse`). Data zatím držíme v obyčejném Python seznamu, databáze
přijde v konceptu 03. Jak založit a spustit projekt: [`../docs/UV.md`](../docs/UV.md)
a zadání cvičení `01-prvni-projekt`.

---

## 1. Jak Django najde view — krok za krokem

V konceptu 01 jsi viděl, že `urlpatterns` se prochází shora dolů. Teď
podrobněji, co se děje s URL `/api/books/3/` při tomhle nastavení:

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("books.urls")),
]

# books/urls.py
app_name = "books"
urlpatterns = [
    path("", views.book_list, name="list"),
    path("<int:book_id>/", views.book_detail, name="detail"),
]
```

1. Django vezme cestu **bez úvodního lomítka a bez query stringu**:
   `api/books/3/`. Query (`?author=…`) se pro výběr routy vůbec
   nepoužívá, skončí v `request.GET`.
2. Projde `config/urls.py` (`ROOT_URLCONF`):
   - `admin/` nesedí
   - `api/books/` sedí jako **začátek** cesty. U `include()` se porovnává
     jen prefix, který se **odřízne**, a zbytek `3/` jde do `books/urls.py`.
3. Projde `books/urls.py` se zbytkem `3/`:
   - `""` nesedí (zbytek není prázdný)
   - `<int:book_id>/` sedí a converter `int` z `"3"` udělá `3`
4. Zavolá `views.book_detail(request, book_id=3)`.

U `/api/books/abc/` sedí krok 2, ale v kroku 3 nesedí nic (`abc` není
`int`), takže vznikne **404 bez zavolání jakéhokoliv view**. U
`/api/books/3` (bez lomítka) taky nic nesedí. Pak nastoupí
`CommonMiddleware` a `APPEND_SLASH` z konceptu 01 (301).

Výpis zkoušených rout na debug 404 stránce je přesně tenhle průchod.

### Pořadí rout

Vyhrává první shoda, takže konkrétní cesty patří **nad** obecné:

```python
urlpatterns = [
    path("new/", views.book_new),              # ✅ musí být první
    path("<str:slug>/", views.book_by_slug),   # "new" by jinak padlo sem
]
```

---

## 2. Parametry v cestě — path convertery

```python
# books/urls.py
path("<int:book_id>/", views.book_detail)

# books/views.py
def book_detail(request, book_id):   # book_id je už int, ne string
    ...
```

Pro srovnání Vue Router:

```ts
// router.ts
{ path: '/books/:id(\\d+)', component: BookDetail }

// BookDetail.vue
const route = useRoute()
route.params.id   // vždycky string, převod na číslo je na tobě
```

Zápis `<converter:jméno>` znamená:
- **converter** určuje, jaký text v URL sedí a na jaký typ se převede,
- **jméno** je název **keyword argumentu**, se kterým Django zavolá view.
  Musí přesně sedět s parametrem funkce.

| Converter | Sedí na | Hodnota ve view |
|---|---|---|
| `str` (výchozí, `<book_id>`) | cokoliv kromě `/`, neprázdné | `str` |
| `int` | `0` nebo kladné celé číslo | `int` |
| `slug` | písmena, číslice, `-`, `_` (`valka-s-mloky`) | `str` |
| `uuid` | UUID (`075194d3-6885-417e-a8a8-6c931e272f00`) | `uuid.UUID` |
| `path` | cokoliv **včetně** `/` | `str` |

Důsledky:
- **Validaci formátu dělá router.** `/api/books/abc/` a `/api/books/-1/`
  (záporná čísla `int` nebere) se k view vůbec nedostanou. Ve view už
  nemusíš řešit „je to číslo?“, jen „existuje taková kniha?“.
- **Bez converteru je to `str`.** `<book_id>` předá `"3"` a porovnání
  `book["id"] == book_id` (`3 == "3"`) v Pythonu vrátí `False`. Python
  na rozdíl od JS `==` typy nepřevádí.
- Víc parametrů = víc keyword argumentů:
  `path("<int:year>/<slug:slug>/", views.article)` →
  `article(request, year=2026, slug="django")`.

Když vestavěné convertery nestačí (třeba rok jako přesně 4 číslice),
existují vlastní convertery nebo `re_path()` s regulárním výrazem. Viz
odkazy v `RESOURCES.md`, v praxi je potřeba zřídka.

---

## 3. `include()`, `app_name` a pojmenované routy

```python
# books/urls.py
app_name = "books"                          # namespace appky

urlpatterns = [
    path("", views.book_list, name="list"),                     # books:list
    path("<int:book_id>/", views.book_detail, name="detail"),   # books:detail
]
```

- `name` dá routě jméno. Je to **identifikátor routy**, nezávislý na
  tom, jak vypadá její URL.
- `app_name` zařadí jména do **jmenného prostoru** appky. Dvě appky tak
  můžou mít routu `detail` bez kolize (`books:detail`, `authors:detail`).
  Bez `app_name` by se jména z různých appek přepisovala.

Obdoba ve Vue Routeru je `name` u routy. Namespace tam neexistuje, a
proto se jména píšou s prefixem ručně (`book-detail`, `author-detail`).

---

## 4. `reverse()` — URL ze jména routy

`reverse()` dělá opačný směr než router: **ze jména a parametrů složí
URL**.

```python
from django.urls import reverse

reverse("books:list")                            # "/api/books/"
reverse("books:detail", args=[3])                # "/api/books/3/"
reverse("books:detail", kwargs={"book_id": 3})   # totéž, explicitněji
```

Obdoba ve Vue Routeru:

```ts
router.resolve({ name: 'book-detail', params: { id: 3 } }).href   // "/books/3"
router.push({ name: 'book-detail', params: { id: 3 } })
```

**Proč ne `f"/api/books/{book_id}/"`:** URL je definovaná na jednom
místě (`urls.py`, včetně prefixu v `config/urls.py`). Když se prefix
změní na `api/v2/books/`, `reverse()` vrátí novou URL sám, kdežto ručně
složené řetězce rozesetě po kódu by se tiše rozbily. Je to stejný
důvod, proč ve Vue používáš `router.push({ name })` místo
`router.push('/books/' + id)`.

Kde se stejný princip potkáš dál:
- `redirect("books:detail", book_id=3)`: přesměrování podle jména
- `{% url "books:detail" 3 %}`: totéž v šablonách (koncept 07)
- DRF pole `url` / `HyperlinkedModelSerializer` (koncept 12)

**Chyby:** neexistující jméno, chybějící `books:` prefix nebo chybějící /
špatně typovaný parametr vyhodí `NoReverseMatch`. `reverse()` totiž
ověřuje, že by výsledná URL **opravdu prošla** routou včetně converteru,
takže `reverse("books:detail", args=["abc"])` taky selže.

### Query string a absolutní URL

`reverse()` vrací jen **cestu**, bez query stringu a domény:

```python
from urllib.parse import urlencode

f"{reverse('books:list')}?{urlencode({'author': 'čapek', 'year_from': 1930})}"
# "/api/books/?author=%C4%8Dapek&year_from=1930"
```

`urlencode` ze standardní knihovny správně zakóduje speciální znaky
(diakritiku, mezery, `&`), což ruční lepení `"?author=" + author`
nezvládne.

Absolutní URL (s `http://…`) složí z aktuálního requestu
`request.build_absolute_uri(reverse("books:detail", args=[3]))` →
`"http://127.0.0.1:8000/api/books/3/"`. Tak to dělá DRF. Ve cvičeních
stačí relativní cesty.

---

## 5. Objekt `request`

```python
request.method               # "GET", "POST", ...
request.path                 # "/api/books/" (bez query)
request.GET                  # query parametry: QueryDict
request.headers["Accept"]    # hlavičky, názvy bez ohledu na velikost písmen
request.body                 # surové body (bytes), u JSONu json.loads(request.body)
```

Metodu a JSON body rozebírá podsekce
[Metoda a JSON body](#metoda-a-json-body) níže.

### Query parametry — `request.GET`

`GET /api/books/?author=čapek&year_from=1930&tag=a&tag=b&limit=`

```python
request.GET.get("author")             # "čapek" (už dekódované z %C4%8D…)
request.GET.get("year_from")          # "1930"  ← vždycky string!
request.GET.get("missing")            # None (parametr chybí)
request.GET.get("missing", "10")      # "10" (výchozí hodnota)
request.GET.get("limit")              # "" (parametr je, ale prázdný)
request.GET.getlist("tag")            # ["a", "b"]
request.GET.get("tag")                # "b" (jen poslední hodnota)
"author" in request.GET               # True
```

`QueryDict` se chová jako slovník, ale jeden klíč může mít víc hodnot
(`?tag=a&tag=b`). Obdoba `route.query` ve Vue, taky vždycky stringy.
Je **neměnný**: když ho potřebuješ upravit (třeba při skládání URL další
stránky), udělej si kopii `request.GET.copy()`.

**Chybějící vs. prázdný parametr:** `?limit=` dá `""`, ne `None`. Obojí
je v Pythonu „falsy“, takže `if not value:` pokryje oba případy. Zda se
prázdný parametr chová jako chybějící, je rozhodnutí API, a zadání
cvičení ho určuje.

**Převod na číslo:** `int("1930")` → `1930`, ale `int("abc")` i
`int("1.5")` vyhodí `ValueError`. Neošetřený `ValueError` ve view znamená
**500**, tedy chybu serveru, i když chybu udělal klient. Správně je
chytit ho (`try` / `except ValueError`) a vrátit **400 Bad Request**
s vysvětlením. Když stejný převod potřebuješ pro víc parametrů, vyplatí
se malá pomocná funkce.

`request.GET` existuje u **každé** metody (query string může mít i POST).
Název je jen historický.

### Metoda a JSON body

V REST API sdílí jedna URL víc operací a liší se metodou:

| Request | Operace | Obvyklý status úspěchu |
|---|---|---|
| `GET /api/books/` | výpis | 200 |
| `POST /api/books/` | vytvoření | **201 Created** + hlavička `Location` |
| `GET /api/books/3/` | detail | 200 |
| `DELETE /api/books/3/` | smazání | **204 No Content**, prázdné body |

Router (`urls.py`) metodu **nerozlišuje**. Obě metody na stejné URL
dorazí do stejného view a větví se až uvnitř přes `request.method`
(vždy velkými písmeny, `"POST"`). Obdoba Express `router.route("/books")
.get(…).post(…)`, jen ručně.

Nepovolenou metodu odmítne dekorátor z `django.views.decorators.http`:

```python
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def book_list(request): ...
```

Pro jinou metodu vrátí **405** s hlavičkou `Allow: GET, POST` a prázdným
body, a tvoje view se vůbec nezavolá. Existují i zkratky `@require_GET`
a `@require_POST`.

**JSON body** je v `request.body` jako surové `bytes`. `request.POST`
obsahuje jen data z HTML formuláře (`application/x-www-form-urlencoded`),
pro JSON je **prázdný**. Na rozdíl od Expressu s `express.json()` Django
JSON za tebe neparsuje:

```python
import json

data = json.loads(request.body)   # bytes → Python objekt
```

- Nevalidní JSON (i prázdné body `b""`) vyhodí `json.JSONDecodeError`,
  podtřídu `ValueError`. Neošetřený znamená 500, správně je 400.
- Validní JSON nemusí být objekt. `json.loads(b"[1, 2]")` vrátí `list`,
  `json.loads(b"42")` vrátí `int`. Na `data.get(...)` pak dostaneš
  `AttributeError`.

Převod typů JSON → Python:

| JSON | Python | Pozor |
|---|---|---|
| `{}` | `dict` | |
| `[]` | `list` | |
| `"text"` | `str` | `"1936"` je pořád string, ne číslo |
| `1936` | `int` | |
| `1936.0` | `float` | není `int`, i když je „celé“ |
| `true` / `false` | `True` / `False` | `bool` je v Pythonu **podtřída `int`**: `isinstance(True, int)` je `True` |
| `null` | `None` | |

JSON nemá schéma, takže typ každého pole ověřuješ sám. Obdoba ručního
`typeof` / zod validace na FE. DRF serializery (koncept 12) to později
udělají deklarativně a chyby vrátí ve tvaru
`{"pole": ["zpráva"]}`, tedy po polích, ne jednou hláškou.

**Hlavičky odpovědi:** `HttpResponse` / `JsonResponse` se k nim chová
jako ke slovníku:

```python
response = JsonResponse(data, status=201)
response["Location"] = "/api/books/7/"   # hodnotu samozřejmě přes reverse()
return response
```

**Prázdná odpověď (204):** `HttpResponse(status=204)`. `JsonResponse`
by vždy poslal nějaké JSON body.

**CSRF:** POST a DELETE na obyčejné Django view z Postmanu skončí
**403**, viz [`../docs/CSRF.md`](../docs/CSRF.md). Pro učební API bez
přihlášení stačí `@csrf_exempt` (kdy ano a kdy ne je v CSRF.md). DRF to
pak řeší samo.

---

## 6. Status kódy a chybové odpovědi v API

| Status | Kdy | Příklad |
|---|---|---|
| **200 OK** | úspěch, i když je výsledek prázdný | `?author=xyz` → `{"count": 0, "results": []}` |
| **201 Created** | záznam vytvořen | `POST /api/books/` → nová kniha + `Location` |
| **204 No Content** | úspěch bez těla | `DELETE /api/books/3/` |
| **400 Bad Request** | klient poslal nesmysl | `?year_from=abc`, nevalidní JSON, chybějící pole |
| **403 Forbidden** | chybí CSRF token (u nás) | POST z Postmanu bez `@csrf_exempt` |
| **404 Not Found** | konkrétní zdroj neexistuje | `/api/books/99/` |
| **405 Method Not Allowed** | URL existuje, metoda ne | view s `@require_http_methods(["GET", "POST"])` dostane `PUT` (u POST/PUT/DELETE bez CSRF tokenu ale dřív zasáhne CSRF → 403) |
| **500 Internal Server Error** | chyba **serveru**: neošetřená výjimka | `int("abc")` bez `try` |

Prázdný výsledek filtru je **200**, ne 404. Kolekce `/api/books/`
existuje, jen v ní nic neodpovídá filtru. 404 patří ke konkrétnímu
zdroji, který neexistuje.

Jak 404 vrátit:

| Způsob | Co klient dostane |
|---|---|
| `return JsonResponse({"error": "Kniha nenalezena"}, status=404)` | **JSON** se statusem 404 ✅ pro API |
| `raise Http404("…")` / `get_object_or_404(...)` | Djangova **HTML** 404 stránka (debug nebo obecná) |
| converter nesedí / routa neexistuje | taky HTML 404 |

FE, které volá API, čeká JSON i u chyby (`await res.json()`). Dokud
nemáme DRF (koncept 12), vracej chyby v API ručně přes `JsonResponse`.
`Http404` a `get_object_or_404` se hodí pro klasické HTML stránky.

---

## 7. JSON a diakritika

`JsonResponse` ve výchozím stavu převádí ne-ASCII znaky na escape
sekvence:

```python
JsonResponse({"author": "Karel Čapek"})
# {"author": "Karel Čapek"}
```

Je to platný JSON a `JSON.parse` / Postman (záložka *Pretty*) ho přečtou
správně, jen surová odpověď (*Raw*, `curl`) je nečitelná. `JsonResponse`
předává `json.dumps` volby přes parametr `json_dumps_params`. Najdi
v dokumentaci `json.dumps`, která volba to řídí.

Mimochodem, `JsonResponse` ve výchozím stavu přijme jen `dict`. Seznam na
nejvyšší úrovni (`JsonResponse([...])`) vyhodí `TypeError`, dokud
nepředáš `safe=False`. Proto se kolekce obvykle balí do objektu
(`{"count": …, "results": [...]}`), což má i tu výhodu, že jde později
přidat stránkování bez rozbití klientů.

---

## Časté chyby

| Příznak | Příčina |
|---|---|
| `TypeError: book_detail() got an unexpected keyword argument 'id'` | jméno parametru v routě (`<int:id>`) nesedí s parametrem funkce |
| `NoReverseMatch` | překlep ve jménu routy, chybí `app_name` prefix (`books:`), chybí parametr, nebo parametr neprojde converterem |
| porovnání `book["id"] == book_id` nikdy nesedí | `book_id` je string, protože converter chybí (`<book_id>` = `str`) |
| 500 u `?year_from=abc` | neošetřený `int(...)` → `ValueError` |
| HTML 404 místo JSON | `Http404` / `get_object_or_404` v API view |
| `TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False` | `JsonResponse` dostal seznam místo dictu |
| filtr na `?author=` (prázdný) nic nenajde / najde vše nečekaně | prázdný string vs. `None`, viz sekce 5 |
| `403 CSRF verification failed` u POST / DELETE z Postmanu | chybí `@csrf_exempt` (nebo CSRF token), viz [`CSRF.md`](../docs/CSRF.md) |
| `request.POST` je prázdný, i když posíláš JSON | `request.POST` čte jen formuláře, JSON je v `request.body` |
| 500 `JSONDecodeError` | neošetřený `json.loads` na nevalidní nebo prázdné body |
| 500 `AttributeError: 'list' object has no attribute 'get'` | body je validní JSON, ale ne objekt |
| `"year": true` projde kontrolou na `int` | `bool` je podtřída `int` |
| 500 `RuntimeError: You called this URL via POST, but the URL doesn't end in a slash` | `POST /api/books` bez lomítka, `APPEND_SLASH` neumí POST přesměrovat |
