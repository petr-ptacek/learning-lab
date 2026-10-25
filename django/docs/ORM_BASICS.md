# ORM — práce s daty (CRUD)

Jak data vytvořit, načíst, upravit a smazat přes Django ORM. To jsou
operace, které v praxi píšeš každý den. Výstupy jsou ověřené na Django 6.1
v `manage.py shell`. Složitější dotazy (`Q`, `F`, `annotate`, agregace,
výkon) jsou v konceptu 04.

Související: [`MODELS_AND_FIELDS.md`](MODELS_AND_FIELDS.md),
[`MIGRATIONS.md`](MIGRATIONS.md), [`DATABASE.md`](DATABASE.md).

Příklady používají model `Book` z [`MODELS_AND_FIELDS.md`](MODELS_AND_FIELDS.md).

## Od seznamu v paměti k ORM

Co jsi v konceptu 02 psal ručně nad `BOOKS`, dělá ORM nad databází:

| Koncept 02 (`BOOKS` list) | ORM |
|---|---|
| `BOOKS` | `Book.objects.all()` |
| `next((b for b in BOOKS if b["id"] == 3), None)` | `Book.objects.filter(pk=3).first()` |
| `[b for b in BOOKS if b["year"] >= 1930]` | `Book.objects.filter(year__gte=1930)` |
| `max(... default=0) + 1` | nic, `id` přidělí databáze |
| `BOOKS.append(book)` | `Book.objects.create(...)` |
| `book.update({...})` | `book.title = ...; book.save()` |
| `BOOKS.remove(book)` | `book.delete()` |
| `len(BOOKS)` | `Book.objects.count()` |
| `book["title"]` | `book.title` (atribut, ne klíč) |

Data navíc přežijí restart serveru a víc procesů vidí stejná data.

## Shell

```bash
uv run manage.py shell
```

Od Django 5.2 shell **sám importuje všechny modely** a pár užitečných věcí.
Při startu to vypíše:

```
13 objects imported automatically (use -v 2 for details).
```

`Book` je tedy hned k dispozici, bez `from library.models import Book`.
Ve skriptech a views importovat musíš.

Jeden příkaz bez interaktivního režimu:

```bash
uv run manage.py shell -c "print(Book.objects.count())"
```

## `objects` a QuerySet

`Book.objects` je **manager**, vstupní bod pro dotazy na tabulku. Většina
metod vrací **QuerySet**: popis dotazu, který se pošle do databáze až ve
chvíli, kdy výsledek opravdu potřebuješ.

```python
qs = Book.objects.filter(author="Karel Čapek")   # žádný SQL dotaz zatím
qs = qs.order_by("year")                         # pořád žádný
for book in qs:                                  # ← teď se pošle SELECT
    print(book)

print(qs.query)   # vypíše SQL, které se pošle
```

Obdoba builderu dotazů (Prisma, Knex): řetězíš podmínky a dotaz proběhne
až při čtení. Kdy přesně se QuerySet vyhodnotí a proč na tom záleží, je
v konceptu 04.

## Create — vytvoření

```python
book = Book.objects.create(title="Krakatit", author="Karel Čapek", year=1924)
book.pk            # 1, ID přidělila databáze
book.created_at    # datetime(2026, 10, 25, 18, 31, 22, tzinfo=UTC)
book.genre         # 'novel', výchozí hodnota z modelu
```

Ve dvou krocích, když potřebuješ objekt před uložením upravit:

```python
book = Book(title="R.U.R.", author="Karel Čapek", year=1920)
book.pk            # None, ještě není v DB
book.save()        # INSERT
book.pk            # 2
```

Hromadně, jedním dotazem:

```python
Book.objects.bulk_create([
    Book(title="Babička", author="Božena Němcová", year=1855),
    Book(title="Saturnin", author="Zdeněk Jirotka", year=1942),
])
```

`bulk_create` nevolá `save()` a u SQLite / PostgreSQL vrátí objekty
i s `pk`.

**`create()` ani `save()` data nevalidují** (kromě omezení přímo
v databázi). U dat od uživatele zavolej nejdřív `full_clean()`, viz
[Validace](MODELS_AND_FIELDS.md#validace-co-hlídá-databáze-a-co-django).

## Read — čtení

### Jeden záznam

```python
Book.objects.get(pk=1)                  # <Book: Krakatit (1924)>
Book.objects.get(title="Krakatit")      # podle čehokoliv, co je jednoznačné
```

`get()` **vyhodí výjimku**, když nesedí přesně jeden řádek:

```python
Book.objects.get(pk=99)
# Book.DoesNotExist: Book matching query does not exist.

Book.objects.get(author="Karel Čapek")
# Book.MultipleObjectsReturned: get() returned more than one Book -- it returned 2!
```

Bez výjimky, `None` když nic není:

```python
Book.objects.filter(pk=99).first()      # None
```

Ve view podle toho, co vracíš:

```python
# JSON API (jako v konceptu 02)
try:
    book = Book.objects.get(pk=book_id)
except Book.DoesNotExist:
    return JsonResponse({"error": "Kniha nenalezena"}, status=404)

# HTML stránky: vyhodí Http404, Django vrátí HTML 404 stránku
from django.shortcuts import get_object_or_404
book = get_object_or_404(Book, pk=book_id)
```

### Víc záznamů

```python
Book.objects.all()                              # všechny
Book.objects.filter(author="Karel Čapek")       # WHERE author = ...
Book.objects.exclude(available=False)           # WHERE NOT ...
Book.objects.filter(author="Karel Čapek", year__gte=1930)   # AND
Book.objects.filter(...).filter(...)            # taky AND
Book.objects.order_by("-year", "title")         # "-" = sestupně
Book.objects.all()[:10]                         # LIMIT 10
Book.objects.all()[10:20]                       # OFFSET 10 LIMIT 10 (stránkování)
```

Výsledek se chová jako seznam: `for`, `len()`, `list()`, indexování.
Záporný index (`qs[-1]`) nejde, místo něj `qs.last()`.

### Lookupy: podmínky v `filter()`

Syntaxe `pole__lookup=hodnota` (dvě podtržítka):

| Lookup | SQL zhruba | Příklad |
|---|---|---|
| (nic) / `exact` | `=` | `filter(year=1924)` |
| `iexact` | `=` bez velikosti písmen | `filter(author__iexact="karel čapek")` |
| `contains` / `icontains` | `LIKE '%…%'` | `filter(title__icontains="mlok")` |
| `startswith` / `istartswith` | `LIKE '…%'` | `filter(title__startswith="Vál")` |
| `gt`, `gte`, `lt`, `lte` | `>`, `>=`, `<`, `<=` | `filter(year__gte=1930)` |
| `range` | `BETWEEN` | `filter(year__range=(1900, 1940))` |
| `in` | `IN (…)` | `filter(pk__in=[1, 3, 5])` |
| `isnull` | `IS NULL` | `filter(price__isnull=True)` |
| `year`, `month`, `date` | část data | `filter(created_at__year=2026)` |

Je to stejný nápad jako filtry v konceptu 02 (`?author=…&year_from=…`),
jen je za tebe provede databáze. `OR`, porovnání dvou sloupců a další jsou
v konceptu 04 (`Q`, `F`).

**SQLite a diakritika:** `icontains` / `iexact` v SQLite ignorují velikost
písmen **jen u ASCII znaků**. Ověřeno:

```python
Book.objects.filter(author__icontains="KAREL")   # najde "Karel Čapek"  ✅
Book.objects.filter(author__icontains="čapek")   # NENAJDE "Karel Čapek" ❌ (č ≠ Č)
Book.objects.filter(author__icontains="Čapek")   # najde                 ✅
```

PostgreSQL porovnává správně i `č` / `Č`. V konceptu 02 jsi to řešil
přes `casefold()` v Pythonu. S databází to v SQLite takhle nejde, pro
učení to ale nevadí, jen se nediv.

### Počet, existence, jen některé sloupce

```python
Book.objects.count()                                    # SELECT COUNT(*)
Book.objects.filter(author="Karel Čapek").exists()      # True / False, nejrychlejší

Book.objects.values("title", "year")[:2]
# <QuerySet [{'title': 'Babička', 'year': 1855}, {'title': 'Krakatit', 'year': 1924}]>

Book.objects.values_list("title", flat=True)
# <QuerySet ['Babička', 'Krakatit', 'R.U.R.']>
```

`count()` a `exists()` místo `len(qs)` a `if qs:`, když nepotřebuješ
samotná data. Databáze pak nemusí vracet řádky.

`values()` vrací slovníky, ale QuerySet není `list` ani `dict`, takže ho
`JsonResponse` přímo nepřijme. Zabal ho: `{"results": list(qs.values())}`. V API se ale obvykle píše
vlastní `serialize_book(book)` (jako v konceptu 02) nebo DRF serializer.

## Update — úprava

Jeden objekt:

```python
book = Book.objects.get(pk=1)
book.title = "Krakatit (2. vydání)"
book.save()                              # UPDATE všech sloupců
book.save(update_fields=["title"])       # UPDATE jen title, rychlejší a bezpečnější
```

Hromadně, jedním dotazem:

```python
Book.objects.filter(author="Karel Čapek").update(available=False)   # vrátí 2 (počet řádků)
```

`QuerySet.update()` **obchází `save()`**: neprojde vlastní logikou
v `save()`, nespustí signály a **nezmění `auto_now` pole**
(`updated_at`).

Objekt v paměti se po změně v DB sám neaktualizuje:

```python
book.available                # True  (stará hodnota v Pythonu)
book.refresh_from_db()
book.available                # False
```

## Delete — smazání

```python
book.delete()                                # (1, {'library.Book': 1})
Book.objects.filter(available=False).delete()
```

Vrací počet smazaných řádků celkem a po modelech. Čísla se liší, když
mazání strhne i závislé záznamy (`on_delete=CASCADE`, koncept 05).

`Book.objects.delete()` neexistuje, abys omylem nesmazal celou tabulku.
Musí to být `Book.objects.all().delete()`.

## Najdi, nebo vytvoř

```python
book, created = Book.objects.get_or_create(
    title="Babička",
    defaults={"author": "Božena Němcová", "year": 1855},
)
# (<Book: Babička (1855)>, True)    poprvé vytvoří
# (<Book: Babička (1855)>, False)   podruhé najde, defaults ignoruje

book, created = Book.objects.update_or_create(
    isbn="9788000000000",
    defaults={"title": "Nový název"},
)
```

Vrací **dvojici** `(objekt, vytvořeno)`. Častá chyba je
`book = Book.objects.get_or_create(...)`, pak je v `book` celá n-tice.
Podle argumentů mimo `defaults` se hledá, `defaults` se použije jen při
vytváření (u `update_or_create` i při úpravě).

## Kolik dotazů to posílá

```python
from django.db import connection, reset_queries
from django.conf import settings

reset_queries()
list(Book.objects.all())
len(connection.queries)        # 1  (funguje jen při DEBUG = True)
connection.queries[-1]["sql"]
```

V shellu je `connection` i `reset_queries` importované automaticky. Proč
na počtu dotazů záleží (N+1 problém), je v konceptu 05.

## Časté chyby

| Příznak | Příčina |
|---|---|
| `NameError: name 'Book' is not defined` ve view | chybí `from .models import Book` (shell importuje sám, view ne) |
| `Book.DoesNotExist` → 500 | `get()` bez `try` / `except`, nebo použij `filter().first()` |
| `MultipleObjectsReturned` | `get()` podle pole, které není unikátní |
| `AttributeError: 'Manager' object has no attribute 'delete'` | `Book.objects.delete()`, správně `Book.objects.all().delete()` |
| `TypeError: 'Book' object is not subscriptable` | `book["title"]` místo `book.title` |
| `TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False.` | `JsonResponse(qs.values())`, QuerySet není `dict`; zabal do objektu: `{"results": list(qs.values())}` |
| `ValueError: Negative indexing is not supported.` | `qs[-1]`, správně `qs.last()` |
| změna se neuložila | chybí `save()` |
| `updated_at` se nezměnil | `QuerySet.update()` obchází `auto_now` |
| `AttributeError: 'tuple' object has no attribute 'title'` | `book = ...get_or_create(...)`, vrací dvojici `(objekt, created)` |
| `FieldError: Cannot resolve keyword 'name' into field. Choices are: …` | překlep v názvu pole ve `filter()`, Django vypíše dostupná pole |
