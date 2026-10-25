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
- [`json.loads`](https://docs.python.org/3/library/json.html#json.loads)
  a [převodní tabulka JSON → Python](https://docs.python.org/3/library/json.html#json-to-py-table)
- [View decorators](https://docs.djangoproject.com/en/6.1/topics/http/decorators/)
  — `require_http_methods`, `require_GET`, `require_POST`
- [`csrf_exempt`](https://docs.djangoproject.com/en/6.1/ref/csrf/#django.views.decorators.csrf.csrf_exempt)
- [Setting header fields](https://docs.djangoproject.com/en/6.1/ref/request-response/#setting-header-fields)
  — `response["Location"] = ...`

## HTTP

- [MDN — HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
  — 201, 204, 400, 404, 405
- [MDN — `Location`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Location)
  a [`Allow`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Allow)

## Pro srovnání z FE

- [Vue Router — Named routes](https://router.vuejs.org/guide/essentials/named-routes.html)
- [Vue Router — Dynamic route matching](https://router.vuejs.org/guide/essentials/dynamic-matching.html)
  — `route.params`, obdoba path converterů
