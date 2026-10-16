# 01 — Projekt a request cyklus — zdroje

## Oficiální dokumentace

- [Tutorial, část 1 — Requests and responses](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
  — oficiální úvod: projekt, app, první view a URL
- [Writing views](https://docs.djangoproject.com/en/6.1/topics/http/views/)
- [Request and response objects](https://docs.djangoproject.com/en/6.1/ref/request-response/)
  — `HttpRequest`, `HttpResponse`, `JsonResponse`
- [URL dispatcher](https://docs.djangoproject.com/en/6.1/topics/http/urls/)
  — jak Django hledá view podle URL
- [How Django processes a request](https://docs.djangoproject.com/en/6.1/topics/http/urls/#how-django-processes-a-request)
  — krátký popis request cyklu krok za krokem
- [Settings](https://docs.djangoproject.com/en/6.1/topics/settings/) —
  proč `from django.conf import settings`
- [`APPEND_SLASH`](https://docs.djangoproject.com/en/6.1/ref/settings/#append-slash)
- [Middleware](https://docs.djangoproject.com/en/6.1/topics/http/middleware/)
  — zatím jen pro představu, do hloubky v konceptu 11
- [CSRF protection](https://docs.djangoproject.com/en/6.1/ref/csrf/) —
  proč POST z `curl` vrací 403

## Nástroje

- [uv — Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Ruff — dokumentace](https://docs.astral.sh/ruff/)
