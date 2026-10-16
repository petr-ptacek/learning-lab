# 01 — Projekt a request cyklus

## Cíl

Pochopit, co se v Djangu děje od chvíle, kdy přijde HTTP request, do chvíle,
kdy odejde response, a umět založit funkční projekt od nuly. Naučíš se:

- založit Django projekt přes uv
- napsat první views
- napojit je na URL
- přečíst si nastavení ze `settings.py`

Na tomhle stojí všechno další v roadmapě. Modely, DRF i middleware jsou
jen další vrstvy kolem stejného cyklu.

Struktura souborů je popsaná v [`../PROJECT_STRUCTURE.md`](../PROJECT_STRUCTURE.md),
nástroje v [`../UV.md`](../UV.md) a [`../RUFF.md`](../RUFF.md). Tady se
neopakují.

## Jak spustit cvičení

V `solution/` daného cvičení:

```bash
uv sync
uv run manage.py migrate      # vytvoří db.sqlite3 (tabulky vestavěných appek)
uv run manage.py runserver    # http://127.0.0.1:8000
```

`runserver` je vývojový server, obdoba `vite dev`. Při změně `.py` souboru
se sám restartuje. V produkci se nepoužívá, tam běží gunicorn/uvicorn přes
`config/wsgi.py` / `asgi.py`.

## View = funkce, která dostane request a vrátí response

Tohle je jádro celého Djanga. View je obyčejná Python funkce:

- první parametr je `request` (objekt `HttpRequest`: metoda, hlavičky,
  query, body, …)
- **musí vrátit** objekt `HttpResponse` (nebo jeho podtřídu)

Pro srovnání s Expressem, který znáš z JS světa:

```ts
// Express (Node)
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})
```

```python
# Django — tasks/views.py
from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok"})


# tasks/urls.py
urlpatterns = [
    path("api/health/", views.health),
]
```

Dva rozdíly:

1. **Routa a handler jsou oddělené.** View neví, na jaké URL visí. Mapování
   je v `urls.py`.
2. **View response vrací (`return`), nevolá `res.json()`.** Když zapomeneš
   `return`, Django spadne s chybou
   `The view ... didn't return an HttpResponse object. It returned None instead.`

### `HttpResponse` vs. `JsonResponse`

```python
from django.http import HttpResponse, JsonResponse

HttpResponse("Ahoj")                     # 200, Content-Type: text/html; charset=utf-8
HttpResponse("Nenalezeno", status=404)   # vlastní status
JsonResponse({"status": "ok"})           # 200, Content-Type: application/json
JsonResponse({"error": "..."}, status=400)
```

`JsonResponse` je `HttpResponse`, který dict serializuje přes
`json.dumps` a nastaví správný `Content-Type`. Dokud nepřijde DRF
(koncept 12), budeš API vracet takhle.

## `urls.py` — routing

```python
# config/urls.py — kořen, odkazuje se na něj ROOT_URLCONF v settings.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),   # vše ostatní řeší appka pages
]
```

- `urlpatterns` je **seznam**, který se prochází shora dolů. Vyhrává
  **první shoda**. Když nic nesedí, vrátí se 404.
- Cesty se píšou **bez úvodního lomítka** (`"api/health/"`, ne
  `"/api/health/"`) a konvenčně **s koncovým lomítkem**.
- `include("pages.urls")` deleguje zbytek URL na `urlpatterns` v
  `pages/urls.py`, podobně jako vnořené `children` ve Vue Routeru. Do
  hloubky (parametry, pojmenované routy, `reverse()`) to řeší koncept 02.

### Koncové lomítko a `APPEND_SLASH`

`GET /api/health` (bez lomítka) na routu `api/health/` nevrátí 404, ale
**301 redirect** na `/api/health/`. Stará se o to `CommonMiddleware`
s nastavením `APPEND_SLASH = True` (výchozí).

U POST to nejde: redirect by ztratil body. V `DEBUG` režimu proto Django
schválně spadne s chybou 500 a vysvětlením. V praxi to je častá chyba FE,
které posílá POST na URL bez lomítka.

## `settings.py` a `django.conf.settings`

`settings.py` je obyčejný Python modul plný konstant (velkými písmeny).
V kódu se ale **nikdy neimportuje přímo**:

```python
from django.conf import settings   # ✅ správně

settings.DEBUG          # True
settings.TIME_ZONE      # "UTC"
```

```python
from config import settings        # ❌ obchází Django (výchozí hodnoty, testy, …)
```

`django.conf.settings` je objekt, který Django naplní při startu. Obsahuje
i výchozí hodnoty pro nastavení, která v souboru nemáš (např.
`APPEND_SLASH`).

### `DEBUG`

`DEBUG = True` (výchozí po `startproject`) zapne podrobné chybové stránky:
u 404 vypíše všechny zkoušené routy, u 500 celý traceback s proměnnými.
Pro vývoj ideální. V produkci musí být `False`, jinak prozradíš kód i
nastavení.

## `manage.py`

Tenký wrapper kolem `django-admin`. Jediné, co navíc dělá, je nastavení
`DJANGO_SETTINGS_MODULE=config.settings`, aby příkazy věděly, který
projekt mají načíst. Proto se po založení projektu všechno dál spouští
přes `uv run manage.py …`.

## Migrace — stručně

Do hloubky je řeší koncept 03. Tady jen tolik, abys věděl, co dělá
`migrate` hned po založení projektu.

**Migrace = verzovaná změna schématu databáze, uložená jako soubor
v repu.** Místo ručního `CREATE TABLE` / `ALTER TABLE` popíšeš data
v Pythonu (model) a Django z toho vygeneruje kroky, jak DB dostat do
odpovídajícího stavu. Obdoba z JS světa: migrace v Prisma / Knex /
TypeORM. Dá se to brát i jako „git pro strukturu DB“: každá migrace je
commit, který ví, na které předchozí navazuje.

Dva příkazy, dvě různé věci:

| Příkaz | Co dělá | Sahá na DB? |
|---|---|---|
| `uv run manage.py makemigrations` | porovná modely (`models.py`) s existujícími migracemi a **vygeneruje nový soubor** do `<app>/migrations/` | ne |
| `uv run manage.py migrate` | **aplikuje** všechny dosud neaplikované migrace na DB | ano |

Při změně modelu je tedy pořadí vždycky **`makemigrations` → `migrate`**.
Vygenerovaný soubor se commituje, aby kolega (nebo produkce) jen pustil
`migrate` a měl stejné schéma.

Které migrace už v DB jsou, si Django pamatuje v tabulce
`django_migrations`. `migrate` je proto bezpečné pouštět opakovaně:
aplikuje jen to, co chybí.

**Proč `migrate` hned u prázdného projektu?** Vestavěné appky
v `INSTALLED_APPS` (`auth`, `admin`, `sessions`, `contenttypes`) mají
modely i migrace přibalené přímo v Djangu (tabulky uživatelů, sessions,
…). `makemigrations` u čerstvého projektu nic nevygeneruje (`No changes
detected`), protože tvoje appka zatím nemá modely. `migrate` jen aplikuje
ty hotové migrace. Dokud to neuděláš, `runserver` hlásí
`You have N unapplied migration(s)`.

```bash
uv run manage.py showmigrations   # přehled: [X] aplikovaná, [ ] čeká
```

## Cesta requestu — co se děje před tvým view

```
request → MIDDLEWARE (shora dolů) → URL resolver → view
response ← MIDDLEWARE (zdola nahoru) ←─────────────┘
```

Middleware (seznam `MIDDLEWARE` v settings) jsou vrstvy kolem každého
requestu. Kterákoliv z nich může request **zastavit dřív, než dojde k
view**. Ve cvičení to uvidíš na vlastní oči:

```bash
curl -i -X POST http://127.0.0.1:8000/api/health/
# HTTP/1.1 403 Forbidden — CSRF verification failed
```

Tvoje `health` view se vůbec nezavolalo. Request zastavil
`CsrfViewMiddleware`, protože POST nemá CSRF token. Proč to tak je a jak
se to u API řeší, přijde v konceptech 10, 11 a 14. Teď stačí vědět, že
mezi `curl` a tvou funkcí něco je.

## Projekt vs. app — kdy appku registrovat

Appku z `startapp` přidej do `INSTALLED_APPS`. Pro samotné views to
technicky potřeba není (URL resolver najde funkci přes import), ale bez
registrace Django nevidí modely, migrace, šablony ani admin dané appky.
Registruj ji proto vždycky hned po `startapp`.

## Časté chyby

| Příznak | Příčina |
|---|---|
| `didn't return an HttpResponse object` | ve view chybí `return` |
| 404 se seznamem zkoušených rout | překlep v cestě, chybí `include()`, nebo chybí lomítko na konci routy |
| warning `urls.W002` při startu | cesta začíná `/` |
| `ModuleNotFoundError: No module named 'django'` | spouštíš `python` mimo venv, místo něj použij `uv run` |
| 403 CSRF u POST | `CsrfViewMiddleware`, viz výše |
