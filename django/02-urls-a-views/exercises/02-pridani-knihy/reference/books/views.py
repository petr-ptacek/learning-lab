import json
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .data import BOOKS

REQUIRED = "Povinné pole"


class ReadableJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)


def serialize_book(book):
    return {**book, "url": reverse("books:detail", args=[book["id"]])}


def find_book(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)


def validate_text(value):
    if not isinstance(value, str) or not value.strip():
        return "Musí být neprázdný text"
    return None


def validate_year(value):
    if isinstance(value, bool) or not isinstance(value, int):
        return "Musí být celé číslo"
    if value > date.today().year:
        return "Rok nesmí být v budoucnosti"
    return None


VALIDATORS = {"title": validate_text, "author": validate_text, "year": validate_year}


def validate_book(data, partial=False):
    """Collect errors for all fields; with partial=True missing fields are fine."""
    errors = {}
    for field, validate in VALIDATORS.items():
        if field in data:
            error = validate(data[field])
        else:
            error = None if partial else REQUIRED
        if error:
            errors[field] = error
    return errors


def clean_book_fields(data):
    """Return only the known fields present in data, texts stripped."""
    fields = {field: data[field] for field in VALIDATORS if field in data}
    for field in ("title", "author"):
        if field in fields:
            fields[field] = fields[field].strip()
    return fields


def parse_json_object(request):
    """Return (data, None), or (None, error response) for an invalid body."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        error = "Tělo requestu není platný JSON"
    else:
        if isinstance(data, dict):
            return data, None
        error = "Tělo requestu musí být JSON objekt"
    return None, ReadableJsonResponse({"error": error}, status=400)


def create_book(request):
    data, error_response = parse_json_object(request)
    if error_response:
        return error_response
    errors = validate_book(data)
    if errors:
        return ReadableJsonResponse({"errors": errors}, status=400)

    book = {"id": max((book["id"] for book in BOOKS), default=0) + 1}
    book.update(clean_book_fields(data))
    BOOKS.append(book)

    body = serialize_book(book)
    response = ReadableJsonResponse(body, status=201)
    response["Location"] = body["url"]
    return response


# csrf_exempt: učební API bez přihlášení, ať jde POST/DELETE poslat z Postmanu.
# V aplikaci se session přihlášením by tu být nesměl, viz docs/CSRF.md.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def book_list(request):
    if request.method == "POST":
        return create_book(request)
    books = [serialize_book(book) for book in BOOKS]
    return ReadableJsonResponse({"count": len(books), "results": books})


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def book_detail(request, book_id):
    book = find_book(book_id)
    if book is None:
        return ReadableJsonResponse({"error": "Kniha nenalezena"}, status=404)
    if request.method == "DELETE":
        BOOKS.remove(book)
        return HttpResponse(status=204)
    return ReadableJsonResponse(serialize_book(book))
