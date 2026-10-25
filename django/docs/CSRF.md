# CSRF — ochrana proti podvrženým requestům

Proč `POST` z Postmanu / `curl` končí `403 Forbidden — CSRF verification
failed`, co tím Django chrání a jak to řeší FE. Do hloubky se k tomu
roadmapa vrací v konceptech 10 (autentizace), 11 (middleware) a 14 (DRF
auth).

## Útok, před kterým to chrání

**CSRF = Cross-Site Request Forgery**, česky podvržení requestu z cizí
stránky.

1. Jsi přihlášený na `banka.cz`. Prohlížeč má uloženou session cookie.
2. Otevřeš `zla-stranka.cz`, která obsahuje třeba:

   ```html
   <form action="https://banka.cz/prevod/" method="POST">
     <input type="hidden" name="komu" value="utocnik">
     <input type="hidden" name="castka" value="10000">
   </form>
   <script>document.forms[0].submit()</script>
   ```

3. Prohlížeč pošle POST na `banka.cz` a **automaticky k němu přibalí
   cookies pro `banka.cz`**, tedy i tvou session. Banka vidí platně
   přihlášeného uživatele a převod provede.

Útočník tvou cookie nikdy neviděl. Jen zneužil to, že ji prohlížeč posílá
sám. Problém tedy vzniká jen tam, kde se **přihlášení drží v cookie**
(session auth). U tokenu v hlavičce `Authorization: Bearer …` k němu
nedojde, protože hlavičku cizí stránka přidat nedokáže.

### Komu cookie patří a kdy se posílá

Častá představa „cookie je vázaná na origin, takže request ze
`zla-stranka.cz` ji nedostane“ je jen napůl pravda:

| Co | Řídí se podle | Cizí stránka |
|---|---|---|
| **čtení** cookie (`document.cookie`) | domény stránky, která čte | ❌ cookie `banka.cz` nepřečte |
| **čtení odpovědi** z `banka.cz` | same-origin policy / CORS | ❌ nepřečte |
| **posílání** cookie s requestem | **cílové** domény requestu | ✅ prohlížeč cookie přibalí |

Prohlížeč se při requestu ptá „**kam** to letí?“, ne „**odkud** to
přišlo?“. Request na `banka.cz` dostane cookies `banka.cz`, ať ho
spustila záložka s bankou, odkaz v e-mailu, nebo formulář na cizí
stránce. Útočník tak request odeslat umí, jen nevidí odpověď. K tomu,
aby převod proběhl, ji ale vidět nepotřebuje.

**Otevřená záložka s bankou není potřeba.** Cookie leží v prohlížeči,
ne v záložce, a platí, dokud session nevyprší nebo se neodhlásíš
(u „zůstat přihlášen“ i týdny). Útočníkovi stačí, že má oběť platnou
session. Proto se odkaz rozesílá hromadně (e-mail, reklama, fórum)
a vyjde u těch, kdo zrovna přihlášení jsou.

### `SameSite` — novější ochrana v prohlížeči

Atribut cookie `SameSite` mění právě otázku „odkud to přišlo?“:

| Hodnota | Cookie se pošle u requestu spuštěného z cizí stránky |
|---|---|
| `Strict` | nikdy |
| `Lax` | jen při obyčejném prokliku odkazem (GET navigace), **ne** u POST formuláře, `fetch`, `<img>` |
| `None` | vždy (musí být zároveň `Secure`) |

Django posílá session cookie s `SameSite=Lax`
([`SESSION_COOKIE_SAMESITE`](https://docs.djangoproject.com/en/6.1/ref/settings/#session-cookie-samesite)),
takže podvržený POST formulář výše by v moderním prohlížeči session
cookie nedostal. Intuice „request z cizí stránky letí bez cookie“ tedy
dnes platí, ale díky `SameSite`, ne díky originu.

CSRF token je přesto potřeba dál:

- **Ne každý prohlížeč a ne každá cookie.** Cookie bez atributu
  `SameSite` prohlížeče zpracovávají různě, starší prohlížeče ho neznají.
- **„Site“ není „origin“.** `uzivatel.banka.cz` je pro `SameSite` stejný
  *site* jako `banka.cz`. Napadená subdoména nebo uživatelský obsah na
  subdoméně ochranu obejde.
- **`Lax` pouští GET.** Kdyby `GET /prevod/?komu=…` něco měnil,
  `SameSite` nepomůže, viz [Které metody se kontrolují](#které-metody-se-kontrolují).
- **Obrana do hloubky.** `SameSite` hlídá prohlížeč, token hlídá server.

## Jak Django brání

Django vyžaduje u „nebezpečných“ requestů **tajný token, který cizí
stránka nemůže znát**:

1. Server pošle klientovi cookie `csrftoken`.
2. Klient musí token z cookie poslat zpátky **ještě jednou jinou cestou**:
   - formulář: skryté pole `csrfmiddlewaretoken` (v šabloně
     `{% csrf_token %}`),
   - JS / API: hlavička `X-CSRFToken`.
3. `CsrfViewMiddleware` porovná obě hodnoty. Když chybí nebo nesedí,
   vrátí **403**.

Proč to funguje: `zla-stranka.cz` dokáže prohlížeč přimět, aby cookie
**poslal**, ale nedokáže ji **přečíst**. Same-origin policy jí nedovolí
číst cookies ani odpovědi z `banka.cz`, a proto do formuláře nebo hlavičky
nemá jakou hodnotu dát.

### Proč nestačí token jen v cookie

Cookie `csrftoken` prohlížeč přibalí i k requestu z cizí stránky, úplně
stejně jako session cookie. Kdyby Django kontrolovalo jen ji, útok by
prošel. Rozhoduje až **druhá kopie v requestu**, kterou musí vložit
stránka sama:

| | Vlastní FE na `banka.cz` | `zla-stranka.cz` |
|---|---|---|
| cookie `csrftoken` v requestu | ✅ prohlížeč přibalí | ✅ prohlížeč přibalí |
| přečíst cookie a dát token do hlavičky / pole formuláře | ✅ `document.cookie` vlastní domény | ❌ cookie cizí domény nepřečte |
| výsledek | projde | **403** |

Formulář útočníka z příkladu výše tedy cookie s tokenem odešle, ale pole
`csrfmiddlewaretoken` v něm není (nebo má vymyšlenou hodnotu), protože
útočník token nezná. Cookie „má“ jen naslepo: prohlížeč ji pošle za něj,
on ji ale nevidí, a nemůže ji proto zopakovat.

Mimochodem i cookie `csrftoken` má ve výchozím stavu `SameSite=Lax`
([`CSRF_COOKIE_SAMESITE`](https://docs.djangoproject.com/en/6.1/ref/settings/#csrf-cookie-samesite)),
takže ji moderní prohlížeč u cross-site POST obvykle nepošle vůbec.
Ochrana na tom ale nestojí, funguje i bez toho díky porovnání obou
kopií.

U HTTPS Django navíc kontroluje hlavičku `Origin` / `Referer`. Request
musí přicházet ze stejné domény, nebo z domény uvedené
v `CSRF_TRUSTED_ORIGINS`.

## Které metody se kontrolují

| Metody | CSRF kontrola | Proč |
|---|---|---|
| `GET`, `HEAD`, `OPTIONS`, `TRACE` | ne | „bezpečné“ metody: podle HTTP nemají nic měnit |
| `POST`, `PUT`, `PATCH`, `DELETE` | **ano** | mění data |

Z toho plyne pravidlo: **GET view nikdy nesmí měnit data** (mazat,
odesílat, převádět). CSRF ochrana by ho nekryla.

## Kde v request cyklu se to děje

`CsrfViewMiddleware` kontroluje až **po nalezení routy, těsně před
zavoláním view**. Potřebuje totiž vědět, které view se bude volat, protože
view může mít CSRF vypnuté (`@csrf_exempt`). Proto ve cvičení `01-prvni-projekt`:

| Request | Status | Kdo |
|---|---|---|
| `POST /api/health/` | 403 | routa existuje → CSRF kontrola → chybí token |
| `POST /api/health` | 500 | routa neexistuje → ke CSRF se nedojde → `CommonMiddleware` (`APPEND_SLASH`) nemůže POST přesměrovat |

V obou případech se tvoje view nezavolá.

## CSRF vs. CORS — nepléct si

Jako FE vývojář znáš hlavně CORS. Řeší něco jiného:

| | CORS | CSRF |
|---|---|---|
| Kdo vynucuje | **prohlížeč** | **server** (Django) |
| Co hlídá | jestli smí JS z cizí domény **číst odpověď** | jestli request **opravdu pochází z tvé aplikace** |
| Chyba | v konzoli prohlížeče, request se může i provést | 403 ze serveru |
| Postman / `curl` | neřeší (nejsou prohlížeč) | **řeší**, proto 403 |

CORS útoku CSRF nezabrání. Obyčejný `<form method="POST">` na cizí doménu
CORS vůbec nekontroluje.

## Jak to řeší FE (Vue + Django se session auth)

Cookie `csrftoken` není `HttpOnly`, takže ji JS přečíst může (jen JS
z vlastní domény). Token se pak posílá v hlavičce:

```ts
// axios — výchozí názvy má jiné (XSRF-TOKEN / X-XSRF-TOKEN), je potřeba je přenastavit
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true   // posílej cookies (session + csrftoken)
// FE na jiném originu (např. Vite na :5173): od axios 1.6 navíc
axios.defaults.withXSRFToken = true
```

```ts
// fetch — ručně
const csrfToken = document.cookie
  .split('; ')
  .find((c) => c.startsWith('csrftoken='))
  ?.split('=')[1]

await fetch('/api/orders/', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken ?? '' },
  body: JSON.stringify(order),
})
```

Aby cookie `csrftoken` vůbec existovala, musí ji server nejdřív poslat:
při vykreslení šablony s `{% csrf_token %}`, z view s dekorátorem
`@ensure_csrf_cookie`, nebo po zavolání `django.middleware.csrf.get_token(request)`.
SPA si ji typicky vyžádá jedním GET requestem při startu.

Když FE běží na jiném originu než Django (dev: `localhost:5173` vs.
`localhost:8000`), je potřeba ho v Djangu povolit:

```python
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]
```

## A co REST API (DRF)?

- **DRF views jsou ve výchozím stavu `csrf_exempt`.** CSRF si vynucuje až
  `SessionAuthentication`, a to jen u přihlášeného uživatele (protože
  jedině tam je přihlášení v cookie).
- U **tokenové / JWT** autentizace (`Authorization` hlavička) se CSRF
  neřeší. Útok popsaný výše na ni nefunguje.

Proto v pracovních projektech často POST přes DRF z Postmanu funguje,
zatímco na obyčejné Django view z tohohle konceptu ne.

## `@csrf_exempt` — kdy ano a kdy ne

```python
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook(request): ...
```

- ✅ **Webhooky** od třetích stran (platební brána, GitHub): volá je
  cizí server, který token mít nemůže. Ověřují se jinak, typicky podpisem.
- ✅ Krátce lokálně při učení, když chceš z Postmanu zkusit POST na
  obyčejné view. Pak zase odstranit.
- ❌ Jako „oprava“ 403 v aplikaci s přihlášením přes session. Tím ochranu
  vypneš.

## Testování v Postmanu (session auth)

1. Pošli GET na view, které nastaví cookie `csrftoken`. Postman si ji
   uloží (záložka *Cookies*).
2. U POST přidej hlavičku `X-CSRFToken` s hodnotou té cookie. Ručně, nebo
   v *Pre-request Script*:

   ```js
   pm.request.headers.upsert({
     key: 'X-CSRFToken',
     value: pm.cookies.get('csrftoken'),
   })
   ```

## Odkazy

- [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/6.1/ref/csrf/)
  — jak CSRF funguje v Djangu, včetně AJAX
- [How to use Django's CSRF protection](https://docs.djangoproject.com/en/6.1/howto/csrf/)
  — praktický návod (formuláře, JS, dekorátory)
- [`CSRF_TRUSTED_ORIGINS`](https://docs.djangoproject.com/en/6.1/ref/settings/#csrf-trusted-origins)
- [DRF — Authentication a CSRF](https://www.django-rest-framework.org/topics/ajax-csrf-cors/)
- [OWASP — CSRF](https://owasp.org/www-community/attacks/csrf)
- [MDN — `SameSite` cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie#samesitesamesite-value)
