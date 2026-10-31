# 02 — Atributy třídy vs. atributy instance

Nejdůležitější cvičení konceptu pro Django: pole modelu
(`title = models.CharField(...)`) jsou atributy **třídy**, hodnoty
konkrétního záznamu atributy **instance**. Tady si vyzkoušíš, kde
Python atribut hledá a kam ho zapíše.

Teorie: [`THEORY.md`](../../THEORY.md#atributy-instance-vs-atributy-třídy),
do hloubky
[`docs/CLASSES_AND_INSTANCES.md`](../../../docs/CLASSES_AND_INSTANCES.md#3-jak-python-hledá-atribut).

## Požadavky

- **Předpověď:** ke každému `print` si napiš do komentáře, co vypíše.
  Pak spusť a u každého rozdílu vysvětli proč:

  ```python
  class Settings:
      language = "cs"
      tags = []


  s1 = Settings()
  s2 = Settings()
  s1.language = "en"
  s1.tags.append("beta")
  print(s1.language, s2.language, Settings.language)
  print(s2.tags)
  print(vars(s1), vars(s2))

  Settings.language = "de"
  print(s1.language, s2.language)

  del s1.language
  print(s1.language)
  ```

- Napiš třídu `Ticket` (tiket v helpdesku):
  - atribut třídy `next_id = 1` a atribut třídy `priority = "normal"`,
  - `__init__(self, title, priority=None)`: přidělí tiketu `id` z
    `next_id` a počítadlo na **třídě** zvýší o 1. Uloží `title`.
    `priority` uloží do instance **jen**, když je zadaná. Jinak ji
    instance nemá a čte se z třídy.
- Oprav třídu `Cart`. Teď sdílí košík mezi všemi zákazníky:

  ```python
  class Cart:
      items = []

      def add(self, item):
          self.items.append(item)
  ```

  Přidej metodu `count()`, která vrátí počet položek.

### Příklady vstup/výstup

Postupně za sebou (ID závisí na pořadí vytvoření):

| Kód                                               | Výsledek                                              |
|---------------------------------------------------|-------------------------------------------------------|
| `t1 = Ticket("Nejde přihlášení")`, `t1.id`        | `1`                                                   |
| `t2 = Ticket("Pomalý web", "high")`, `t2.id`      | `2`                                                   |
| `t3 = Ticket("Překlep v patičce")`, `t3.id`       | `3`                                                   |
| `Ticket.next_id`                                  | `4`                                                   |
| `t1.priority, t2.priority`                        | `('normal', 'high')`                                  |
| `vars(t1)`                                        | `{'id': 1, 'title': 'Nejde přihlášení'}`              |
| `vars(t2)`                                        | `{'id': 2, 'title': 'Pomalý web', 'priority': 'high'}`|
| `Ticket.priority = "low"`, pak `t1.priority, t2.priority` | `('low', 'high')`                             |

| Kód                                                     | Výsledek                         |
|---------------------------------------------------------|----------------------------------|
| `c1, c2 = Cart(), Cart()`, `c1.add("mléko")`, `c2.items` | `[]` (po opravě)                |
| `c1.add("chléb")`, `c1.items, c1.count(), c2.count()`   | `(['mléko', 'chléb'], 2, 0)`     |

## Bonus

Práce s atributy, jejichž jméno je ve **stringu**, přes `getattr`
a `setattr` (Django to dělá pořád, např. `getattr(settings, "X",
default)`):

- `describe(obj, fields)` — funkce (ne metoda), vrátí dict
  `jméno → hodnota` pro zadaná jména atributů. Chybějící atribut →
  `None`. Jedním comprehensionem.
- `update(obj, **changes)` — nastaví objektu všechny zadané atributy.

### Příklady vstup/výstup (bonus)

S tikety z tabulky výše (před změnou `Ticket.priority`):

| Kód                                               | Výsledek                                                         |
|---------------------------------------------------|------------------------------------------------------------------|
| `describe(t2, ["id", "title", "priority"])`       | `{'id': 2, 'title': 'Pomalý web', 'priority': 'high'}`           |
| `describe(t1, ["id", "priority", "author"])`      | `{'id': 1, 'priority': 'normal', 'author': None}`                |
| `describe(t1, [])`                                | `{}`                                                             |
| `update(t1, title="Opraveno", status="done")`, `vars(t1)` | `{'id': 1, 'title': 'Opraveno', 'status': 'done'}`       |
