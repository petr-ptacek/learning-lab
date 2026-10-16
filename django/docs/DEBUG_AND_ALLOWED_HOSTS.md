# `DEBUG` a `ALLOWED_HOSTS`

Dvě nastavení ze `settings.py`, která spolu souvisí a v produkci jsou
kritická pro bezpečnost. Po `startproject` máš:

```python
DEBUG = True
ALLOWED_HOSTS = []
```

Pro vývoj je to v pořádku, pro produkci ani jedno.

## `DEBUG`

`DEBUG = True` zapne podrobné chybové stránky, užitečné při vývoji:

| Chyba | Co debug stránka ukáže |
|---|---|
| **404** | **seznam všech URL patternů**, které Django zkoušelo |
| **500** | celý **traceback** s lokálními proměnnými, data requestu a **tabulku settings** |

S `DEBUG = False` dostane klient jen obecnou stránku *Not Found* /
*Server Error* bez detailů.

### Proč nikdy `DEBUG = True` v produkci

Debug stránky prozradí útočníkovi:

- **URL patterny**: skryté a interní endpointy (admin, interní API, …),
  o kterých by jinak nevěděl.
- **Settings**: Django sice samo skryje hodnoty s citlivě znějícím
  názvem (`SECRET_KEY`, `*PASSWORD*`, `*TOKEN*`, `*KEY*`, `*API*` …)
  hvězdičkami, ale vidět zůstane adresa a jméno databáze, cesty na
  serveru i vlastní nastavení s nevinným názvem (`PAYMENT_URL`).
- **Verze** Pythonu a Djanga, podle kterých se hledají známé zranitelnosti.
- **Lokální proměnné** v tracebacku, včetně dat z requestu.

`DEBUG = True` v produkci je jedna z nejčastějších a nejnebezpečnějších
chyb v Django nasazení. V praxi se hodnota bere z proměnné prostředí,
ne natvrdo ze souboru.

## `ALLOWED_HOSTS`

**Seznam domén, pod kterými je tvůj server dostupný.** Neříká, *kdo*
smí volat, ale *jak se server smí jmenovat*.

```python
ALLOWED_HOSTS = ["moje-aplikace.cz", "www.moje-aplikace.cz"]
# ".moje-aplikace.cz" (tečka na začátku) = doména i všechny subdomény
```

Django u každého requestu porovná hlavičku **`Host`** se seznamem. Když
v něm není, vrátí **400 Bad Request** (`DisallowedHost`). Hlavička `Host`
říká, **na jakou doménu klient volá** (cíl requestu), ne odkud request
přichází. Prohlížeč na `https://moje-aplikace.cz/…` do ní dá
`moje-aplikace.cz`.

### Proč je to potřeba: podvržený `Host`

Hlavičku `Host` vyplňuje klient, takže ji útočník může přepsat na
cokoliv (v Postmanu záložka *Headers*). Django ji přitom používá ke
skládání absolutních URL, například v e-mailu pro reset hesla:

1. Útočník zadá do formuláře „zapomenuté heslo“ **tvůj** e-mail a pošle
   request s `Host: zla-stranka.cz`.
2. Django vygeneruje odkaz
   `https://zla-stranka.cz/reset-hesla/<tvůj-tajný-token>/` a pošle ho
   **tobě**.
3. E-mail je pravý, přišel od skutečné aplikace, takže na odkaz klikneš.
4. Tvůj tajný token skončí na serveru útočníka, který si s ním nastaví
   tvoje heslo.

S `ALLOWED_HOSTS = ["moje-aplikace.cz"]` útok skončí hned v kroku 1:
request s cizím `Host` dostane 400 a e-mail se vůbec nepošle.

### Proč to nevadí při `DEBUG = True`

S prázdným `ALLOWED_HOSTS` a `DEBUG = True` Django automaticky povolí jen
lokální adresy `localhost` (včetně subdomén), `127.0.0.1` a `[::1]`.
Na vývojovém stroji tě nezdržuje. Jakmile přepneš `DEBUG = False`,
Django odmítne nastartovat, dokud seznam nevyplníš:

```
CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.
```

## Nesplést si s podobnými nastaveními

| Nastavení | Otázka, kterou řeší | Hlavička |
|---|---|---|
| `ALLOWED_HOSTS` | Pod jakými doménami **můj server** odpovídá? | `Host` |
| `CSRF_TRUSTED_ORIGINS` | Ze kterých **cizích originů** smí přijít POST s cookies? (viz [`CSRF.md`](CSRF.md)) | `Origin` |
| CORS (balíček `django-cors-headers`) | Kterým **cizím originům** prohlížeč dovolí číst odpovědi? | `Origin` → `Access-Control-Allow-Origin` |

„Povolené originy, ze kterých můžou chodit požadavky“ je
`CSRF_TRUSTED_ORIGINS` / CORS, **ne** `ALLOWED_HOSTS`.

## Odkazy

- [`DEBUG`](https://docs.djangoproject.com/en/6.1/ref/settings/#debug)
- [`ALLOWED_HOSTS`](https://docs.djangoproject.com/en/6.1/ref/settings/#allowed-hosts)
- [Host header validation](https://docs.djangoproject.com/en/6.1/topics/security/#host-header-validation)
- [Deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)
  — co dalšího zkontrolovat před nasazením (`uv run manage.py check --deploy`)
- [Filtering error reports](https://docs.djangoproject.com/en/6.1/howto/error-reporting/#filtering-error-reports)
  — které settings Django na debug stránce skrývá
