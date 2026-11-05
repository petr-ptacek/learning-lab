# 10 — `Enum`: pevná sada hodnot

Stav objednávky, priorita, role uživatele: hodnoty, kterých je přesně
daný počet. Místo stringů, ve kterých se snadno udělá překlep, se na
ně v Pythonu používá `enum`. V Djangu je to `models.TextChoices`
u každého pole s výběrem (`status = models.CharField(choices=Status)`).
Enum je přitom obyčejná třída: členy jsou její instance, může mít
metody a property a dědí se z něj.

Teorie: [`docs/ENUMS.md`](../../../docs/ENUMS.md).

## Požadavky

- `OrderStatus(Enum)` se členy `NEW`, `PAID`, `SHIPPED`, `DELIVERED`,
  `CANCELLED`. Hodnoty jsou stejná slova malými písmeny (`"paid"`).
  - property `is_final` → `True` pro `DELIVERED` a `CANCELLED`,
  - metoda `can_change_to(other)` → `True`, když je přechod povolený:
    `NEW` → `PAID` nebo `CANCELLED`, `PAID` → `SHIPPED` nebo
    `CANCELLED`, `SHIPPED` → `DELIVERED`. Z konečných stavů nikam.
    Nápověda: slovník `stav → set povolených stavů` dej **do metody**,
    ne do těla třídy (proč, zjistíš, když to zkusíš).
- `Priority(IntEnum)`: `LOW = 1`, `NORMAL = 2`, `HIGH = 3`, `URGENT = 4`.
- `Order(number, priority=Priority.NORMAL)`:
  - `priority` si uloží jako `Priority`, takže `Order(2, 3)` má
    `Priority.HIGH`,
  - `status` začíná na `OrderStatus.NEW`, `history` je seznam stavů,
    kterými prošla (začíná `[OrderStatus.NEW]`),
  - `change_status(new)` přijme člen **nebo** hodnotu jako string
    (`"paid"`, typicky z formuláře). Povolený přechod provede, zapíše
    do `history` a vrátí `True`. Jinak nic nezmění a vrátí `False`.
    Neplatný string ať vyhodí `ValueError` (stačí nechat probublat
    z enumu).
- **Předpověď:** napiš do komentáře, co vypíše, pak spusť.

  ```python
  print(OrderStatus("paid"), OrderStatus["PAID"])
  print(OrderStatus("paid") is OrderStatus.PAID)
  print(OrderStatus.PAID == "paid", OrderStatus.PAID.value == "paid")
  print(Priority.HIGH == 3, Priority.HIGH > Priority.LOW)
  print(f"stav: {OrderStatus.PAID}, priorita: {Priority.HIGH}")
  ```

  Proč se `OrderStatus.PAID` nerovná `"paid"`, ale `Priority.HIGH` se
  rovná `3`? Co se změní, když `OrderStatus` podědí ze `StrEnum`?
  A co udělá `OrderStatus("PAID")`?

### Příklady vstup/výstup

| Kód                                                       | Výsledek                                        |
|-----------------------------------------------------------|-------------------------------------------------|
| `OrderStatus.PAID.name, OrderStatus.PAID.value`           | `('PAID', 'paid')`                              |
| `OrderStatus("paid")`                                     | `<OrderStatus.PAID: 'paid'>`                    |
| `OrderStatus["PAID"]`                                     | `<OrderStatus.PAID: 'paid'>`                    |
| `OrderStatus("PAID")`                                     | `ValueError: 'PAID' is not a valid OrderStatus` |
| `OrderStatus["paid"]`                                     | `KeyError: 'paid'`                              |
| `[s.value for s in OrderStatus]`                          | `['new', 'paid', 'shipped', 'delivered', 'cancelled']` |
| `OrderStatus.DELIVERED.is_final, OrderStatus.PAID.is_final` | `(True, False)`                               |
| `[s.name for s in OrderStatus if not s.is_final]`         | `['NEW', 'PAID', 'SHIPPED']`                    |
| `OrderStatus.NEW.can_change_to(OrderStatus.PAID)`         | `True`                                          |
| `OrderStatus.NEW.can_change_to(OrderStatus.SHIPPED)`      | `False` (nejdřív zaplatit)                      |
| `OrderStatus.SHIPPED.can_change_to(OrderStatus.CANCELLED)` | `False`                                        |
| `OrderStatus.DELIVERED.can_change_to(OrderStatus.NEW)`    | `False` (konečný stav)                          |
| `OrderStatus.PAID.can_change_to(OrderStatus.PAID)`        | `False`                                         |
| `OrderStatus.PAID < OrderStatus.SHIPPED`                  | `TypeError: '<' not supported between instances of 'OrderStatus' and 'OrderStatus'` |

| Kód                                                       | Výsledek                                        |
|-----------------------------------------------------------|-------------------------------------------------|
| `Priority(4)`                                             | `<Priority.URGENT: 4>`                          |
| `Priority(9)`                                             | `ValueError: 9 is not a valid Priority`         |
| `sorted([Priority.URGENT, Priority.LOW, Priority.HIGH])`  | `[<Priority.LOW: 1>, <Priority.HIGH: 3>, <Priority.URGENT: 4>]` |
| `max(Priority)`                                           | `<Priority.URGENT: 4>`                          |
| `str(Priority.HIGH), str(OrderStatus.PAID)`               | `('3', 'OrderStatus.PAID')`                     |

Postupně za sebou s `o = Order(1)`:

| Kód                                          | Výsledek                                        |
|----------------------------------------------|-------------------------------------------------|
| `o.status, o.priority`                       | `(<OrderStatus.NEW: 'new'>, <Priority.NORMAL: 2>)` |
| `o.change_status(OrderStatus.SHIPPED)`       | `False`, `o.status` zůstává `NEW`               |
| `o.change_status(OrderStatus.PAID)`          | `True`                                          |
| `o.change_status("shipped")`                 | `True` (string z formuláře)                     |
| `o.change_status("delivered")`               | `True`                                          |
| `o.status.is_final`                          | `True`                                          |
| `o.change_status(OrderStatus.CANCELLED)`     | `False`                                         |
| `[s.value for s in o.history]`               | `['new', 'paid', 'shipped', 'delivered']`       |
| `o.change_status("lost")`                    | `ValueError: 'lost' is not a valid OrderStatus` |
| `Order(2, 3).priority`                       | `<Priority.HIGH: 3>`                            |

S `orders = [Order(1, Priority.LOW), Order(2, Priority.URGENT), Order(3), Order(4, Priority.HIGH)]`:

| Kód                                                                   | Výsledek       |
|-----------------------------------------------------------------------|----------------|
| `[o.number for o in sorted(orders, key=lambda o: o.priority, reverse=True)]` | `[2, 4, 3, 1]` |
| `[o.number for o in orders if o.priority >= Priority.HIGH]`           | `[2, 4]`       |

| Předpověď                                              | Výsledek                                     |
|--------------------------------------------------------|----------------------------------------------|
| `OrderStatus("paid"), OrderStatus["PAID"]` (přes `print`) | `OrderStatus.PAID OrderStatus.PAID`        |
| `OrderStatus("paid") is OrderStatus.PAID`              | `True`                                       |
| `OrderStatus.PAID == "paid", OrderStatus.PAID.value == "paid"` | `(False, True)`                      |
| `Priority.HIGH == 3, Priority.HIGH > Priority.LOW`     | `(True, True)`                               |
| f-string                                               | `stav: OrderStatus.PAID, priorita: 3`        |
| s `class OrderStatus(StrEnum)`: `OrderStatus.PAID == "paid"` | `True`, f-string dá `stav: paid`        |

## Bonus

Vlastní mini verze Django `TextChoices`: hodnota pro databázi
a popisek pro člověka v jednom členu.

- Základ `Choices(StrEnum)` bez členů. Podtřídy píšou členy jako
  `DRAFT = "draft", "Koncept"` (hodnota, popisek), nebo jen
  `IN_REVIEW = "in_review"` bez popisku.
  - `__new__(cls, value, label=None)` vyrobí člena:
    `str.__new__(cls, value)`, nastaví `_value_` a uloží popisek.
  - property `label` → uložený popisek, nebo když chybí, popisek ze
    jména: `IN_REVIEW` → `"In Review"` (`_` → mezera, `.title()`),
  - `@classmethod choices(cls)` → seznam `(hodnota, popisek)`,
  - `@classmethod labels(cls)` → seznam popisků.
- `ArticleStatus(Choices)`: `DRAFT = "draft", "Koncept"`,
  `IN_REVIEW = "in_review"`, `PUBLISHED = "published", "Publikováno"`,
  `ARCHIVED = "archived"`.
- `Article(title, status=ArticleStatus.DRAFT)` si stav uloží jako
  `ArticleStatus` (přijme člen i string) a má `get_status_display()`
  → popisek stavu. Stejnou metodu Django přidá každému modelu
  s `choices`.
- **Předpověď:** co udělá tohle? Proč smí `ArticleStatus` dědit
  z `Choices`, ale `Extended` z `ArticleStatus` ne?

  ```python
  class Extended(ArticleStatus):
      DELETED = "deleted"
  ```

> V Djangu se volá `Status.choices` **bez závorek**. Django to dělá
> přes property na vlastní metatřídě (`ChoicesType`), viz
> [`docs/ENUMS.md`](../../../docs/ENUMS.md). Tady stačí classmethod.

### Příklady vstup/výstup (bonus)

| Kód                                                   | Výsledek                                                |
|-------------------------------------------------------|---------------------------------------------------------|
| `ArticleStatus.DRAFT`                                 | `<ArticleStatus.DRAFT: 'draft'>`                        |
| `ArticleStatus.DRAFT.value, ArticleStatus.DRAFT.label` | `('draft', 'Koncept')`                                 |
| `ArticleStatus.IN_REVIEW.label`                       | `'In Review'`                                           |
| `ArticleStatus.ARCHIVED.label`                        | `'Archived'`                                            |
| `ArticleStatus.choices()`                             | `[('draft', 'Koncept'), ('in_review', 'In Review'), ('published', 'Publikováno'), ('archived', 'Archived')]` |
| `ArticleStatus.labels()`                              | `['Koncept', 'In Review', 'Publikováno', 'Archived']`   |
| `ArticleStatus.DRAFT == "draft"`                      | `True`                                                  |
| `ArticleStatus("published").label`                    | `'Publikováno'`                                         |
| `ArticleStatus("Koncept")`                            | `ValueError: 'Koncept' is not a valid ArticleStatus` (hledá podle hodnoty) |
| `list(Choices)`                                       | `[]`                                                    |
| `Article("Ahoj").get_status_display()`                | `'Koncept'`                                             |
| `Article("Ahoj", "in_review").get_status_display()`   | `'In Review'`                                           |
| `Article("Ahoj", ArticleStatus.PUBLISHED).get_status_display()` | `'Publikováno'`                               |
| `Article("Ahoj", "deleted")`                          | `ValueError: 'deleted' is not a valid ArticleStatus`    |
| `class Extended(ArticleStatus): ...`                  | `TypeError: <enum 'Extended'> cannot extend <enum 'ArticleStatus'>` |
