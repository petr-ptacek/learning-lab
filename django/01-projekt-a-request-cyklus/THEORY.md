# 01 — Projekt a request cyklus

## Cíl

Pochopit, co se v Djangu děje od chvíle, kdy přijde HTTP request, do chvíle,
kdy odejde response, a umět založit funkční projekt od nuly. Naučíš se:

- založit Django projekt přes uv
- napsat první views
- napojit je na URL
- přečíst si nastavení ze `settings.py`
- rozumět tomu, co mezi klientem a tvým view dělají middleware

Na tomhle stojí všechno další v roadmapě. Modely, DRF i autentizace jsou
jen další vrstvy kolem stejného cyklu.

Struktura souborů je popsaná v [`../docs/PROJECT_STRUCTURE.md`](../docs/PROJECT_STRUCTURE.md),
nástroje v [`../docs/UV.md`](../docs/UV.md) a [`../docs/RUFF.md`](../docs/RUFF.md). Tady se
neopakují.

## Jak spustit cvičení

V `solution/` daného cvičení:

```bash
uv sync
uv run manage.py migrate      # vytvoří db.sqlite3 (tabulky vestavěných appek)
uv run manage.py runserver    # http://127.0.0.1:8000
```

---

## 1. Velký obrázek — co Django vlastně je

Django je **knihovna, kterou volá webový server**. Samo o sobě na síti
neposlouchá. Mezi serverem a Djangem je standardní rozhraní:

```
prohlížeč / Postman
      │  HTTP
      ▼
webový server          runserver (vývoj), gunicorn / uvicorn (produkce)
      │  WSGI / ASGI   standardní Python rozhraní „server ↔ aplikace“
      ▼
config/wsgi.py         application = get_wsgi_application()
      │
      ▼
Django                 middleware → URL resolver → tvoje view
```

- **WSGI** (synchronní) a **ASGI** (async) jsou dohody, jak server předá
  request aplikaci a jak od ní dostane response. Díky nim jde Django
  pustit pod libovolným kompatibilním serverem. V `config/wsgi.py` a
  `asgi.py` je jen vstupní bod `application`.
- Obdoba z JS: Express app je funkce `(req, res) => …`, kterou volá
  Nodeův `http` server. Django je totéž, jen se standardizovaným
  rozhraním.

### Dvě fáze: start procesu a obsluha requestu

**Při startu procesu (jednou):**

1. Načte se `settings.py` (podle `DJANGO_SETTINGS_MODULE`).
2. Django projde `INSTALLED_APPS` a naplní **registr appek**: načte
   jejich konfiguraci (`apps.py`), modely, a zavolá `AppConfig.ready()`.
3. Sestaví se řetězec middleware a načte se URLconf (`config/urls.py`).

**Pro každý request (pořád dokola):**

1. Server předá surová data requestu a Django z nich vyrobí objekt
   `HttpRequest`.
2. Request projde middleware (shora dolů).
3. URL resolver najde podle cesty view.
4. Zavolá se view a vrátí `HttpResponse`.
5. Response projde middleware zpátky (zdola nahoru).
6. Server ji pošle klientovi.

**Důležitý důsledek:** proces běží dlouho a obslouží tisíce requestů.
Kód na úrovni modulu (mimo funkce), třeba `BOOKS = [...]` v `data.py`,
se provede **jednou** a sdílí ho všechny requesty. Kdybys do takového
seznamu ve view zapisoval, změny by „prosakovaly“ mezi requesty a
uživateli. V produkci navíc běží víc procesů (gunicorn workery), každý
s vlastní kopií, takže by se data mezi nimi rozcházela. Stav patří do
databáze, ne do proměnných modulu.

---

## 2. Projekt vs. app

| | Projekt | App |
|---|---|---|
| Vznikne | `django-admin startproject config .` | `uv run manage.py startapp pages` |
| Obsahuje | `settings.py`, kořenové `urls.py`, `wsgi.py`/`asgi.py` | modely, views, URL, admin, testy jedné oblasti |
| Kolik jich je | jeden | libovolně (`users`, `orders`, `billing`, …) |
| FE obdoba | celá Vue aplikace (`main.ts`, router, config) | feature modul (`src/features/orders/`) |

Appka se aktivuje přidáním do **`INSTALLED_APPS`**. To ji zapíše do
registru appek (fáze startu, krok 2). Bez registrace:

- **views fungují dál**: URL resolver jen importuje modul
  (`include("pages.urls")`) a k tomu registr nepotřebuje,
- ale Django **nevidí** modely a migrace appky (`makemigrations` řekne
  `No changes detected`), její `admin.py`, šablony v `pages/templates/`,
  statické soubory, `AppConfig.ready()` ani vlastní `manage.py` příkazy.

Nic z toho nehlásí chybu hned, a proto se appka registruje vždycky hned
po `startapp`. `apps.py` z `startapp` stačí tak, jak je. Atribut `label`
(technický identifikátor, musí to být platný Python identifikátor, bez
mezer) se mění jen výjimečně. `verbose_name` je lidský název pro admin.

---

## 3. `manage.py` a `django-admin`

`django-admin` je CLI Djanga. `manage.py` je tenký wrapper, který navíc
nastaví `DJANGO_SETTINGS_MODULE=config.settings`, aby příkazy věděly,
který projekt mají načíst. Po založení projektu proto všechno spouštíš
přes `uv run manage.py …`.

| Příkaz | Co dělá |
|---|---|
| `runserver` | vývojový server, obdoba `vite dev` |
| `migrate` / `makemigrations` | migrace, viz sekce 8 |
| `shell` | Python REPL s načteným Djangem (zkoušení kódu, ORM) |
| `check` | statická kontrola projektu (settings, URL, modely) |
| `startapp` | nová appka |
| `createsuperuser` | uživatel do `/admin/` |
| `test` | spustí testy (koncept 16) |

**`runserver` uvnitř:** spustí dva procesy. Hlídací proces sleduje
změny `.py` souborů a při změně restartuje ten druhý, který obsluhuje
requesty. Proto se po uložení souboru server sám restartuje, a proto se
debugger v PyCharmu musí připojovat i k podprocesům (viz
[`../docs/UV.md`](../docs/UV.md)). V produkci se `runserver` nepoužívá:
není optimalizovaný na výkon ani zabezpečený.

---

## 4. `settings.py` a `django.conf.settings`

`settings.py` je obyčejný Python modul plný konstant (velkými písmeny).
V kódu se ale **nikdy neimportuje přímo**:

```python
from django.conf import settings   # ✅ správně

settings.DEBUG          # True
settings.TIME_ZONE      # "UTC"
settings.APPEND_SLASH   # True, i když v settings.py není
```

```python
from config import settings        # ❌ obchází Django
```

`django.conf.settings` je objekt, který Django naplní při startu
**dvěma vrstvami**: nejdřív výchozí hodnoty Djanga (`global_settings`,
stovky nastavení), pak přepíše tím, co je v tvém `settings.py`. Přímý
import by výchozí hodnoty neměl. Navíc testy umí settings dočasně
přepsat (`override_settings`), a to funguje jen přes
`django.conf.settings`.

Nastavení, která potkáš hned na začátku:

| Nastavení | K čemu je |
|---|---|
| `DEBUG` | podrobné chybové stránky; v produkci `False` |
| `SECRET_KEY` | podepisování sessions, tokenů, CSRF; v produkci tajný, z env |
| `ALLOWED_HOSTS` | domény, pod kterými server odpovídá |
| `INSTALLED_APPS` | aktivní appky (sekce 2) |
| `MIDDLEWARE` | řetězec vrstev kolem requestu (sekce 7) |
| `ROOT_URLCONF` | odkud začíná routing (`"config.urls"`) |
| `DATABASES` | připojení k DB (u nás SQLite) |
| `TIME_ZONE`, `USE_TZ` | časová pásma, viz [`../docs/TIME_AND_TIMEZONES.md`](../docs/TIME_AND_TIMEZONES.md) |

### `DEBUG`

`DEBUG = True` (výchozí po `startproject`) zapne podrobné chybové stránky:
u 404 vypíše všechny zkoušené routy, u 500 celý traceback s proměnnými.
Pro vývoj ideální. V produkci musí být `False`, jinak prozradíš kód i
nastavení. Proč přesně a jak s tím souvisí `ALLOWED_HOSTS`, je v
[`../docs/DEBUG_AND_ALLOWED_HOSTS.md`](../docs/DEBUG_AND_ALLOWED_HOSTS.md).

---

## 5. View = funkce, která dostane request a vrátí response

Tohle je jádro celého Djanga. View je obyčejná Python funkce:

- první parametr je `request` (objekt `HttpRequest`: metoda, hlavičky,
  query, body, …; do hloubky v konceptu 02)
- **musí vrátit** objekt `HttpResponse` (nebo jeho podtřídu)

Pro srovnání s Expressem, který znáš z JS světa:

```ts
// Express (Node)
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})
```

```python
# Django — pages/views.py
from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok"})


# pages/urls.py
urlpatterns = [
    path("api/health/", views.health),
]
```

Dva rozdíly:

1. **Routa a handler jsou oddělené.** View neví, na jaké URL visí. Mapování
   je v `urls.py`.
2. **View response vrací (`return`), nevolá `res.json()`.** Response je
   obyčejný objekt, který jde vytvořit, upravit a vrátit. Když zapomeneš
   `return`, Django spadne s chybou
   `The view ... didn't return an HttpResponse object. It returned None instead.`

### Response objekty

```python
from django.http import HttpResponse, JsonResponse

HttpResponse("Ahoj")                     # 200, Content-Type: text/html; charset=utf-8
HttpResponse("Nenalezeno", status=404)   # vlastní status
HttpResponse("a,b", content_type="text/csv")
JsonResponse({"status": "ok"})           # 200, Content-Type: application/json
JsonResponse({"error": "..."}, status=400)

response = JsonResponse({"status": "ok"})
response["Cache-Control"] = "no-store"   # hlavičku jde nastavit i dodatečně
return response
```

`JsonResponse` je `HttpResponse`, který dict serializuje přes
`json.dumps` a nastaví správný `Content-Type`. Dokud nepřijde DRF
(koncept 12), budeš API vracet takhle.

Status a body jsou na sobě nezávislé. Chybový status s JSON body
(`{"error": "…"}`) je u API běžná praxe. FE pozor: `fetch` u 4xx/5xx
nevyhodí výjimku (`res.ok === false`), axios ano.

---

## 6. `urls.py` — routing

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
  `"/api/health/"`). Django porovnává cestu už bez něj, takže
  `"/api/health/"` by nikdy nesedělo (a `check` hlásí varování
  `urls.W002`). Konvenčně se píšou **s koncovým lomítkem**.
- `include("pages.urls")` odřízne sedící prefix a zbytek cesty předá
  `urlpatterns` v `pages/urls.py`, podobně jako vnořené `children` ve
  Vue Routeru. Výsledná URL = prefix + cesta v appce, takže
  `path("/", include(...))` + `path("", ...)` dá `"/"`, což nesedí na
  prázdnou cestu `/`.

Průchod resolveru krok za krokem, parametry v URL a pojmenované routy
řeší koncept 02.

---

## 7. Middleware — co se děje před tvým view a po něm

Middleware jsou vrstvy kolem **každého** requestu, jako slupky cibule:

```
request ──► Security ─► Session ─► Common ─► Csrf ─► Auth ─► … ─► URL resolver ─► view
                                                                                   │
response ◄─ Security ◄─ Session ◄─ Common ◄─ Csrf ◄─ Auth ◄─ … ◄───────────────────┘
```

Obdoba z FE: axios interceptory (request i response) nebo router guardy
ve Vue. Každá vrstva může request upravit, odpověď upravit, nebo
**request zastavit a odpovědět sama**. Pak se view vůbec nezavolá.

Výchozí `MIDDLEWARE` po `startproject` (pořadí je důležité):

| Middleware | Co dělá |
|---|---|
| `SecurityMiddleware` | bezpečnostní hlavičky (HSTS, `X-Content-Type-Options`, …), přesměrování na HTTPS |
| `SessionMiddleware` | načte session z cookie → `request.session` |
| `CommonMiddleware` | `APPEND_SLASH` (doplnění lomítka), blokování user agentů |
| `CsrfViewMiddleware` | CSRF ochrana pro POST/PUT/PATCH/DELETE |
| `AuthenticationMiddleware` | přihlášený uživatel → `request.user` (potřebuje session, proto je až za ní) |
| `MessageMiddleware` | jednorázové „flash“ zprávy mezi stránkami |
| `XFrameOptionsMiddleware` | hlavička `X-Frame-Options` proti vložení stránky do cizího `<iframe>` |

Vlastní middleware se píše v konceptu 11.

### Tři situace ze cvičení `01-prvni-projekt`

| Request | Výsledek | Kdo odpověděl |
|---|---|---|
| `GET /api/health` (bez lomítka) | 301 → `/api/health/` | `CommonMiddleware`: routa nesedí, s lomítkem by seděla → redirect |
| `POST /api/health` (bez lomítka) | 500 `RuntimeError` | `CommonMiddleware`: redirect by ztratil body POSTu, Django raději hlasitě spadne |
| `POST /api/health/` | 403 CSRF | `CsrfViewMiddleware`: chybí CSRF token |

Ve všech třech případech se tvoje view **nezavolalo**, ověřitelné
breakpointem.

Proč 403 vs. 500 záleží na lomítku: CSRF kontrola potřebuje vědět, které
view se bude volat (view může mít CSRF vypnuté), takže běží až po
nalezení routy. Bez lomítka se routa nenajde, ke CSRF kontrole se
nedojde a zasáhne `CommonMiddleware`.

**Pravidlo pro FE:** POST/PUT/PATCH/DELETE posílej vždy na URL
s koncovým lomítkem. Co je CSRF a jak ho FE řeší, je v
[`../docs/CSRF.md`](../docs/CSRF.md).

---

## 8. Migrace — stručně

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

---

## Časté chyby

| Příznak | Příčina |
|---|---|
| `didn't return an HttpResponse object` | ve view chybí `return` |
| 404 se seznamem zkoušených rout | překlep v cestě, chybí `include()`, nebo chybí lomítko na konci routy |
| warning `urls.W002` při startu | cesta začíná `/` |
| `ImproperlyConfigured: The app label '…' is not a valid Python identifier` | `label` v `apps.py` obsahuje mezeru apod.; `label` většinou vůbec nenastavuj |
| `ModuleNotFoundError: No module named 'django'` | spouštíš `python` mimo venv, místo něj použij `uv run` |
| `pyenv: version '3.14' is not installed` | holý `python` v uv projektu, viz [`../docs/UV.md`](../docs/UV.md) |
| 301 u GET bez lomítka, 500 u POST bez lomítka | `APPEND_SLASH`, viz sekce 7 |
| 403 CSRF u POST | `CsrfViewMiddleware`, viz sekce 7 |
| `makemigrations` hlásí `No changes detected`, i když model existuje | appka chybí v `INSTALLED_APPS` |
