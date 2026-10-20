# django — Roadmap

Plán konceptů v doporučeném pořadí. Zaškrtnuto = koncept zvládnutý (teorie
prostudovaná + cvičení vyřešená), ne jen založený.

## Část 1 — Jak Django funguje (jádro)

- [x] 01-projekt-a-request-cyklus — projekt vs. app, `manage.py`,
  `settings.py`, cesta requestu: URL → view → `HttpResponse` /
  `JsonResponse`
- [ ] 02-urls-a-views — `path()`, path convertery, `include()`, pojmenované
  routy a `reverse()`, objekt `request` (metoda, query parametry, body)
- [ ] 03-modely-a-migrace — `models.Model`, typy polí, `makemigrations` /
  `migrate`, co je v migraci, CRUD v `manage.py shell`
- [ ] 04-querysety — `filter`/`exclude`/`get`, lookupy (`__icontains`,
  `__gte`), `Q` a `F`, řazení, lazy vyhodnocení, `aggregate`/`annotate`
  (staví na 03)
- [ ] 05-vztahy-mezi-modely — `ForeignKey`, `ManyToManyField`,
  `OneToOneField`, `related_name`, N+1 problém, `select_related` /
  `prefetch_related` (staví na 04)
- [ ] 06-admin — registrace modelů, `ModelAdmin` (`list_display`,
  `list_filter`, `search_fields`, inlines)

## Část 2 — Klasický Django web

- [ ] 07-sablony — šablony, kontext, dědičnost (`extends`/`block`), tagy a
  filtry (kratší koncept — hlavně pro čtení existujícího kódu)
- [ ] 08-formulare-a-validace — `Form`, `ModelForm`, `clean_*`, chybové
  hlášky (základ, na kterém pak stojí DRF serializery)
- [ ] 09-class-based-views — `View`, generické `ListView`/`DetailView`/
  `CreateView`, mixiny, kdy FBV a kdy CBV
- [ ] 10-autentizace-a-opravneni — `User`, sessions, login/logout,
  `login_required`, permissions a skupiny
- [ ] 11-middleware — životní cyklus requestu přes `MIDDLEWARE`, vlastní
  middleware (staví na 01)

## Část 3 — REST API (Django REST Framework)

- [ ] 12-drf-serializery — `Serializer`, `ModelSerializer`, validace,
  vnořené serializery (staví na 05 a 08)
- [ ] 13-drf-views-a-viewsety — `APIView`, generic views, `ViewSet`,
  routery (staví na 09)
- [ ] 14-drf-auth-a-permissions — autentizace (session/token), permission
  třídy, vlastní permission
- [ ] 15-drf-filtrovani-a-strankovani — filtrování, řazení, vyhledávání,
  pagination

## Část 4 — Kvalita a pokročilé

- [ ] 16-testovani — `TestCase`, test `Client`, `APITestCase`, fixtures /
  factory data
- [ ] 17-transakce-signaly-a-commands — `transaction.atomic`, signály (a
  proč s nimi šetřit), vlastní `manage.py` příkazy
