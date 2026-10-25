# Modul `json`

Převod mezi Python objekty a JSON textem: obdoba `JSON.stringify` /
`JSON.parse` z JS. Modul je ve standardní knihovně, stačí `import json`.
Výstupy jsou ověřené na Pythonu 3.14.

Oficiální docs: [`json`](https://docs.python.org/3/library/json.html).

## Čtyři hlavní funkce

| Funkce | Směr | Pracuje se | JS obdoba |
|---|---|---|---|
| `json.dumps(obj)` | Python → JSON | **stringem** (`dump s` = *dump string*) | `JSON.stringify(obj)` |
| `json.loads(text)` | JSON → Python | **stringem** (nebo `bytes`) | `JSON.parse(text)` |
| `json.dump(obj, f)` | Python → JSON | **souborem** | nemá (`fs.writeFile` + `stringify`) |
| `json.load(f)` | JSON → Python | **souborem** | nemá (`fs.readFile` + `parse`) |

```python
import json

book = {"title": "Krakatit", "year": 1924, "tags": ("sci-fi",), "available": True}

text = json.dumps(book)
# '{"title": "Krakatit", "year": 1924, "tags": ["sci-fi"], "available": true}'

json.loads(text)
# {'title': 'Krakatit', 'year': 1924, 'tags': ['sci-fi'], 'available': True}
```

`loads` přijme i `bytes` (UTF-8), proto v Djangu jde rovnou
`json.loads(request.body)`.

## Převod typů

| Python | → JSON | → zpět do Pythonu |
|---|---|---|
| `dict` | objekt `{}` | `dict` |
| `list`, `tuple` | pole `[]` | **vždy `list`** |
| `str` | string | `str` |
| `int` | číslo | `int` (libovolně velké, žádná ztráta přesnosti jako v JS) |
| `float` | číslo | `float` (`1.0` i `1e2` jsou `float`) |
| `True` / `False` | `true` / `false` | `True` / `False` |
| `None` | `null` | `None` |
| `set`, `date`, `datetime`, `Decimal`, vlastní třída | ❌ `TypeError` | viz [Nepodporované typy](#nepodporované-typy) |

Na co si dát pozor:

- **Klíče jsou v JSONu vždy stringy.** `json.dumps({1: "x"})` dá
  `'{"1": "x"}'` a zpět se vrátí `{'1': 'x'}`, ne `{1: 'x'}`.
- **`tuple` se vrátí jako `list`.**
- **`bool` je v Pythonu podtřída `int`.** Po `loads` je `isinstance(True,
  int)` pořád `True`. Když validuješ „celé číslo“, vyřaď `bool` zvlášť.
- **Duplicitní klíč** (`'{"a": 1, "a": 2}'`) chybu nevyhodí, vyhraje
  poslední hodnota: `{'a': 2}`.

## `dumps` — užitečné parametry

Stejné parametry má i `dump`.

| Parametr | Co dělá | Příklad výstupu |
|---|---|---|
| `ensure_ascii=False` | ne-ASCII znaky nechá jak jsou (výchozí `True` je escapuje) | `"Karel Čapek"` místo `"Karel Čapek"` |
| `indent=2` | odsazení, víc řádků (obdoba `JSON.stringify(obj, null, 2)`) | pro čtení a soubory |
| `sort_keys=True` | seřadí klíče | stabilní výstup pro diff a testy |
| `separators=(",", ":")` | bez mezer, nejkratší výstup | `{"a":1,"b":[1,2]}` |
| `default=funkce` | volá se pro objekty, které `json` neumí | viz níže |
| `allow_nan=False` | `nan` / `inf` vyhodí `ValueError` místo nevalidního `NaN` | výchozí `True` píše `NaN`, což není platný JSON |

```python
json.dumps({"author": "Karel Čapek"})
# '{"author": "Karel \\u010capek"}'   ← platný JSON, jen nečitelný
json.dumps({"author": "Karel Čapek"}, ensure_ascii=False)
# '{"author": "Karel Čapek"}'

print(json.dumps({"b": 1, "a": [1, 2]}, indent=2, sort_keys=True))
# {
#   "a": [
#     1,
#     2
#   ],
#   "b": 1
# }
```

Escapovaný výstup (`Č`) je **platný JSON** a každý parser z něj
dostane zpět `Č`. `ensure_ascii=False` je jen kvůli čitelnosti
a velikosti.

## Nepodporované typy

```python
import datetime

json.dumps({"date": datetime.date(2026, 10, 25)})
# TypeError: Object of type date is not JSON serializable
```

Parametr `default` dostane objekt, který `json` neumí, a vrátí něco, co
umí:

```python
def to_json(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


json.dumps({"date": datetime.date(2026, 10, 25), "tags": {3, 1}}, default=to_json)
# '{"date": "2026-10-25", "tags": [1, 3]}'
```

Rychlá varianta `default=str` převede cokoliv přes `str()`. Hodí se na
ladicí výpis, v API ale radši explicitně, ať se omylem nezačne
serializovat něco, co nechceš.

Obdoba `toJSON()` / replaceru v `JSON.stringify`. V Djangu za tebe
`date`, `datetime` a `Decimal` převádí `DjangoJSONEncoder`, který
používá `JsonResponse`.

## `loads` — chyby a co může vrátit

Nevalidní vstup vyhodí `json.JSONDecodeError`. Je to podtřída
`ValueError`, takže ji chytí i `except ValueError`.

```python
try:
    data = json.loads(text)
except json.JSONDecodeError as error:
    print(error.msg, error.lineno, error.colno)
```

| Vstup | Výsledek |
|---|---|
| `''` (prázdný) | `JSONDecodeError: Expecting value` |
| `'{"a": 1,}'` | `JSONDecodeError: Illegal trailing comma before end of object` |
| `"{'a': 1}"` | `JSONDecodeError: Expecting property name enclosed in double quotes` (apostrofy JSON nezná) |
| `'[1, 2]'` | `[1, 2]` → `list` |
| `'42'` | `42` → `int` |
| `'"x"'` | `'x'` → `str` |
| `'null'` | `None` |
| `' {"a": 1} '` | `{'a': 1}` (mezery okolo nevadí) |

**Validní JSON nemusí být objekt.** Když čekáš `dict`, ověř to
(`isinstance(data, dict)`), jinak na `data.get(...)` dostaneš
`AttributeError`.

Parametr `parse_float=decimal.Decimal` načte desetinná čísla přesně
(`1.10` → `Decimal('1.10')`), hodí se pro peníze.

## Soubory

```python
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

with open("books.json", encoding="utf-8") as f:
    books = json.load(f)
```

`encoding="utf-8"` uváděj vždy. Výchozí kódování závisí na systému
a s `ensure_ascii=False` by na Windows mohla diakritika skončit
rozbitá. Práce se soubory a `with` je v konceptu `10-soubory`.

## Z příkazové řádky

Formátování a kontrola JSONu bez psaní kódu (obdoba `jq .`):

```bash
echo '{"b": 1, "a": "Č"}' | python -m json --sort-keys --no-ensure-ascii --indent 2
# {
#   "a": "Č",
#   "b": 1
# }

python -m json data.json      # zformátuje soubor, u chyby vypíše řádek a sloupec
```

`python -m json` je novinka 3.14. Ve starších verzích stejně funguje
`python -m json.tool`.

## Časté chyby

| Chyba | Příčina |
|---|---|
| `TypeError: Object of type date is not JSON serializable` | `dumps` neumí `date` / `set` / `Decimal` / vlastní třídu, použij `default` |
| `TypeError: the JSON object must be str, bytes or bytearray, not dict` | `loads` na něco, co už je Python objekt |
| `AttributeError: 'str' object has no attribute 'read'` | `load(text)` místo `loads(text)`, `load` chce soubor |
| `JSONDecodeError: Expecting property name enclosed in double quotes` | apostrofy, nebo `str(dict)` místo `json.dumps(dict)` |
| `JSONDecodeError: Expecting value: line 1 column 1` | prázdný vstup, nebo HTML místo JSONu (např. chybová stránka) |
| po načtení `data[1]` hází `KeyError` | klíče jsou po JSONu stringy, správně `data["1"]` |
| `"Karel Čapek"` ve výstupu | výchozí `ensure_ascii=True` |
