# Práce s časem a časovými pásmy

Krátce: **v Django aplikaci nepoužívej `datetime.now()`**, ale funkce
z `django.utils.timezone`. Modul `datetime` samotný ale zakázaný není.
Typy `datetime`, `date` a `timedelta` používáš dál, jen aktuální čas
nebereš přes `datetime.now()`.

## Naive vs. aware

| | Naive | Aware |
|---|---|---|
| Co to je | čas **bez** informace o pásmu | čas **s** offsetem / pásmem (`tzinfo`) |
| Příklad v JSONu | `"2026-10-16T17:21:17"` | `"2026-10-16T17:21:17+02:00"` nebo `"2026-10-16T15:21:17Z"` |
| Jednoznačný? | ❌ nikdo neví, kterou 17:21 myslíš | ✅ přesný okamžik |
| Odkud | `datetime.now()` | `timezone.now()`, `timezone.localtime()` |

Proč na tom záleží pro FE: `new Date("2026-10-16T17:21:17")` vyloží prohlížeč
jako čas **ve svém** pásmu. Uživatel v Londýně dostane jiný okamžik než
uživatel v Praze, a nikdo si toho nevšimne. S offsetem (`+02:00` / `Z`)
dostanou všichni stejný okamžik.

## `USE_TZ` a `TIME_ZONE`

```python
USE_TZ = True                # výchozí od startproject
TIME_ZONE = "Europe/Prague"  # výchozí je "UTC"
```

- **`USE_TZ = True`** neznamená „použij `TIME_ZONE`“, ale **„pracuj
  s aware časy a interně všechno drž v UTC“**. Do DB se ukládá UTC.
- **`TIME_ZONE`** se použije, až když se čas převádí **pro člověka**:
  zobrazení v šablonách a adminu, čtení data z formuláře, nebo výslovné
  `localtime()`.

Obdoba v JS: `Date` je uvnitř taky okamžik v UTC a do místního pásma ho
převádí až `toLocaleString()`.

## Funkce, které používat

```python
from django.utils import timezone

timezone.now()          # aware, vždy v UTC         → 2026-10-16 15:21:17+00:00
timezone.localtime()    # aware, v TIME_ZONE        → 2026-10-16 17:21:17+02:00
timezone.localdate()    # dnešní datum v TIME_ZONE  → 2026-10-16
```

| Kdy | Co |
|---|---|
| ukládání, výpočty, porovnávání | `timezone.now()` (UTC) |
| zobrazení / API odpověď v místním čase | `timezone.localtime(dt)` (bez argumentu = teď) |
| „dnešní den“ (filtr dnešních objednávek, …) | `timezone.localdate()`, ne `date.today()` |
| naive čas z cizího zdroje udělat aware | `timezone.make_aware(dt)` (bere `TIME_ZONE`) |
| jiné pásmo než `TIME_ZONE` | `timezone.localtime(dt, ZoneInfo("America/New_York"))` |

```python
from datetime import timedelta
from zoneinfo import ZoneInfo   # standardní knihovna, databáze pásem

tomorrow = timezone.now() + timedelta(days=1)   # aritmetika s timedelta je v pořádku
```

`timezone.now()` při `USE_TZ = False` vrací naive místní čas, stejně jako
`datetime.now()`. Se zapnutým `USE_TZ` je to vždycky aware UTC.

## Čemu se vyhnout

| ❌ | Proč | ✅ |
|---|---|---|
| `datetime.now()` | naive, bez pásma | `timezone.now()` / `timezone.localtime()` |
| `datetime.utcnow()` | naive (i když UTC), od Pythonu 3.12 deprecated | `timezone.now()` |
| `date.today()` | systémové datum serveru, ne `TIME_ZONE` | `timezone.localdate()` |
| porovnání naive a aware | `TypeError: can't compare offset-naive and offset-aware datetimes` | obě strany aware |
| naive čas do `DateTimeField` | Django uloží, ale vypíše `RuntimeWarning: ... received a naive datetime while time zone support is active` | aware čas |
| ruční `+ timedelta(hours=2)` pro „místní čas“ | v zimě je offset +1, přechody letního času to rozbijí | `localtime()` přechody řeší samo |

## Čas v JSON odpovědi

```python
JsonResponse({"now": timezone.localtime()})
# → "2026-10-16T17:21:17.850+02:00"   (Djangův encoder zkrátí na milisekundy)

JsonResponse({"now": timezone.now()})
# → "2026-10-16T15:21:17.850Z"        (UTC zapíše jako "Z")

JsonResponse({"now": timezone.localtime().isoformat()})
# → "2026-10-16T17:21:17.850123+02:00" (formát řídíš sám)
```

Všechny tři zápisy jsou platné ISO 8601 a FE je přečte (`new Date(...)`).
Pro API se často vrací rovnou UTC (`Z`) a do místního času převádí až FE
podle uživatele. Místní čas ze serveru dává smysl, když záleží na pásmu
podniku (otevírací doba, uzávěrka objednávek).

## Odkazy

- [Time zones](https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/)
  — hlavní průvodce, včetně FAQ
- [`django.utils.timezone`](https://docs.djangoproject.com/en/6.1/ref/utils/#module-django.utils.timezone)
- [`USE_TZ`](https://docs.djangoproject.com/en/6.1/ref/settings/#use-tz)
  a [`TIME_ZONE`](https://docs.djangoproject.com/en/6.1/ref/settings/#time-zone)
- [`zoneinfo`](https://docs.python.org/3/library/zoneinfo.html) a
  [aware vs. naive](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)
  v dokumentaci Pythonu
