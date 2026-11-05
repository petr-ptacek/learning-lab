# 06 — Vnořená `Meta` a konfigurace třídou

Každý Django model může mít `class Meta:` s nastavením (`ordering`,
`verbose_name`, `abstract`, …). Tady si napíšeš základ, který tu `Meta`
čte, a uvidíš, co se s ní děje při dědění. Žádná magie: `Meta` je jen
atribut třídy, takže se hledá stejně jako `role` ve cvičení 01.

Teorie: [`docs/CLASSES_AND_INSTANCES.md`](../../../docs/CLASSES_AND_INSTANCES.md)
(vnořená třída, hledání atributů) a
[`docs/CLASS_CREATION_AND_METACLASSES.md`](../../../docs/CLASS_CREATION_AND_METACLASSES.md)
(jak `Meta` čte Django).

## Požadavky

- Základní třída `Model`:
  - `__init__(self, **fields)` — každý pojmenovaný argument uloží jako
    atribut instance (`setattr`),
  - `__repr__` → `Book('Švejk')` (jméno třídy + `title`),
  - `@classmethod get_option(cls, name, default=None)` — vrátí
    `cls.Meta.<name>`, když třída `Meta` má a v ní ta volba je.
    Jinak `default`. Nápověda: dvakrát `getattr` s výchozí hodnotou.
  - `@classmethod verbose_name(cls)` — volba `verbose_name`, výchozí
    je jméno třídy malými písmeny,
  - `@classmethod sort(cls, items)` — **nový** seznam seřazený podle
    `Meta.ordering`: seznam jmen polí, `"-year"` znamená sestupně.
    Bez `ordering` vrátí položky v původním pořadí.
    Nápověda: `sort` je stabilní. Když řadíš postupně od **posledního**
    pole k prvnímu, výsledek je seřazený podle všech.
- `Book(Model)` s `Meta`: `ordering = ["author", "-year"]`,
  `verbose_name = "kniha"`.
- `Author(Model)` bez `Meta`.
- **Předpověď:** napiš do komentáře, co vypíše, pak spusť.

  ```python
  class Ebook(Book):
      pass


  print(Ebook.get_option("ordering"), Ebook.verbose_name())
  print(Ebook.Meta is Book.Meta, "Meta" in vars(Ebook))


  class Ebook2(Book):
      class Meta:
          verbose_name = "e-kniha"


  print(Ebook2.get_option("ordering"), Ebook2.verbose_name())


  class Ebook3(Book):
      class Meta(Book.Meta):
          verbose_name = "e-kniha"


  print(Ebook3.get_option("ordering"), Ebook3.verbose_name())
  print(Book.verbose_name())
  ```

  Proč `Ebook` „má“ `Meta`, i když žádnou nenapsal? Proč ji `Ebook2`
  ztratil? Co je `class Meta(Book.Meta)` za zápis?

> Django dědění `Meta` řeší vlastními pravidly. U abstraktního rodiče
> se `Meta` zdědí, pokud ji potomek nenapíše. U konkrétního rodiče se
> nezdědí skoro nic. Základ, na kterém to stojí, je ale přesně tohle
> hledání atributů.

### Příklady vstup/výstup

```python
books = [
    Book(title="Proměna", author="Kafka", year=1915),
    Book(title="Švejk", author="Hašek", year=1923),
    Book(title="Proces", author="Kafka", year=1925),
    Book(title="Saturnin", author="Jirotka", year=1942),
    Book(title="Zámek", author="Kafka", year=1926),
]
```

| Kód                                    | Výsledek                                   |
|----------------------------------------|--------------------------------------------|
| `Book.get_option("ordering")`          | `['author', '-year']`                      |
| `Book.get_option("db_table", "books")` | `'books'` (v `Meta` není)                  |
| `Author.get_option("ordering", [])`    | `[]` (`Meta` vůbec nemá)                   |
| `Author.get_option("verbose_name")`    | `None`                                     |
| `Book.verbose_name(), Author.verbose_name()` | `('kniha', 'author')`                |
| `books[0].Meta.verbose_name`           | `'kniha'` (přes instanci taky)             |
| `Book.sort(books)`                     | `[Book('Švejk'), Book('Saturnin'), Book('Zámek'), Book('Proces'), Book('Proměna')]` |
| `Author.sort(books)`                   | původní pořadí: `[Book('Proměna'), Book('Švejk'), Book('Proces'), Book('Saturnin'), Book('Zámek')]` |
| `Book.sort([])`                        | `[]`                                       |
| `books` po `Book.sort(books)`          | nezměněný seznam                           |

| Předpověď                                    | Výsledek                       |
|----------------------------------------------|--------------------------------|
| `Ebook.get_option("ordering"), Ebook.verbose_name()` | `(['author', '-year'], 'kniha')` |
| `Ebook.Meta is Book.Meta, "Meta" in vars(Ebook)` | `(True, False)`            |
| `Ebook2.get_option("ordering"), Ebook2.verbose_name()` | `(None, 'e-kniha')`  |
| `Ebook3.get_option("ordering"), Ebook3.verbose_name()` | `(['author', '-year'], 'e-kniha')` |
| `Book.verbose_name()`                        | `'kniha'` (rodič beze změny)   |

## Bonus

Volba `abstract = True`: abstraktní model je jen společný základ
(třeba pole `created` pro všechny), jeho instance vytvořit nejde.

- `@classmethod is_abstract(cls)` — `True` jen tehdy, když `abstract`
  je ve **vlastní** `Meta` té třídy.
- `__init__` abstraktního modelu vyhodí
  `TypeError("<Jméno> je abstraktní model")`.
- **Předpověď:** proč nestačí `cls.get_option("abstract", False)`?
  Zkus obě verze na třídách níže. Nápověda: `vars(cls)` vs. hledání
  atributu přes rodiče.

  ```python
  class TimestampedModel(Model):
      class Meta:
          abstract = True
          ordering = ["-created"]


  class Article(TimestampedModel):
      pass


  class Comment(TimestampedModel):
      class Meta(TimestampedModel.Meta):
          abstract = False
  ```

### Příklady vstup/výstup (bonus)

| Kód                                                      | Výsledek                               |
|----------------------------------------------------------|----------------------------------------|
| `TimestampedModel.is_abstract()`                         | `True`                                 |
| `Article.is_abstract(), Comment.is_abstract()`           | `(False, False)`                       |
| `Model.is_abstract()`                                    | `False`                                |
| naivně přes `get_option`: `Article`                      | `True` (špatně, zdědil rodičovu `Meta`) |
| `"Meta" in vars(Article), hasattr(Article, "Meta")`      | `(False, True)`                        |
| `Article.get_option("ordering")`                         | `['-created']` (ostatní volby se dědí dál) |
| `Article(title="Ahoj", created=2)`                       | `Article('Ahoj')`                      |
| `TimestampedModel(title="x")`                            | `TypeError: TimestampedModel je abstraktní model` |
