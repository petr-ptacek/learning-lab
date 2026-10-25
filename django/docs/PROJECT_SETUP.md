# Založení Django projektu krok za krokem

Postup, jak v prázdné složce (u cvičení `solution/`) založit Django projekt
s uv, Ruffem a jednou appkou. Co je pak který soubor, popisuje
[`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md). Nástroje do hloubky
vysvětlují [`UV.md`](UV.md) a [`RUFF.md`](RUFF.md).

V příkladech se appka jmenuje `books` a má prefix `api/books/`. Ve cvičení
použij název a prefix ze zadání.

## Přehled

| # | Příkaz / akce | Výsledek |
|---|---|---|
| 1 | `cd …/solution` | jsi ve správné složce |
| 2 | `uv init --bare` | `pyproject.toml` |
| 3 | `uv python pin 3.14` | `.python-version` |
| 4 | `uv add django` | Django v `.venv`, zapsané v `pyproject.toml` + `uv.lock` |
| 5 | `uv add --dev ruff` | Ruff jako vývojová závislost |
| 6 | konfigurace Ruffu do `pyproject.toml` | Ruff ví, co kontrolovat |
| 7 | `uv run django-admin startproject config .` | `manage.py` + `config/` |
| 8 | `uv run manage.py migrate` + `runserver` | DB s tabulkami vestavěných appek, ověřený běh |
| 9 | `uv run manage.py startapp books` | appka `books/` |
| 10 | `books` do `INSTALLED_APPS` | Django appku vidí |
| 11 | vytvořit `books/urls.py` | routy appky |
| 12 | `include()` v `config/urls.py` | routy appky pod prefixem |
| 13 | `uv run ruff check --fix .` + `uv run ruff format .` | kód projde Ruffem |
| 14 | PyCharm: interpreter + Sources Root | napovídání a debugger |

---

## 1. Přejdi do složky projektu

```bash
cd django/02-urls-a-views/exercises/01-katalog-knih/solution
ls -a      # jen . .. .gitkeep
```

Všechny další příkazy se spouštějí **odsud**. uv i Django pracují
s aktuální složkou, takže ve špatné složce založíš projekt jinam.

## 2. uv projekt

```bash
uv init --bare
```

Vytvoří `pyproject.toml`, tedy manifest projektu (obdoba `npm init` →
`package.json`). `--bare` znamená bez ukázkového `main.py` a `README.md`,
protože Django si soubory vytvoří samo.

## 3. Verze Pythonu

```bash
uv python pin 3.14
```

Vytvoří `.python-version` s `3.14` (obdoba `.nvmrc`). Když Python 3.14 na
stroji chybí, uv ho při dalším kroku sám stáhne.

## 4. Django

```bash
uv add django
```

Udělá tři věci najednou: zapíše `django` do `dependencies` v
`pyproject.toml`, zamkne přesné verze do `uv.lock` a nainstaluje Django do
`.venv/` (které při prvním použití vytvoří). Obdoba `npm install django`.

**Ne** `pip install django`. To by Django nainstalovalo, ale projekt by
o něm nevěděl (nebylo by v `pyproject.toml` ani v `uv.lock`).

## 5. Ruff

```bash
uv add --dev ruff
```

`--dev` zařadí Ruff do vývojových závislostí (`[dependency-groups] dev`),
obdoba `npm install -D`.

## 6. Konfigurace Ruffu

Na konec `pyproject.toml` připiš:

```toml
[tool.ruff]
extend-exclude = ["*/migrations/*"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "DJ"]
ignore = ["E501"]
```

Co která sada pravidel hlídá, je v [`RUFF.md`](RUFF.md).

## 7. Django projekt

```bash
uv run django-admin startproject config .
```

Rozbor příkazu:

| Část | Význam |
|---|---|
| `uv run` | spusť v prostředí projektu (`.venv`) |
| `django-admin` | CLI Djanga, nainstalované v kroku 4 |
| `startproject` | vytvoř projekt |
| `config` | **jméno** projektu = jméno konfigurační složky (`config/settings.py`, …) |
| `.` | **cílová složka** = aktuální složka, tedy `manage.py` přímo v `solution/` |

Proč `django-admin`, a ne `manage.py`: **`manage.py` vzniká až tímhle
příkazem.** Dokud projekt neexistuje, `manage.py` taky neexistuje. Od
teď už všechno spouštíš přes `uv run manage.py …`, protože `manage.py`
navíc ví, který `settings.py` načíst.

Bez tečky (`startproject config`) by vznikla vnořená složka
`config/config/` a `manage.py` by nebyl v `solution/`.

Výsledek:

```
solution/
├── manage.py
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## 8. Migrace a první spuštění

```bash
uv run manage.py migrate
uv run manage.py runserver
```

- `migrate` vytvoří `db.sqlite3` s tabulkami vestavěných appek (uživatelé,
  sessions, …). Tvoje appka zatím nemá modely, takže `makemigrations` teď
  není potřeba. Viz sekce o migracích v `01-projekt-a-request-cyklus/THEORY.md`.
- Otevři `http://127.0.0.1:8000/`. Měla by tam být **uvítací stránka
  s raketou**. Ukazuje se jen, dokud `config/urls.py` nemá žádné vlastní
  routy, takže ji ověř teď. Po kroku 12 bude na `/` místo ní 404.
- Server zastav přes `Ctrl+C`.

## 9. Appka

```bash
uv run manage.py startapp books
```

Vytvoří `books/` s `models.py`, `views.py`, `admin.py`, `apps.py`,
`tests.py` a `migrations/`. **Nevytvoří `urls.py`**, ten přidáš v kroku 11.

Název appky je Python identifikátor: malá písmena, množné číslo podle
konvence (`books`, `orders`), bez pomlček.

## 10. Registrace appky

V `config/settings.py` přidej appku do `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    # … vestavěné appky
    "django.contrib.staticfiles",
    "books",
]
```

Bez registrace views fungují, ale Django nevidí modely, migrace, admin
ani šablony appky. Proto to dělej vždycky hned po `startapp`.

## 11. `urls.py` appky

Vytvoř `books/urls.py`:

```python
from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    # path("", views.book_list, name="list"),
]
```

- `app_name` = jmenný prostor pro `reverse("books:…")` (koncept 02).
- Dokud nemáš první routu, Ruff hlásí nepoužité importy `path` a
  `views`. To je v pořádku, zmizí s první routou.

## 12. Napojení do `config/urls.py`

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("books.urls")),
]
```

- `include` je potřeba doplnit do importu.
- Prefix **bez** úvodního lomítka a **s** koncovým (`"api/books/"`).
- Výsledná URL routy = prefix + cesta v `books/urls.py`.

## 13. Ruff

```bash
uv run ruff check --fix .
uv run ruff format .
uv run ruff check .            # kontrola: All checks passed!
uv run ruff format --check .   # kontrola: … files already formatted
```

Proč hned u čerstvého projektu: vygenerované soubory Ruffem neprojdou.

- `startapp` dává do `admin.py`, `models.py` a `tests.py` nepoužité
  importy (`F401`). `--fix` je odstraní.
- `startproject` používá jednoduché uvozovky, `format` je převede na
  dvojité.

Totéž pouštěj před každým odevzdáním řešení.

## 14. PyCharm

Interpreter přepni na `solution/.venv/bin/python` a přidej ho jako typ
**uv** (Add Local Interpreter → Type: uv → Select existing). Jako
Virtualenv / Python by PyCharm ukázal prázdný seznam balíčků, protože
uv do `.venv` neinstaluje `pip`. `solution/` pak označ jako Sources Root.
Podrobně v [`UV.md`](UV.md#nastavení-pycharmu).

---

## Co se commituje

| Commitovat | Necommitovat (je v `.gitignore`) |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | `.venv/` |
| `manage.py`, `config/`, `books/` včetně `migrations/` | `db.sqlite3` |
| | `__pycache__/` |

## Celý postup najednou

```bash
cd …/solution
uv init --bare
uv python pin 3.14
uv add django
uv add --dev ruff
# → konfigurace Ruffu do pyproject.toml (krok 6)
uv run django-admin startproject config .
uv run manage.py migrate
uv run manage.py runserver            # ověřit raketu, Ctrl+C
uv run manage.py startapp books
# → "books" do INSTALLED_APPS (krok 10)
# → books/urls.py (krok 11)
# → include() v config/urls.py (krok 12)
uv run ruff check --fix . && uv run ruff format .
```

## Časté chyby při zakládání

| Chyba | Příčina |
|---|---|
| `can't open file '…/manage.py': No such file or directory` (resp. u `uv run manage.py` jen `No such file or directory (os error 2)`) | spouštíš `manage.py` před `startproject` (krok 7 používá `django-admin`) |
| `CommandError: …/manage.py already exists` | `startproject` jsi už jednou spustil. Django existující soubory nepřepisuje. |
| vnořené `config/config/`, `manage.py` ve špatné složce | chybí tečka na konci `startproject config .` |
| `CommandError: '…' is not a valid project name` | prohozené argumenty (`startproject . config`) nebo neplatný název |
| `pyenv: version '3.14' is not installed` | holý `python` místo `uv run`, viz [`UV.md`](UV.md) |
| `ModuleNotFoundError: No module named 'django'` | Django není přidané (`uv add django`) nebo běžíš mimo `uv run` |
| rakety na `/` není, je tam 404 | to je správně po kroku 12, raketa je jen u projektu bez vlastních rout |
