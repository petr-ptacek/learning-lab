# Velikost písmen a porovnávání stringů

`lower()`, `upper()`, `casefold()` a příbuzné metody, a jak porovnávat
stringy bez ohledu na velikost písmen (případně i diakritiku). Výstupy
jsou ověřené na Pythonu 3.14.

Oficiální docs:
[String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods),
[`str.casefold`](https://docs.python.org/3/library/stdtypes.html#str.casefold),
[`unicodedata`](https://docs.python.org/3/library/unicodedata.html).

## Metody pro velikost písmen

Všechno jsou **metody stringu** (`text.lower()`, ne `lower(text)`). Vracejí
**nový** string a původní nemění, protože stringy jsou neměnné.

| Metoda | Co dělá | Příklad | JS obdoba |
|---|---|---|---|
| `lower()` | malá písmena | `"Karel ČAPEK".lower()` → `"karel čapek"` | `toLowerCase()` |
| `upper()` | velká písmena | `"čapek".upper()` → `"ČAPEK"` | `toUpperCase()` |
| `casefold()` | malá písmena **pro porovnávání** | `"Straße".casefold()` → `"strasse"` | nemá |
| `capitalize()` | první písmeno velké, zbytek malý | `"KAREL".capitalize()` → `"Karel"` | nemá |
| `title()` | první písmeno každého slova velké | `"karel čapek".title()` → `"Karel Čapek"` | nemá |
| `swapcase()` | prohodí velká a malá | `"Karel".swapcase()` → `"kAREL"` | nemá |
| `islower()` / `isupper()` | test, vrací `bool` | `"ČAPEK".isupper()` → `True` | nemá |

`title()` bere za začátek slova cokoliv po ne-písmenu:
`"o'neil".title()` → `"O'Neil"`. Na jména se proto moc nehodí.

## `casefold()` vs. `lower()`

`casefold()` je „agresivnější“ `lower()`. Kromě převodu na malá písmena
sjednotí i znaky, které se v některých jazycích píšou víc způsoby:

```python
"Karel ČAPEK".lower()      # 'karel čapek'
"Karel ČAPEK".casefold()   # 'karel čapek'   ← pro češtinu stejné

"Straße".lower()           # 'straße'
"Straße".casefold()        # 'strasse'       ← německé ß → ss
"ς".lower()                # 'ς'
"ς".casefold()             # 'σ'             ← řecká koncová sigma → běžná
"ﬁle".casefold()           # 'file'          ← ligatura ﬁ → dvě písmena
```

Proč na tom záleží:

```python
"Straße".lower() == "STRASSE".lower()        # False ('straße' vs 'strasse')
"Straße".casefold() == "STRASSE".casefold()  # True
```

| Účel | Metoda |
|---|---|
| **porovnávání, vyhledávání, klíče ve slovníku** bez ohledu na velikost | `casefold()` (doporučuje přímo dokumentace) |
| **zobrazení** uživateli, normalizace e-mailu apod. | `lower()` (`casefold()` může text změnit víc, než chceš) |

## Porovnávání bez ohledu na velikost písmen

Převádí se **obě strany**:

```python
"čap" in "Karel Čapek"                        # False ('č' vs 'Č')
"ČAP".casefold() in "Karel Čapek".casefold()  # True

"ČAPEK".casefold() == "čapek".casefold()      # True
```

`in` u stringů testuje, jestli je jeden podřetězcem druhého. Obdoba JS
`"Karel Čapek".includes("čap")`. `"" in text` je vždycky `True`: prázdný
řetězec je podřetězcem čehokoliv, takže prázdný filtr pustí všechno.

## Diakritika

Žádná z metod výše diakritiku **neodstraní**: `"Č".casefold()` je `"č"`,
ne `"c"`. Hledání `"capek"` tedy Čapka nenajde.

Bez diakritiky se dá porovnávat přes normalizaci Unicode. Znak `Č` se
rozloží na `C` + kombinační háček (`NFD`) a kombinační znaky se zahodí:

```python
import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


strip_accents("Karel Čapek")      # 'Karel Capek'
strip_accents("Božena Němcová")   # 'Bozena Nemcova'

strip_accents("capek").casefold() in strip_accents("Karel Čapek").casefold()   # True
```

V JS se totéž dělá přes `text.normalize('NFD').replace(/\p{M}/gu, '')`,
pro porovnání pak `Intl.Collator('cs', { sensitivity: 'base' })`.

V Django aplikaci se vyhledávání většinou nechává na databázi
(`__icontains`, viz koncept 04 v `django/ROADMAP.md`). Chování s
diakritikou tam pak závisí na databázi a její collation.

## Časté chyby

| Chyba | Příčina |
|---|---|
| `NameError: name 'lower' is not defined` | `lower(text)` místo `text.lower()`, je to metoda |
| hledání nic nenajde kvůli velikosti písmen | převedena jen jedna strana porovnání |
| `AttributeError: 'NoneType' object has no attribute 'lower'` | proměnná je `None` (např. chybějící query parametr), ne string |
| `text.lower()` „nic neudělá“ | výsledek se nikam neuložil, `text = text.lower()` |
| `"capek"` nenajde `"Čapek"` | diakritiku metody pro velikost písmen neřeší, viz `strip_accents` |
