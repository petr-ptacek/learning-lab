# 02 — URLs a views — zdroje

## Oficiální dokumentace

- [URL dispatcher](https://docs.djangoproject.com/en/6.1/topics/http/urls/)
  — `path()`, pořadí rout, `include()`
- [Path converters](https://docs.djangoproject.com/en/6.1/topics/http/urls/#path-converters)
  — `int`, `str`, `slug`, `uuid`, `path` (a vlastní convertery)
- [Naming URL patterns](https://docs.djangoproject.com/en/6.1/topics/http/urls/#naming-url-patterns)
  a [URL namespaces](https://docs.djangoproject.com/en/6.1/topics/http/urls/#url-namespaces)
  — `name`, `app_name`
- [`reverse()`](https://docs.djangoproject.com/en/6.1/ref/urlresolvers/#reverse)
- [`HttpRequest`](https://docs.djangoproject.com/en/6.1/ref/request-response/#httprequest-objects)
  — `method`, `GET`, `headers`, `body`
- [`QueryDict`](https://docs.djangoproject.com/en/6.1/ref/request-response/#querydict-objects)
  — `get()`, `getlist()`
- [`JsonResponse`](https://docs.djangoproject.com/en/6.1/ref/request-response/#jsonresponse-objects)
  — včetně `json_dumps_params`
- [`json.dumps`](https://docs.python.org/3/library/json.html#json.dumps) —
  volby serializace (dokumentace Pythonu)

## Pro srovnání z FE

- [Vue Router — Named routes](https://router.vuejs.org/guide/essentials/named-routes.html)
- [Vue Router — Dynamic route matching](https://router.vuejs.org/guide/essentials/dynamic-matching.html)
  — `route.params`, obdoba path converterů
