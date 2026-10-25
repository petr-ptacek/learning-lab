import json
from datetime import datetime
from http import HTTPStatus

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from books.data.books import BOOKS


def _serialize_book(book, request: HttpRequest | None = None):
    url = reverse("books:book_detail", kwargs={"book_id": book["id"]})

    if request:
        url = request.build_absolute_uri(url)

    return {**book, "url": url}


def _validate_year(data):
    if "year" not in data:
        return "Povinne pole"

    value = data["year"]

    if isinstance(value, bool) or not isinstance(value, int):
        return "Musí být celé číslo"

    if value > datetime.now().year:
        return "Rok nesmí být v budoucnosti"

    return None


def _validate_author(data):
    if "author" not in data:
        return "Povinne pole"

    value = data["author"]

    if not isinstance(value, str) or len(value.strip()) == 0:
        return "Musi byt neprazdny text"

    return None


def _validate_title(data):
    if "title" not in data:
        return "Povinne pole"

    value = data["title"]

    if not isinstance(value, str) or len(value.strip()) == 0:
        return "Musi byt neprazdny text"

    return None


def _validate_data(data):
    error_fields = {
        field: error_message
        for field, error_message in [
            ("author", _validate_author(data)),
            ("title", _validate_title(data)),
            ("year", _validate_year(data)),
        ]
        if error_message
    }

    return error_fields


class ReadableJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        results = list(map(lambda book: _serialize_book(book, request=request), BOOKS))
        return ReadableJsonResponse(
            {"count": len(results), "results": results}, status=HTTPStatus.OK
        )

    # POST

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return ReadableJsonResponse(
            {"error": "Telo requestu neni platni JSON"}, status=HTTPStatus.BAD_REQUEST
        )

    if not isinstance(data, dict):
        return ReadableJsonResponse(
            {"error": "Telo requestu neni JSON object"}, status=HTTPStatus.BAD_REQUEST
        )

    error_fields = _validate_data(data)

    if error_fields:
        return ReadableJsonResponse(
            {
                "errors": error_fields,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    book_raw = {
        "id": max(map(lambda book: book["id"], BOOKS), default=0) + 1,
        "title": data["title"].strip(),
        "year": data["year"],
        "author": data["author"].strip(),
    }

    BOOKS.append(book_raw)

    book = _serialize_book(
        book_raw,
        request=request,
    )

    response = ReadableJsonResponse(book, status=HTTPStatus.CREATED)
    response.headers["Location"] = book.get("url")

    return response


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def book_detail(request, book_id: int):
    book, book_index = next(
        iter(
            [(book, index) for index, book in enumerate(BOOKS) if book["id"] == book_id]
        ),
        (None, None),
    )

    if book is None:
        return ReadableJsonResponse(
            {"error": "Kniha nenalezena"}, status=HTTPStatus.NOT_FOUND
        )

    # GET
    if request.method == "GET":
        return ReadableJsonResponse(
            _serialize_book(book, request=request), status=HTTPStatus.OK
        )

    BOOKS.pop(book_index)

    return HttpResponse(status=HTTPStatus.NO_CONTENT)
