# Databáze — SQLite, PostgreSQL a jak se do ní podívat

Jakou databázi používáme, jak ji vidět, jak do ní nahrát testovací data
a čím se liší od PostgreSQL, který potkáš v práci. Ověřeno na Django 6.1.

Související: [`MODELS_AND_FIELDS.md`](MODELS_AND_FIELDS.md),
[`MIGRATIONS.md`](MIGRATIONS.md), [`ORM_BASICS.md`](ORM_BASICS.md).

## V tomhle repu: SQLite

```python
# config/settings.py (vygeneroval startproject)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

- Databáze je **jeden soubor** `db.sqlite3` ve složce projektu.
  Vytvoří ho první `migrate`.
- Nic se neinstaluje, neběží žádný server. SQLite je součástí Pythonu.
- `db.sqlite3` se **necommituje** (je v `.gitignore`). Smazat ho můžeš
  kdykoliv, `migrate` vytvoří prázdnou DB znovu.
- Každé cvičení má vlastní soubor, cvičení se navzájem neovlivňují.

## Jak se do databáze podívat

| Nástroj | Jak |
|---|---|
| **Django shell** | `uv run manage.py shell`, pak `Book.objects.all()` (viz [`ORM_BASICS.md`](ORM_BASICS.md)) |
| **PyCharm Professional** | *Database* panel (vpravo) → `+` → *Data Source* → *SQLite* → soubor `db.sqlite3`. Poprvé nabídne stažení ovladače. Tabulky pak vidíš a upravuješ jako v tabulce |
| **DB Browser for SQLite** | samostatná aplikace (`sudo apt install sqlitebrowser`) |
| **admin** | `/admin/` po registraci modelu, koncept 06 |
| `manage.py dbshell` | SQL konzole databáze. U SQLite potřebuje program `sqlite3` (`sudo apt install sqlite3`), jinak hlásí `You appear not to have the 'sqlite3' program installed` |

Tabulky se jmenují `<appka>_<model>`: `library_book`. Kromě tvých tam jsou
tabulky vestavěných appek (`auth_user`, `django_session` …)
a `django_migrations` se seznamem aplikovaných migrací.

## Testovací data: fixtures

Ručně v shellu je to pomalé. Django umí data vyexportovat a nahrát
z JSON souboru (**fixture**):

```bash
# export dat z DB
uv run manage.py dumpdata library --indent 2 -o library/fixtures/books.json

# nahrání (hledá v <appka>/fixtures/ podle jména)
uv run manage.py loaddata books
#   Installed 3 object(s) from 1 fixture(s)
```

```json
[
  {
    "model": "library.book",
    "pk": 1,
    "fields": {"title": "Válka s mloky", "author": "Karel Čapek", "year": 1936}
  }
]
```

- `loaddata` záznamy se stejným `pk` **přepíše**, ostatní nechá být.
  Opakované nahrání tedy nevytváří duplicity.
- Pole, která ve fixture chybí, dostanou `default` z modelu. Povinné pole
  bez `default` musí ve fixture být.
- `loaddata` ukládá „surově“ (`raw`): nevolá vlastní `save()`, validaci
  a **nevyplní `auto_now_add` / `auto_now`**. Pole `created_at` proto
  musí být ve fixture, jinak `NOT NULL constraint failed`.
- Fixture musí odpovídat **aktuálnímu** modelu. Po přidání povinného
  pole bez `default` (třeba unikátního `slug`) stará fixture přestane jít
  nahrát. Vyexportuj ji znovu přes `dumpdata`.
- Fixtures se commitují. V cvičeních je bude mít zadání jako hotový soubor.

Smazání všech dat (tabulky zůstanou):

```bash
uv run manage.py flush --noinput
```

## SQLite vs. PostgreSQL

ORM kód je stejný, liší se chování databáze. Na co narazíš:

| | SQLite (tady) | PostgreSQL (v práci) |
|---|---|---|
| Instalace | nic, soubor | server (Docker, služba), Python balíček `psycopg` |
| `max_length` u `CharField` | **nehlídá**, uloží i delší text | odmítne (`value too long`) |
| `icontains` s diakritikou | `č` ≠ `Č` (jen ASCII bez velikosti písmen) | funguje správně |
| Souběžný zápis | zamyká celou databázi | zamyká jen řádky, desítky současných zápisů |
| `ALTER TABLE` v migracích | většinou přes novou tabulku a kopii dat | přímo |
| Typy | volné (do `integer` sloupce jde uložit text) | striktní |
| Navíc | | `ArrayField`, fulltext, `JSONField` s indexy (`django.contrib.postgres`) |

SQLite je pro produkční web s víc uživateli málokdy vhodná. Pro vývoj,
testy a učení je ideální.

Jak by vypadalo nastavení pro PostgreSQL (jen pro orientaci, v repu ho
nepoužíváme):

```python
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

Přihlašovací údaje se nikdy nepíšou do `settings.py`, berou se
z proměnných prostředí. V pracovních projektech to často řeší balíček
`dj-database-url` (`DATABASE_URL=postgres://…`).

## Časté chyby

| Příznak | Příčina |
|---|---|
| `OperationalError: no such table: …` | chybí `migrate` (nebo jsi smazal `db.sqlite3`) |
| `OperationalError: database is locked` | SQLite zamčená jiným procesem: otevřený zápis v PyCharm Database / DB Browseru, nebo dva procesy zapisují najednou. Zavři ho nebo potvrď změny |
| v PyCharmu nevidíš nová data | Database panel neobnovil pohled, *Refresh* (Ctrl+F5) |
| `CommandError: You appear not to have the 'sqlite3' program installed` | `dbshell` potřebuje `sqlite3`, nebo použij PyCharm / shell |
| `IntegrityError: Problem installing fixture … NOT NULL constraint failed` | ve fixture chybí povinné pole bez `default` |
| `DeserializationError: … Invalid model identifier: library.knihy` | ve fixture nesedí `"model"`, správně `<appka>.<model malými>` (`library.book`) |
