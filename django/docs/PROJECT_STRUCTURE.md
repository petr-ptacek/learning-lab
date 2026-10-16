# Struktura Django projektu

Referenční přehled: co je který soubor, jak spolu souvisí a kde co hledat.
Do hloubky jednotlivé části rozebírají koncepty v [`ROADMAP.md`](../ROADMAP.md).

## Projekt vs. app

Django rozlišuje dvě úrovně:

- **Projekt** je celá aplikace: konfigurace (`settings.py`), hlavní
  routing a vstupní body pro server. V jednom repu je jeden.
- **App** je jedna funkční oblast (např. `tasks`, `users`, `billing`)
  s vlastními modely, views a URL. Projekt se skládá z více appek a
  appka se teoreticky dá přenést do jiného projektu.

FE obdoba: projekt je celá Vue aplikace (`main.ts`, router, konfigurace),
appka je feature modul (`src/features/tasks/` s vlastními komponentami,
store a routami).

Proto se zakládají dvěma příkazy:

```bash
uv run django-admin startproject config .   # projekt (konfigurace do config/)
uv run manage.py startapp tasks             # app
```

> Název `config` je konvence. Výchozí `startproject mysite` pojmenuje
> konfigurační složku stejně jako projekt (`mysite/mysite/`), což mate.
> V práci můžeš potkat obojí.

## Strom souborů

```
solution/
├── pyproject.toml, uv.lock, .python-version   # uv, viz UV.md
├── manage.py            # CLI vstup: runserver, migrate, shell, test, ...
├── db.sqlite3           # databáze (vznikne po migrate, necommituje se)
│
├── config/              # PROJEKT — konfigurace
│   ├── __init__.py      # dělá ze složky Python balíček (bývá prázdný)
│   ├── settings.py      # veškerá konfigurace
│   ├── urls.py          # kořenový routing, sem se napojují appky
│   ├── wsgi.py          # vstup pro produkční server (gunicorn, ...)
│   └── asgi.py          # totéž pro async servery (uvicorn, ...)
│
└── tasks/               # APP — jedna funkční oblast
    ├── __init__.py
    ├── apps.py          # konfigurace appky (název, signály v ready())
    ├── models.py        # datové modely = tabulky v DB
    ├── migrations/      # vygenerované změny schématu DB (commitují se)
    ├── views.py         # obsluha requestů → response
    ├── urls.py          # routy appky (startapp ho NEvytvoří, zakládá se ručně)
    ├── admin.py         # registrace modelů do /admin/
    └── tests.py         # testy
```

Soubory, které přibývají s dalšími koncepty (stejné názvy uvidíš v práci):

| Soubor                         | Co v něm je                                      | Koncept |
|--------------------------------|--------------------------------------------------|---------|
| `templates/tasks/*.html`       | HTML šablony                                     | 07      |
| `forms.py`                     | formuláře a validace                             | 08      |
| `serializers.py`               | DRF: převod model ↔ JSON + validace              | 12      |
| `permissions.py`               | DRF: vlastní oprávnění                           | 14      |
| `management/commands/*.py`     | vlastní `manage.py` příkazy                      | 17      |
| `signals.py`                   | reakce na události modelů                        | 17      |
| `services.py` / `selectors.py` | business logika mimo views (konvence, ne Django) | —       |

## `settings.py` — co je důležité

```python
DEBUG = True  # detailní chybové stránky; v produkci False
SECRET_KEY = "..."  # podepisování sessions/tokenů; v produkci z env
ALLOWED_HOSTS = []  # domény, na kterých server odpovídá

INSTALLED_APPS = [  # které appky jsou aktivní
  "django.contrib.admin",  # vestavěné appky Djanga (admin, auth, ...)
  "django.contrib.auth",
  # ...
  "tasks",  # ← vlastní appku je potřeba sem přidat,
]  # jinak Django nevidí její modely a migrace

MIDDLEWARE = [...]  # řetězec funkcí kolem každého requestu (koncept 11)
ROOT_URLCONF = "config.urls"  # odkud začíná routing
DATABASES = { ... }  # připojení k DB (u nás SQLite)
```

Ze settings se nic neimportuje přímo. Všude se používá
`from django.conf import settings`.

## Jak to do sebe zapadá — cesta requestu

`GET /tasks/42/`:

```
 HTTP request
     │
     ▼
 MIDDLEWARE (settings.py)         sessions, auth, CSRF, ... (≈ router guards)
     │
     ▼
 config/urls.py                   path("tasks/", include("tasks.urls"))
     │  odřízne "tasks/", zbytek pošle dál
     ▼
 tasks/urls.py                    path("<int:pk>/", views.task_detail)
     │  pk=42
     ▼
 tasks/views.py                   task_detail(request, pk=42)
     │  ▲
     ▼  │
 tasks/models.py  ── ORM ──►  DB  Task.objects.get(pk=42)
     │
     ▼
 HttpResponse / JsonResponse      zpět přes MIDDLEWARE → klient
```

V kódu:

```python
# config/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
]
```

```python
# tasks/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.task_detail, name="task-detail"),
]
```

```python
# tasks/models.py
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title   # jak se objekt zobrazí v adminu, shellu, logu
```

```python
# tasks/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Task


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)   # neexistuje → 404
    return JsonResponse({"id": task.pk, "title": task.title, "done": task.done})
```

Pro srovnání stejná routa ve Vue Routeru:

```ts
// router.ts
{ path: '/tasks/:id(\\d+)', component: TaskDetail }
```

Rozdíl: ve Vue je cílem routy komponenta, která si data dotáhne sama.
V Djangu je cílem **funkce, která dostane request a musí vrátit
response**. Mezi tím může dělat cokoliv (DB, validace, volání API).

## Užitečné `manage.py` příkazy

```bash
uv run manage.py runserver        # dev server na http://127.0.0.1:8000
uv run manage.py makemigrations   # z modelů vygeneruje migrace
uv run manage.py migrate          # aplikuje migrace na DB
uv run manage.py shell            # Python REPL s načteným Djangem (zkoušení ORM)
uv run manage.py createsuperuser  # uživatel do /admin/
uv run manage.py test             # spustí testy
```

## Jak se zorientovat v cizím (pracovním) projektu

1. `settings.py` → `INSTALLED_APPS`: jaké appky projekt má (vlastní i
   knihovny jako `rest_framework`).
2. `ROOT_URLCONF` → kořenový `urls.py` → `include(...)`: kterou URL obsluhuje
   která appka.
3. V appce `models.py`: s jakými daty pracuje. To je nejrychlejší cesta
   k pochopení domény.
4. `views.py` + `serializers.py`: co dělá API.
5. `MIDDLEWARE`: co se děje s každým requestem (auth, logování, tenanti, ...).

## Odkazy

- [Tutorial, část 1 — projekt, app, první view](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
- [Applications](https://docs.djangoproject.com/en/6.1/ref/applications/) — co je app
- [Settings reference](https://docs.djangoproject.com/en/6.1/ref/settings/)
- [django-admin a manage.py](https://docs.djangoproject.com/en/6.1/ref/django-admin/)
