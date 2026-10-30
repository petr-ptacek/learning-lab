# 04 — Pipeline nad logem

Několik malých generátorů za sebou: každý bere iterable a vydává další.
Data jimi protékají po jednom řádku, bez mezilistů.

## Požadavky

- V kódu měj log (`"""\` na začátku zabrání prázdnému prvnímu řádku):

  ```python
  LOG = """\
  2026-10-01 08:00:01 INFO server started
  2026-10-01 08:05:12 WARN disk usage 85%

  2026-10-01 08:07:44 ERROR db timeout
  # ručně přidaná poznámka
  2026-10-01 09:12:03 INFO user anna logged in
  2026-10-01 09:15:30 ERROR payment failed

  2026-10-01 10:00:00 INFO backup done
  2026-10-01 10:30:00 ERROR backup verification failed
  """
  ```

- Napiš tyto funkce. Každá kromě `count_by_level` vrací **generátor**
  (`yield` nebo generátorový výraz), žádná nevytváří seznam:
  - `lines(text)` — vydá řádky bez okrajových mezer, vynechá prázdné
    a komentáře (začínají `#`). Nápověda: `text.splitlines()`.
  - `parse(lines)` — z každého řádku vydá tuple `(čas, úroveň, zpráva)`.
    Datum zahoď. Zpráva obsahuje mezery, takže pozor na `split`:
    podívej se na parametr `maxsplit`.
  - `with_level(records, level)` — jen záznamy dané úrovně.
  - `messages(records)` — jen zprávy.
  - `count_by_level(records)` — dict `úroveň → počet`. Tady už výsledek
    seznam/dict být musí.
- Funkce skládej do sebe: výstup jedné je vstup druhé.
- **Předpověď:** přidej do `lines` těsně před `yield` výpis
  `print("čtu:", line)` a zavolej:

  ```python
  next(with_level(parse(lines(LOG)), "ERROR"))
  ```

  Kolikrát se vypíše `čtu:`? Proč ne pro všech 7 řádků s daty?
  Pak výpis zase smaž.

### Příklady vstup/výstup

| Volání                                                         | Výsledek                                                         |
|----------------------------------------------------------------|------------------------------------------------------------------|
| `list(messages(with_level(parse(lines(LOG)), "ERROR")))`       | `['db timeout', 'payment failed', 'backup verification failed']` |
| `list(messages(with_level(parse(lines(LOG)), "DEBUG")))`       | `[]`                                                             |
| `next(parse(lines(LOG)))`                                      | `('08:00:01', 'INFO', 'server started')`                         |
| `len(list(lines(LOG)))`                                        | `7`                                                              |
| `list(lines(""))`                                              | `[]`                                                             |
| `list(lines("# jen komentář\n\n"))`                            | `[]`                                                             |
| `count_by_level(parse(lines(LOG)))`                            | `{'INFO': 3, 'WARN': 1, 'ERROR': 3}`                             |
| `count_by_level(parse(lines("")))`                             | `{}`                                                             |

## Bonus

- `errors_per_hour(records)` — dict `hodina → počet ERROR záznamů`
  (hodina jako string `"08"`).
- `count(iterable)` — počet prvků **bez** `len` a bez vytvoření seznamu.
  Jedním řádkem přes `sum`. Proč je `len(list(...))` u generátoru nad
  obřím souborem horší?

### Příklady vstup/výstup (bonus)

| Volání                                                 | Výsledek                            |
|--------------------------------------------------------|-------------------------------------|
| `errors_per_hour(parse(lines(LOG)))`                   | `{'08': 1, '09': 1, '10': 1}`       |
| `errors_per_hour([])`                                  | `{}`                                |
| `count(lines(LOG))`                                    | `7`                                 |
| `count(x for x in range(10) if x % 3 == 0)`            | `4`                                 |
| `count([])`                                            | `0`                                 |
