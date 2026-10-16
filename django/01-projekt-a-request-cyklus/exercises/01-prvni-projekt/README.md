# 01 — První projekt

Založ Django projekt od nuly a napiš první views. Tohle je výjimka ze
zvyklosti tématu: `solution/` není předpřipravený. Celé založení projektu
přes uv je součástí úkolu, protože ho budeš v práci i ve vlastních
projektech dělat znovu a znovu.

## Část 1 — Založení projektu

Všechno v `solution/` (je v ní jen prázdný `.gitkeep`, aby složka šla
commitnout). Příkazy najdeš v [`UV.md`](../../../UV.md) a
[`RUFF.md`](../../../RUFF.md).

- Založ uv projekt bez ukázkových souborů a připni Python 3.14.
- Přidej `django` jako závislost a `ruff` jako dev závislost.
- Do `pyproject.toml` přidej konfiguraci Ruffu z `RUFF.md`.
- Vytvoř Django projekt s konfigurační složkou `config` **přímo do
  `solution/`** (pozor na tečku na konci příkazu, viz
  [`PROJECT_STRUCTURE.md`](../../../PROJECT_STRUCTURE.md)).
- Vytvoř appku `pages` a zaregistruj ji v `INSTALLED_APPS`.
- Spusť migrace a dev server a ověř, že na `http://127.0.0.1:8000/` vidíš
  uvítací stránku Djanga s raketou.

Výsledná struktura (bez `.venv/` a `db.sqlite3`):

```
solution/
├── .gitkeep
├── .python-version
├── pyproject.toml
├── uv.lock
├── manage.py
├── config/
└── pages/
```

## Část 2 — Views

Ve `pages/views.py` napiš tři views a napoj je přes nový soubor
`pages/urls.py`, který z `config/urls.py` zahrneš pomocí `include()`:

| Metoda + URL | View | Vrací |
|---|---|---|
| `GET /` | `home` | text `Ahoj z Djanga!` (`HttpResponse`) |
| `GET /api/health/` | `health` | JSON `{"status": "ok"}` |
| `GET /api/info/` | `info` | JSON s informacemi o běžícím serveru (viz níže) |

`/api/info/` vrací:

- `framework`: vždy `"Django"`
- `django_version`: verze Djanga jako string (Django ji umí vrátit samo,
  dohledej v dokumentaci)
- `python_version`: verze Pythonu jako string (standardní knihovna, modul
  `platform`)
- `debug`: aktuální hodnota `DEBUG` ze settings (načtená správným
  způsobem, viz `THEORY.md`)

Po zastavení serveru musí projít:

```bash
uv run ruff format --check .
uv run ruff check .
```

### Příklady request → response

Ověřuj přes `curl -i` (vypíše i status a hlavičky), GET případně
v prohlížeči.

| Request | Status | `Content-Type` | Body |
|---|---|---|---|
| `GET /` | 200 | `text/html; charset=utf-8` | `Ahoj z Djanga!` |
| `GET /api/health/` | 200 | `application/json` | `{"status": "ok"}` |
| `GET /api/info/` | 200 | `application/json` | `{"framework": "Django", "django_version": "6.1.2", "python_version": "3.14.8", "debug": true}` |
| `GET /api/health` (bez lomítka) | 301 | `text/html; charset=utf-8` | prázdné, hlavička `Location: /api/health/` |
| `GET /neexistuje/` | 404 | `text/html; charset=utf-8` | debug stránka se seznamem zkoušených rout |
| `POST /api/health/` | 403 | `text/html; charset=utf-8` | `CSRF verification failed` |
| `POST /api/health` (bez lomítka) | 500 | `text/html; charset=utf-8` | `RuntimeError`, Django vysvětluje, proč nemůže přesměrovat |

Konkrétní verze v `/api/info/` se můžou lišit podle toho, co ti uv
nainstaluje. Důležité je, že je nevypisuješ natvrdo.

### Otázky k zamyšlení

Odpověz si sám (nemusíš je nikam psát), u kontroly se na ně zeptám:

1. Proč `GET /api/health` vrátí 301, ale `POST /api/health` 500? Kdo z
   cesty requestu to rozhoduje?
2. U `POST /api/health/` → 403: zavolala se vůbec tvoje funkce `health`?
   Jak bys to ověřil (např. `print()` ve view)?
3. Co se stane, když `pages` vyřadíš z `INSTALLED_APPS`? Funguje to
   pořád? Proč (viz `THEORY.md`)?
4. Co vrátí `GET /neexistuje/`, když v settings nastavíš `DEBUG = False`?
   (Bude potřeba upravit i `ALLOWED_HOSTS`, Django ti řekne jak.)

## Bonus

Podle konvence tématu jde bonus do druhé appky `bonus` ve stejném
projektu, namapované pod `/bonus/`.

- Vytvoř appku `bonus`, zaregistruj ji a napoj její `urls.py` pod
  prefix `bonus/`.
- Přepni projekt do českého časového pásma (`Europe/Prague`) v settings.
- `GET /bonus/time/` vrátí aktuální **místní** čas serveru v ISO formátu a
  název časového pásma ze settings. Django má pro práci s časem vlastní
  modul, nepoužívej `datetime.now()` napřímo. Zjisti proč.
- `GET /bonus/teapot/` vrátí JSON `{"error": "Jsem konvice"}` se statusem
  **418**.

| Request | Status | Body |
|---|---|---|
| `GET /bonus/time/` | 200 | `{"now": "2026-10-16T11:45:52.404927+02:00", "time_zone": "Europe/Prague"}` |
| `GET /bonus/time/` v zimě | 200 | `{"now": "2026-12-01T09:00:00.000000+01:00", "time_zone": "Europe/Prague"}` |
| `GET /bonus/teapot/` | 418 | `{"error": "Jsem konvice"}` |
| `GET /bonus/` | 404 | prefix sám žádnou view nemá |
| `GET /time/` | 404 | bonusové views jsou jen pod `/bonus/` |

Všimni si offsetu `+02:00` / `+01:00` (letní / zimní čas). Kdyby tam bylo
`+00:00`, vracíš čas v UTC, ne místní.
