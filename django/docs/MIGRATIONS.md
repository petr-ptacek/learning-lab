# Migrace — jak se model dostane do databáze

Co migrace jsou, jak s nimi pracovat denně a jak řešit situace, na které
v týmu narazíš (nové povinné pole, přejmenování, konflikt po merge, návrat
zpět). Výstupy příkazů jsou ověřené na Django 6.1.

Související: [`MODELS_AND_FIELDS.md`](MODELS_AND_FIELDS.md),
[`ORM_BASICS.md`](ORM_BASICS.md), [`DATABASE.md`](DATABASE.md).

## Mentální model

Migrace jsou **verzovaná historie schématu databáze**, uložená jako Python
soubory v `<appka>/migrations/`. Obdoba migrací z Prisma / Knex / TypeORM,
nebo „git pro strukturu tabulek“.

```
models.py  ──makemigrations──►  migrations/0002_book_pages.py  ──migrate──►  DB
(jak to má být)                 (recept na změnu, commituje se)              (jak to je)
```

- **`makemigrations`** porovná `models.py` se stavem, který vznikne
  přehráním dosavadních migrací, a rozdíl zapíše jako nový soubor.
  **Na databázi při tom nesahá.**
- **`migrate`** spustí na databázi migrace, které tam ještě neproběhly.
  Které proběhly, si Django pamatuje v tabulce `django_migrations`.

Proto jsou to dva kroky. Migraci vytvoří jeden vývojář, commitne ji
a všichni ostatní (i produkce) ji jen aplikují přes `migrate`. Obdoba
`package.json` vs. `npm install`: migrace jsou předpis, `migrate` ho
provede.

## Denní workflow

```bash
# 1. upravíš models.py
uv run manage.py makemigrations          # vytvoří migraci
#    Migrations for 'library':
#      library/migrations/0002_book_pages.py
#        + Add field pages to book

# 2. (doporučeno) podíváš se, co vznikne
uv run manage.py sqlmigrate library 0002 # SQL, které migrace spustí

# 3. aplikuješ
uv run manage.py migrate
#    Applying library.0002_book_pages... OK

# 4. commitneš models.py i nový soubor v migrations/ dohromady
```

Po `git pull` od kolegy stačí `uv run manage.py migrate`.

## Přehled příkazů

| Příkaz | Co dělá |
|---|---|
| `makemigrations` | nové migrace pro všechny appky |
| `makemigrations library` | jen pro jednu appku |
| `makemigrations -n add_isbn` | vlastní název souboru (`0003_add_isbn.py`) |
| `makemigrations --dry-run` | ukáže, co by vzniklo, nic nezapíše |
| `makemigrations --check` | skončí kódem 1, když model a migrace nesedí (do CI) |
| `makemigrations --empty library -n fill_x` | prázdná migrace pro ruční (datovou) migraci |
| `makemigrations --merge` | sloučí dvě větve migrací, viz [Konflikt](#konflikt-po-merge-dvě-migrace-se-stejným-číslem) |
| `migrate` | aplikuje vše, co chybí |
| `migrate library 0002` | posune appku na stav po `0002`, i **dozadu** |
| `migrate library zero` | odvolá všechny migrace appky (smaže její tabulky) |
| `migrate --plan` | co by `migrate` udělal |
| `migrate --check` | skončí kódem 1, když jsou neaplikované migrace |
| `showmigrations` | seznam migrací, `[X]` aplikovaná, `[ ]` ne |
| `sqlmigrate library 0002` | SQL migrace (pro SQLite, PostgreSQL by vypsal jiné) |

Všechny se spouští přes `uv run manage.py …` ze složky projektu.

## Co je v souboru migrace

```python
# library/migrations/0002_book_pages.py
class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),     # na čem stavím
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="pages",
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]
```

- **`dependencies`**: pořadí migrací není dané číslem v názvu, ale tímhle
  seznamem. Migrace tvoří graf. Migrace s `ForeignKey` na jinou appku
  závisí i na její migraci.
- **`operations`**: `CreateModel`, `AddField`, `RemoveField`, `AlterField`,
  `RenameField`, `DeleteModel`, `AddConstraint`, `RunPython`, `RunSQL` …
  Většina jde automaticky i obráceně, proto funguje návrat zpět.
- Soubor je čitelný a **má se číst**. Před commitem zkontroluj, že dělá to,
  co čekáš, zvlášť u přejmenování a mazání.

## Situace z praxe

### Nové povinné pole do tabulky, která už má data

```
$ uv run manage.py makemigrations
It is impossible to add a non-nullable field 'pages' to book without
specifying a default. This is because the database needs something to
populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
```

Existující řádky musí dostat nějakou hodnotu. Možnosti:

| Volba | Kdy |
|---|---|
| `1)` a zadat hodnotu (`100`, `""`, `timezone.now`) | jednorázová hodnota jen pro staré řádky, v modelu `default` nebude |
| `2)` a doplnit `default=…` do modelu | i nové záznamy mají mít výchozí hodnotu |
| pole jako `null=True` | hodnota u starých řádků opravdu není známá |
| `null=True` → datová migrace → `null=False` | správné hodnoty se dají spočítat, viz [Datová migrace](#datová-migrace-runpython) |

U `--noinput` (v CI) Django místo dotazu jen vypíše chybu
`it is impossible to add a non-nullable field … without specifying a default`.

### Přejmenování pole

```
$ uv run manage.py makemigrations
Was book.pages renamed to book.page_count (a PositiveIntegerField)? [y/N]
```

- **`y`** → `RenameField`, data zůstanou.
- **`N`** (nebo `--noinput`) → `RemoveField` + `AddField`, tedy **sloupec
  i data zmizí** a vznikne nový prázdný.

Django přejmenování jen odhaduje. Když najednou změníš název i typ, nezeptá
se a vygeneruje smazání a přidání. Proto přejmenovávej samostatně
a soubor migrace si přečti.

### Datová migrace (`RunPython`)

Když je potřeba změnit **data**, ne strukturu: přepočítat sloupec, naplnit
nové pole, opravit hodnoty.

```bash
uv run manage.py makemigrations --empty library -n fill_slugs
```

```python
from django.db import migrations
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    Book = apps.get_model("library", "Book")   # historická verze modelu!
    for book in Book.objects.filter(slug=""):
        book.slug = slugify(book.title)
        book.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("library", "0004_book_slug")]

    operations = [
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
```

- **Model ber přes `apps.get_model()`, nikdy `from .models import Book`.**
  Migrace musí fungovat i za rok, kdy už `models.py` vypadá jinak.
  `apps.get_model` vrátí model ve stavu odpovídajícím této migraci.
  Vlastní metody modelu tam nejsou, jen pole.
- Druhý argument je funkce pro návrat zpět. `RunPython.noop` = „zpět nic
  nedělej“. Bez něj návrat přes tuto migraci nejde.

### Konflikt po merge: dvě migrace se stejným číslem

Ty i kolega jste ve svých větvích vytvořili `0004_…`:

```
$ uv run manage.py migrate
CommandError: Conflicting migrations detected; multiple leaf nodes in the
migration graph: (0004_book_note, 0004_book_isbn in library).
To fix them run 'python manage.py makemigrations --merge'
```

```bash
uv run manage.py makemigrations --merge
# Created new merge migration .../0005_merge_0004_book_note_0004_book_isbn.py
uv run manage.py migrate
```

Merge migrace jen spojí obě větve (`dependencies` na obě, `operations`
prázdné). Když obě větve mění stejné pole, Django se zeptá a je potřeba
rozhodnout ručně. Alternativa: smazat svou neaplikovanou `0004`,
stáhnout kolegovu, `migrate` a pak znovu `makemigrations`.

### Návrat zpět

```bash
uv run manage.py showmigrations library
#  [X] 0001_initial
#  [X] 0002_book_pages
#  [X] 0003_rename_pages_book_page_count

uv run manage.py migrate library 0001
#  Unapplying library.0003_rename_pages_book_page_count... OK
#  Unapplying library.0002_book_pages... OK
```

Po návratu migrace v databázi neplatí, ale soubory zůstávají. Pokud změnu
nechceš vůbec, smaž soubory a vrať `models.py`. Mazání sloupce zpět
neobnoví data, jen sloupec.

### Lokálně se to celé zamotalo

Jen **lokálně a u migrací, které ještě nejsou v gitu / na serveru**:

```bash
rm db.sqlite3                          # smaže celou lokální DB i s daty
rm library/migrations/000[2-9]*.py     # smaže tvoje nové migrace
uv run manage.py makemigrations
uv run manage.py migrate
```

## Pravidla pro tým

1. **Migrace se commitují** spolu se změnou `models.py`, v jednom commitu.
2. **Aplikovanou migraci, která už je ve sdílené větvi, neupravuj ani
   nemaž.** Kolegové a produkce ji už mají v `django_migrations` a tvoje
   úprava se k nim nikdy nedostane. Oprava = nová migrace.
3. Neaplikované migrace ve své větvi klidně smaž a vygeneruj znovu, ať
   nevzniká `0004`, `0005`, `0006` pro jednu změnu.
4. V CI se pouští `makemigrations --check`. Spadne, když někdo změnil
   model a zapomněl migraci.
5. Migrace se nelinkují ani neformátují ručně. Ruff je v tomto repu
   vynechává (`extend-exclude = ["*/migrations/*"]`).

## SQLite vs. PostgreSQL

- `sqlmigrate` vypíše SQL pro **aktuální** databázi. Na PostgreSQL by byl
  jiný (`bigint GENERATED BY DEFAULT AS IDENTITY` místo `AUTOINCREMENT`).
- SQLite neumí většinu `ALTER TABLE`. Django proto změnu typu nebo omezení
  provádí tak, že vytvoří novou tabulku, překopíruje data a starou smaže.
  Funguje to, ale u velké tabulky v PostgreSQL by šlo o jednoduchý `ALTER`.
- V PostgreSQL běží každá migrace v transakci. Když spadne uprostřed,
  nic se nezmění. SQLite to má podobně, MySQL ne.

## Časté chyby

| Příznak | Příčina |
|---|---|
| `OperationalError: no such table: library_book` | chybí `migrate`, nebo appka není v `INSTALLED_APPS` |
| `No changes detected` po úpravě modelu | appka není v `INSTALLED_APPS`, nebo soubor není uložený |
| `You have N unapplied migration(s)` při `runserver` | po `pull` chybí `migrate` |
| `OperationalError: no such column: library_book.pages` | model změněný bez migrace, nebo migrace vytvořená, ale ne aplikovaná |
| `Conflicting migrations detected; multiple leaf nodes` | dvě větve se stejným číslem, `makemigrations --merge` |
| po přejmenování zmizela data | na otázku `Was … renamed …?` odpověď `N`, vzniklo smazání + přidání |
| `ImportError` / chyba v migraci za půl roku | datová migrace importuje model z `models.py` místo `apps.get_model` |
| `IntegrityError: NOT NULL constraint failed` při `migrate` | data v tabulce nesplňují nové omezení |
| `IrreversibleError: Operation <RunPython …> … is not reversible` při návratu | `RunPython` bez funkce pro návrat, doplň `RunPython.noop` |
