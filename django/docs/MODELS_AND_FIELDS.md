# Modely a pole — praktický přehled

Jak napsat model, jaká pole se v praxi používají a co znamenají jejich
volby. Výběr z oficiální dokumentace, ověřený na Django 6.1 se SQLite.
Kde se PostgreSQL chová jinak, je to u daného místa uvedené.

Související: [`MIGRATIONS.md`](MIGRATIONS.md) (jak se model dostane do
databáze), [`ORM_BASICS.md`](ORM_BASICS.md) (jak s daty pracovat),
[`DATABASE.md`](DATABASE.md) (SQLite, PostgreSQL, jak se do DB podívat).

## Model v jedné ukázce

```python
# library/models.py
from django.db import models


class Book(models.Model):
    class Genre(models.TextChoices):
        NOVEL = "novel", "Román"
        DRAMA = "drama", "Drama"
        POETRY = "poetry", "Poezie"

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=20, choices=Genre, default=Genre.NOVEL)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    note = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(year__gte=1450), name="book_year_gte_1450"
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"
```

Z toho Django vygeneruje tabulku `library_book` (`<appka>_<model malými
písmeny>`):

```sql
CREATE TABLE "library_book" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "title" varchar(200) NOT NULL,
  "author" varchar(100) NOT NULL,
  "year" smallint unsigned NOT NULL CHECK ("year" >= 0),
  "genre" varchar(20) NOT NULL,
  "isbn" varchar(13) NULL UNIQUE,
  "price" decimal NULL,
  ...
  CONSTRAINT "book_year_gte_1450" CHECK ("year" >= 1450)
);
```

Výpis SQL pro libovolnou migraci: `uv run manage.py sqlmigrate library 0001`.

**Srovnání s FE:** model je TS `interface` + popis, jak ho uložit. Pole
jsou typy sloupců, volby (`null`, `max_length`, `unique`) jsou omezení
v databázi a zároveň pravidla validace.

```ts
interface Book {
  id: number
  title: string           // CharField(max_length=200)
  isbn: string | null     // null=True
  note: string            // TextField(blank=True): prázdný string, ne null
  genre: 'novel' | 'drama' | 'poetry'   // choices
  createdAt: string       // auto_now_add
}
```

## Primární klíč `id`

Nemusíš ho psát. Django přidá `id = models.BigAutoField(primary_key=True)`
samo. Od Django 6.0 je výchozí `BigAutoField` (64bit), proto už
`settings.py` ani `apps.py` nové projekty `DEFAULT_AUTO_FIELD` neobsahují.
Ve starších projektech v práci ho uvidíš nastavený ručně.

- `book.pk` je alias pro primární klíč, ať se jmenuje jakkoliv.
  V kódu se používá `pk`, ne `id`.
- Vlastní primární klíč: `models.UUIDField(primary_key=True, default=uuid.uuid4,
  editable=False)`. Používá se, když ID nemá být uhodnutelné v URL.

## Typy polí, které potkáš nejčastěji

| Pole | Python typ | Kdy | Poznámka |
|---|---|---|---|
| `CharField(max_length=…)` | `str` | krátký text: jméno, název, kód | `max_length` uváděj vždy, viz pod tabulkou |
| `TextField()` | `str` | dlouhý text: popis, poznámka | bez limitu |
| `IntegerField()` | `int` | celé číslo | |
| `PositiveIntegerField()` / `PositiveSmallIntegerField()` | `int` | počet, rok, stránky | DB přidá `CHECK (>= 0)` |
| `BigIntegerField()` | `int` | velká čísla | |
| `DecimalField(max_digits, decimal_places)` | `Decimal` | **peníze**, přesná čísla | nikdy ne `FloatField` pro peníze |
| `FloatField()` | `float` | měření, kde nevadí nepřesnost | |
| `BooleanField(default=…)` | `bool` | ano/ne | vždy s `default` |
| `DateField()` | `date` | datum bez času | narozeniny, datum vydání |
| `DateTimeField()` | `datetime` | okamžik v čase | s `USE_TZ = True` v UTC, viz [`TIME_AND_TIMEZONES.md`](TIME_AND_TIMEZONES.md) |
| `DurationField()` | `timedelta` | délka trvání | |
| `EmailField()` / `URLField()` / `SlugField()` | `str` | `CharField` s validací formátu | `SlugField` pro URL (`valka-s-mloky`) |
| `UUIDField()` | `UUID` | neuhodnutelné ID, veřejné tokeny | |
| `JSONField()` | `dict` / `list` | volná struktura, nastavení | nepoužívej místo normálních sloupců |
| `FileField()` / `ImageField()` | soubor | nahrané soubory | v DB je jen cesta, soubor na disku / v S3 |
| `ForeignKey`, `ManyToManyField`, `OneToOneField` | | vztahy | koncept 05 |

**`CharField` bez `max_length`:** v SQLite a PostgreSQL to dnes Django
dovolí (neomezený `varchar`), v MySQL a starších verzích Djanga je to
chyba `fields.E120`. Limit je ale i dokumentace dat a validace vstupu,
proto ho uváděj. Na dlouhý text bez limitu je `TextField`.

Kompletní seznam:
[Model field reference](https://docs.djangoproject.com/en/6.1/ref/models/fields/).

## Volby polí

| Volba | Kde platí | Co dělá |
|---|---|---|
| `null=True` | **databáze** | sloupec smí být `NULL` |
| `blank=True` | **validace** (formuláře, admin, DRF, `full_clean`) | pole smí zůstat prázdné |
| `default=…` | Python | hodnota, když ji nezadáš (hodnota nebo funkce bez závorek: `default=timezone.now`) |
| `db_default=…` | databáze | výchozí hodnota přímo v DB (`DEFAULT` v SQL), platí i pro INSERT mimo Django |
| `unique=True` | databáze | `UNIQUE`, duplicita vyhodí `IntegrityError` |
| `db_index=True` | databáze | index pro rychlé hledání podle sloupce |
| `choices=…` | validace + admin | povolené hodnoty, viz níže |
| `max_length=…` | DB (`varchar(n)`) + validace | |
| `verbose_name="…"` | admin, formuláře | lidský název pole |
| `help_text="…"` | admin, formuláře | nápověda |
| `editable=False` | admin, formuláře | pole se nezobrazí k úpravě |
| `validators=[…]` | validace | vlastní kontroly, viz [Validace](#validace-co-hlídá-databáze-a-co-django) |

### `null` vs. `blank`: nejčastější zmatek

| Zápis | Prázdná hodnota v DB | Typické použití |
|---|---|---|
| (nic) | povinné | `title` |
| `blank=True` | `""` (prázdný string) | **textová** nepovinná pole: `note`, `subtitle` |
| `null=True, blank=True` | `NULL` | **netextová** nepovinná pole: `price`, `published_at`, `ForeignKey` |
| `null=True` bez `blank` | `NULL`, ale formulář pole vyžaduje | výjimečně |

**Text nikdy `null=True`** (s výjimkou `unique=True`, viz `isbn` výše).
Jinak má „prázdno“ dvě podoby, `""` a `NULL`, a každý filtr musí počítat
s oběma. Ruff to hlídá pravidlem `DJ001`. U `unique` je `NULL` nutný,
protože víc řádků s `""` by porušilo unikátnost, kdežto `NULL` se za
duplicitu nepočítá.

### `choices` — výčet hodnot

```python
class Genre(models.TextChoices):
    NOVEL = "novel", "Román"      # hodnota v DB, popisek pro lidi
    DRAMA = "drama", "Drama"

genre = models.CharField(max_length=20, choices=Genre, default=Genre.NOVEL)
```

```python
book.genre                 # 'novel'   (hodnota v DB)
book.get_genre_display()   # 'Román'   (popisek, metoda vzniká automaticky)
Book.Genre.NOVEL == "novel"   # True, TextChoices je str
Book.Genre.choices         # [('novel', 'Román'), ('drama', 'Drama'), ...]
```

- Pro čísla je `models.IntegerChoices`.
- V kódu porovnávej s `Book.Genre.DRAMA`, ne se stringem `"drama"`. Překlep
  pak skončí chybou, ne tichým nesouladem.
- **Databáze `choices` nehlídá.** `Book(genre="nesmysl").save()` projde.
  Zachytí to až validace (`full_clean`, formulář, DRF serializer).
- Srovnání s TS: `enum` / union typ `'novel' | 'drama'`.

### `auto_now_add` a `auto_now`

```python
created_at = models.DateTimeField(auto_now_add=True)   # nastaví se při vytvoření
updated_at = models.DateTimeField(auto_now=True)       # při každém save()
```

Obě pole jsou automaticky `editable=False`. Pozor:
`Book.objects.filter(...).update(...)` volá rovnou SQL `UPDATE` bez
`save()`, takže `updated_at` **nezmění**.

## `Meta` — nastavení celého modelu

```python
class Meta:
    ordering = ["-created_at", "title"]   # výchozí řazení, "-" = sestupně
    verbose_name = "kniha"
    verbose_name_plural = "knihy"          # jinak admin napíše "Books" / "knihas"
    constraints = [...]                    # viz níže
    indexes = [models.Index(fields=["author", "year"])]
    db_table = "books"                     # vlastní název tabulky (u legacy DB)
```

`ordering` se uplatní u každého dotazu bez vlastního `order_by()`.
U velkých tabulek může zbytečně zpomalovat, v praxi se proto často
nenastavuje a řadí se explicitně v dotazu (koncept 04).

### Omezení v databázi (`constraints`)

```python
constraints = [
    models.UniqueConstraint(fields=["title", "author"], name="unique_book_per_author"),
    models.CheckConstraint(condition=models.Q(year__gte=1450), name="book_year_gte_1450"),
]
```

- `UniqueConstraint`: unikátní kombinace víc sloupců. Pro jeden sloupec
  stačí `unique=True`.
- `CheckConstraint`: libovolná podmínka. Parametr se jmenuje
  **`condition`**. Ve starších projektech uvidíš `check=`, ten byl
  v Django 6.0 odstraněn.
- `name` je povinné a musí být unikátní v celé databázi. Konvence:
  `<model>_<co>`.
- Porušení vyhodí `IntegrityError` už při `save()`, i když nevoláš
  validaci. Je to poslední pojistka, kterou nikdo neobejde.

## `__str__` a vlastní metody

```python
def __str__(self):
    return f"{self.title} ({self.year})"
```

Používá se v adminu, v shellu (`<Book: Krakatit (1924)>`) a v chybových
hláškách. Bez něj uvidíš `<Book: Book object (1)>`. Ruff to hlídá jako
`DJ008`.

Na model patří i logika, která se týká jedné instance. Obdoba
computed / getteru v TS třídě:

```python
@property
def is_classic(self):
    return self.year < 1950

def mark_unavailable(self):
    self.available = False
    self.save(update_fields=["available"])
```

## Validace: co hlídá databáze a co Django

Tohle je **nejčastější překvapení**: `save()` model **nevaliduje**.

| Kontrola | `save()` / `create()` | `full_clean()` |
|---|---|---|
| `null=False` | ✅ DB: `IntegrityError: NOT NULL constraint failed` | ✅ |
| `unique`, `UniqueConstraint`, `CheckConstraint` | ✅ DB: `IntegrityError` | ✅ |
| `PositiveIntegerField` záporné | ✅ DB: `CHECK constraint failed` | ✅ |
| `max_length` | ❌ v SQLite projde i delší text (PostgreSQL ho odmítne) | ✅ |
| `blank=False` (prázdný string) | ❌ `""` se uloží | ✅ |
| `choices` | ❌ uloží cokoliv | ✅ |
| `validators=[…]`, `EmailField` formát | ❌ | ✅ |

```python
from django.core.exceptions import ValidationError

book = Book(title="", author="a", year=1000, genre="bad")
try:
    book.full_clean()
except ValidationError as e:
    e.message_dict
    # {'title': ['This field cannot be blank.'],
    #  'genre': ["Value 'bad' is not a valid choice."],
    #  '__all__': ['Constraint “book_year_gte_1450” is violated.']}
```

`full_clean()` volají za tebe formuláře (`ModelForm`, koncept 08), admin
a DRF `ModelSerializer` (koncept 12). Ve vlastních view nebo skriptech ho
musíš zavolat sám, než uložíš data od uživatele. Tvar `message_dict` je
stejný jako tvoje `{"errors": {...}}` z konceptu 02.

## Časté chyby

| Příznak | Příčina |
|---|---|
| `OperationalError: no such table: library_book` | model je, migrace ne: `makemigrations` + `migrate` |
| `<Book: Book object (1)>` | chybí `__str__` |
| `IntegrityError: NOT NULL constraint failed` | povinné pole bez hodnoty a bez `default` |
| uložila se nevalidní hodnota (`genre="nesmysl"`) | `save()` nevaliduje, chybí `full_clean()` |
| filtr na prázdný text nenajde všechno | text s `null=True`, prázdno je jednou `""`, jindy `NULL` |
| `updated_at` se po `.update()` nezměnil | `QuerySet.update()` obchází `save()` a `auto_now` |
| `TypeError: CheckConstraint.__init__() got an unexpected keyword argument 'check'` | starý zápis, správně `condition=` |
| `default=timezone.now()` dá všem stejný čas | volání při startu serveru, správně bez závorek |
