# django

Specifika tohoto tématu:

- Pracujeme s aktuální stabilní verzí **Django 6.1** na **Pythonu 3.14**,
  pro REST API **Django REST Framework (DRF) 3.18**. Python 3.14 instaluje
  a spravuje uv (`uv python install 3.14`), systémový Python 3.12 zůstává
  nedotčený. Kód piš idiomaticky
  pro tyto verze (žádné deprecated API ze starších verzí, i když je uživatel
  může potkat v práci — pokud je rozdíl podstatný, zmiň ho v `THEORY.md`).
- Uživatel (Petr) je zkušený FE developer (TS, Vue, JS), Django lehce
  používá v práci — umí najít URL, view a obslužný kód, ale chybí mu
  ucelený model toho, **jak Django funguje** (request cyklus, ORM,
  migrace, DRF vrstvy). Nepředpokládej hlubokou znalost Pythonu ani BE.
  V `THEORY.md` používej přirovnání k FE světu tam, kde opravdu sedí
  (`urls.py` ≈ router, middleware ≈ router guard / axios interceptor,
  serializer ≈ validační schéma typu zod + mapování na DTO, model ≈ TS
  `interface` + perzistence) — s krátkým kódem vedle sebe, ne jen slovně.
- OOP v Pythonu uživatel zvládá, případně doplňuje za běhu — u
  class-based views / DRF stačí krátká poznámka k Python specifikům
  (dekorátory, `super()`, mixiny/vícenásobná dědičnost), ne výklad OOP.

## Správa závislostí — uv

Používáme [**uv**](https://docs.astral.sh/uv/) (moderní náhrada `pip` +
`venv` + `pip-tools`), ne `pip` / `requirements.txt`. Uživatel uv zná jen
podle jména — u prvních cvičení stručně připomínej příkazy (analogie k
npm: `pyproject.toml` ≈ `package.json`, `uv.lock` ≈ `package-lock.json`,
`.venv/` ≈ `node_modules/`, `uv sync` ≈ `npm install`, `uv add` ≈
`npm install <pkg>`, `uv run` ≈ `npx` / `npm run`). Úvod a přehled příkazů je v
[`UV.md`](UV.md), linter/formatter v [`RUFF.md`](RUFF.md), struktura
Django projektu v
[`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) — v `THEORY.md` na ně
odkazuj místo opakování.

## Struktura cvičení

Každé cvičení je **plnohodnotný, samostatný Django projekt** s vlastním uv
projektem (`pyproject.toml` + `uv.lock` + `.python-version`) — stejně
izolovaný jako Vite projekt u Reactu, žádný sdílený projekt ani venv napříč
cvičeními:

```
exercises/NN-nazev-ukolu/
├── README.md
└── solution/                  # (po dořešení stejně i reference/)
    ├── pyproject.toml         # uv init; závislosti: django (+ DRF od 12)
    ├── uv.lock
    ├── .python-version        # 3.14 (uv init --bare + uv python pin 3.14)
    ├── manage.py
    ├── config/                # django-admin startproject config .
    │   ├── settings.py        # SQLite, jen nutné INSTALLED_APPS
    │   └── urls.py
    └── <app>/                 # manage.py startapp <app>
        ├── models.py, views.py, urls.py, ...   # sem se píše řešení
        └── migrations/
```

- Scaffold je předpřipravený a spustitelný (`startproject` + `startapp`,
  app zaregistrovaná v `INSTALLED_APPS`, `urls.py` napojené). Soubory,
  kam se píše řešení, jsou prázdné stuby — co přesně implementovat, říká
  `README.md`. `pyproject.toml` je bez build-systemu (není to balíček,
  jen aplikace). Výjimka: `01-projekt-a-request-cyklus/exercises/01-prvni-projekt`,
  kde je založení projektu přes uv součástí zadání (`solution/` obsahuje
  jen `.gitkeep`).
- **Ruff** (výslovně vyžádaný, výjimka z obecného pravidla „žádný
  tooling navíc“) je v každém cvičení jako dev závislost
  (`uv add --dev ruff`) s konfigurací v `pyproject.toml`, viz
  [`RUFF.md`](RUFF.md). Scaffold i `reference/` musí projít
  `uv run ruff format --check .` a `uv run ruff check .`. Při kontrole
  řešení upozorni na Ruff chyby stejně jako na ostatní, tedy návodnými
  otázkami. Kód pravidla (např. `DJ008`) jde prozradit, protože ho vypíše
  i sám Ruff.
- Spuštění cvičení v `solution/`: `uv sync`, pak
  `uv run manage.py migrate` a `uv run manage.py runserver`, ověření přes
  prohlížeč / `curl`. Od konceptu testování ověřují zadání i testy
  (`uv run manage.py test`).
- `README.md` obsahuje místo vstup/výstup funkcí **příklady HTTP requestů a
  odpovědí** (metoda, URL, body → status, JSON), resp. ORM dotazů v
  `manage.py shell` a jejich výsledků — vč. okrajových případů (404,
  nevalidní data, prázdný seznam, neexistující ID).
- Bonus (sekce `## Bonus`) jde do druhé app `bonus/` ve stejném projektu,
  namapované pod `/bonus/` — obdoba `bonus.py` vedle `main.py`.
- Migrace se commitují, `db.sqlite3` ne (je v `.gitignore`).

Obecná pravidla repa viz kořenový [`CLAUDE.md`](../CLAUDE.md).
