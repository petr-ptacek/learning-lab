# 03 — Modely a migrace

## Cíl

Přesunout data z Python seznamu do databáze a pochopit, co mezi tvým
kódem a databází dělá Django:

- **model**: popis dat jako Python třída, ze které vznikne tabulka
- **migrace**: jak se změna modelu bezpečně dostane do databáze, tvé
  i kolegů a produkce
- **ORM**: jak data vytvořit, načíst, upravit a smazat bez psaní SQL
- kde se data **validují** (databáze vs. Django) a proč na tom záleží

Staví na `02-urls-a-views`: views, `reverse()` a JSON odpovědi zůstávají,
mění se jen zdroj dat. Na modelech stojí všechno další: querysety (04),
vztahy (05), admin (06), formuláře (08) i DRF (12).

Praktické přehledy, na které se tu odkazuje a které se neopakují:

- [`../docs/MODELS_AND_FIELDS.md`](../docs/MODELS_AND_FIELDS.md): typy
  polí, `null` vs. `blank`, `choices`, `Meta`, omezení, validace
- [`../docs/MIGRATIONS.md`](../docs/MIGRATIONS.md): příkazy, workflow,
  situace z praxe (nové povinné pole, přejmenování, konflikt, návrat)
- [`../docs/ORM_BASICS.md`](../docs/ORM_BASICS.md): CRUD, shell, lookupy
- [`../docs/DATABASE.md`](../docs/DATABASE.md): SQLite, jak se do DB
  podívat, fixtures, rozdíly oproti PostgreSQL

---

## 1. Co je ORM a proč

Databáze rozumí SQL. Tvůj kód je Python. **ORM** (Object-Relational
Mapping) je překladač mezi nimi:

| Databáze | Django | FE obdoba |
|---|---|---|
| tabulka `library_book` | třída `Book(models.Model)` | TS `interface Book` |
| sloupec `title varchar(200)` | atribut `title = models.CharField(max_length=200)` | `title: string` |
| řádek | instance `Book(...)` | objekt `{ id: 1, title: "…" }` |
| `SELECT … WHERE year >= 1930` | `Book.objects.filter(year__gte=1930)` | query builder (Prisma, Knex) |

```python
# Bez ORM (ručně SQL)
cursor.execute("SELECT id, title, year FROM library_book WHERE year >= %s", [1930])
rows = cursor.fetchall()             # [(2, 'Válka s mloky', 1936), ...] — n-tice

# S ORM
books = Book.objects.filter(year__gte=1930)
books[0].title                       # 'Válka s mloky' — objekt s atributy
```

Co ORM přináší:

- **Jeden zdroj pravdy.** Model je zároveň schéma DB, typy pro Python
  a základ pro validaci, admin, formuláře i DRF serializery.
- **Bezpečnost.** Hodnoty jdou do SQL jako parametry, ne lepením stringů.
  SQL injection přes ORM v běžném použití nevznikne.
- **Přenositelnost.** Stejný kód běží na SQLite i PostgreSQL, viz
  [`DATABASE.md`](../docs/DATABASE.md#sqlite-vs-postgresql).

Co ORM neskrývá: každý dotaz je pořád SQL dotaz do databáze. Kolik jich
posíláš, uvidíš v konceptech 04 a 05.

---

## 2. Model → tabulka

```python
# library/models.py
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
```

- Dědí z `models.Model`, tím Django ví, že jde o tabulku.
- `id` se přidá samo (`BigAutoField`, autoincrement).
- Každé pole je **objekt popisující sloupec**, ne hodnota. Na instanci
  (`book.title`) už je to obyčejný `str`.
- Appka musí být v `INSTALLED_APPS`, jinak Django model nevidí:
  `makemigrations` hlásí `No changes detected` a tabulka nevznikne.

V konceptu 02 jsi mohl appku v `INSTALLED_APPS` vynechat a fungovalo to.
Bez modelů ji Django nepotřeboval. Teď už ano.

Typy polí, volby a `Meta`: [`MODELS_AND_FIELDS.md`](../docs/MODELS_AND_FIELDS.md).

---

## 3. Migrace — jak to funguje uvnitř

Změna `models.py` sama databázi nezmění. Mezi nimi jsou migrace:

```
models.py ─► makemigrations ─► migrations/0001_initial.py ─► migrate ─► db.sqlite3
                (porovná)        (soubor v gitu)             (spustí SQL)   + záznam v django_migrations
```

Krok za krokem, co se stane při `makemigrations`:

1. Django načte všechny existující soubory v `migrations/` a **v paměti je
   přehraje**. Vznikne „stav podle migrací“, tedy jak by měla vypadat DB.
2. Porovná ho s aktuálním `models.py`.
3. Rozdíl (nové pole, smazaný model …) zapíše jako nový soubor
   s operacemi (`AddField`, `CreateModel` …).

Databáze se při tom vůbec nečte. Proto `makemigrations` funguje i bez
`db.sqlite3`.

Při `migrate`:

1. Přečte tabulku `django_migrations`: které migrace už v **této**
   databázi proběhly.
2. Neaplikované migrace seřadí podle `dependencies` (graf, ne čísla).
3. Každou převede na SQL pro konkrétní databázi a spustí ji.
4. Zapíše ji do `django_migrations`.

Z toho plynou pravidla, která v týmu platí:

| Pravidlo | Proč |
|---|---|
| migrace se commitují | kolegové a produkce musí přehrát stejnou historii |
| aplikovanou sdílenou migraci neupravuj | ostatní ji mají v `django_migrations` jako hotovou, tvoje úprava se k nim nedostane |
| po `git pull` spusť `migrate` | nové migrace od kolegů ještě nejsou ve tvé DB |
| `db.sqlite3` se necommituje | každý má vlastní data, struktura se vytváří z migrací |

FE obdoba: `migrations/` je jako `package-lock.json` pro strukturu DB.
`django_migrations` je jako `node_modules`: co je u tebe lokálně opravdu
nainstalované.

Příkazy a situace z praxe: [`MIGRATIONS.md`](../docs/MIGRATIONS.md).

---

## 4. Cesta jednoho dotazu

```python
books = Book.objects.filter(author="Karel Čapek").order_by("year")
for book in books:
    print(book.title)
```

1. `Book.objects` je **manager**, vstupní bod pro dotazy na tabulku.
2. `.filter(...)` a `.order_by(...)` vrací **QuerySet**, tedy popis dotazu.
   Do DB se zatím nic neposlalo.
3. `for` QuerySet **vyhodnotí**: Django složí SQL
   (`SELECT … FROM library_book WHERE author = %s ORDER BY year`), pošle ho
   s parametrem `"Karel Čapek"` a dostane řádky.
4. Z každého řádku vytvoří instanci `Book`. Převede typy (`smallint` →
   `int`, `datetime` → `datetime` s časovou zónou).

Lenost QuerySetu je jako u builderu dotazů na FE: řetězíš, dokud nečteš.
Že `print(qs.query)` vypíše SQL a kdy přesně se dotaz posílá, je
v [`ORM_BASICS.md`](../docs/ORM_BASICS.md#objects-a-queryset). Do hloubky
v konceptu 04.

---

## 5. Kdo hlídá data: databáze vs. Django

V konceptu 02 jsi validoval ručně ve view. S modelem jsou kontroly ve
**třech vrstvách**:

| Vrstva | Co hlídá | Kdy běží | Chyba |
|---|---|---|---|
| **databáze** | `NOT NULL`, `UNIQUE`, `CHECK` (omezení z modelu) | vždy, při každém `INSERT` / `UPDATE` | `IntegrityError` → 500, pokud ji nechytíš |
| **model** (`full_clean()`) | `blank`, `max_length`, `choices`, `validators`, formát e-mailu… | **jen když ho zavoláš** | `ValidationError` s `message_dict` |
| **view / formulář / serializer** | tvar requestu, JSON, typy | v tvém kódu | tvoje 400 odpověď |

Nejdůležitější věta konceptu: **`save()` a `create()` model nevalidují.**

```python
Book.objects.create(title="", author="a", year=2000)        # uloží prázdný název
Book.objects.create(title="x" * 500, author="a", year=2000) # SQLite uloží 500 znaků
Book.objects.create(title="T", author="a", year=-5)
# IntegrityError: CHECK constraint failed — to hlídá databáze
```

Proč to tak je: `save()` volá kód všude (skripty, migrace, testy, hromadné
importy) a validace by ho zpomalovala nebo blokovala. Validace patří
k **datům od uživatele**. Formuláře (08) a DRF (12) volají `full_clean()`
za tebe. Do té doby ho voláš sám, nebo validuješ ve view jako v 02.

Co dát kam:

| Pravidlo | Kam |
|---|---|
| hodnota nesmí chybět | pole bez `null=True` (DB) + bez `blank=True` (validace) |
| nesmí být duplicita | `unique=True` / `UniqueConstraint` (DB) |
| rozsah, vztah mezi sloupci | `CheckConstraint` (DB) |
| povolené hodnoty | `choices` (validace) |
| formát, délka | typ pole + `max_length` (validace) |
| závisí na requestu nebo uživateli | view / serializer |

Detail a ověřené výstupy:
[`MODELS_AND_FIELDS.md`](../docs/MODELS_AND_FIELDS.md#validace-co-hlídá-databáze-a-co-django).

---

## 6. Model ve view

Views z konceptu 02 se mění jen v tom, odkud berou data. Struktura
(metody, statusy, JSON, `reverse()`) zůstává.

```python
from .models import Book


def serialize_book(book):
    return {
        "id": book.pk,
        "title": book.title,
        # ...
        "url": reverse("books:detail", args=[book.pk]),
    }
```

Instance modelu **není slovník**: `{**book}` ani `book["title"]` nefungují
a `JsonResponse(book)` taky ne. Převod model → JSON píšeš ručně. To je
přesně práce, kterou později převezme DRF serializer.

Kterou metodu kdy:

| Potřebuješ | Použij | Ne |
|---|---|---|
| jeden záznam podle ID, 404 když není | `try: Book.objects.get(pk=…)` / `except Book.DoesNotExist` | `filter(...)[0]` (`IndexError`) |
| jeden záznam nebo `None` | `filter(...).first()` | |
| jestli něco existuje | `.exists()` | `len(qs) > 0` |
| počet | `.count()` | `len(qs)` |
| upravit jeden objekt | změnit atributy + `save(update_fields=[...])` | |
| upravit hodně řádků najednou | `qs.update(...)` (pozor, obchází `save()`) | cyklus se `save()` |
| vytvořit, když neexistuje | `get_or_create(...)` | `get` + `except` + `create` |

Příklady ke každé: [`ORM_BASICS.md`](../docs/ORM_BASICS.md).

---

## Časté chyby

| Příznak | Příčina |
|---|---|
| `No changes detected` po úpravě modelu | appka není v `INSTALLED_APPS` |
| `OperationalError: no such table` | chybí `migrate` |
| `OperationalError: no such column` | změna modelu bez nové migrace, nebo migrace neaplikovaná |
| `Book.DoesNotExist` → 500 | `get()` bez `try` / `except` |
| uložila se prázdná nebo nevalidní hodnota | `save()` nevaliduje, chybí `full_clean()` / vlastní validace |
| `IntegrityError` → 500 | porušení `unique` / `CHECK` / `NOT NULL`, nechycené |
| `TypeError: 'Book' object is not subscriptable` | `book["title"]` místo `book.title` |
| po přejmenování pole zmizela data | na `Was … renamed …?` odpověď `N` |
| `<Book: Book object (1)>` | chybí `__str__` |

Další v [`MODELS_AND_FIELDS.md`](../docs/MODELS_AND_FIELDS.md#časté-chyby),
[`MIGRATIONS.md`](../docs/MIGRATIONS.md#časté-chyby) a
[`ORM_BASICS.md`](../docs/ORM_BASICS.md#časté-chyby).
