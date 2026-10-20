from django.http import JsonResponse
from django.urls import reverse

from .data import BOOKS


class ReadableJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)


def serialize_book(book):
    return {**book, "url": reverse("books:detail", args=[book["id"]])}


def parse_int_param(request, name):
    value = request.GET.get(name)
    return int(value) if value else None


def book_list(request):
    author = request.GET.get("author", "").casefold()
    filters = {}
    for name in ("year_from", "year_to"):
        try:
            filters[name] = parse_int_param(request, name)
        except ValueError:
            return ReadableJsonResponse(
                {"error": f"Parametr {name} musí být celé číslo"}, status=400
            )
    year_from, year_to = filters["year_from"], filters["year_to"]

    books = [
        serialize_book(book)
        for book in BOOKS
        if author in book["author"].casefold()
        and (year_from is None or book["year"] >= year_from)
        and (year_to is None or book["year"] <= year_to)
    ]
    return ReadableJsonResponse({"count": len(books), "results": books})


def book_detail(request, book_id):
    book = next((book for book in BOOKS if book["id"] == book_id), None)
    if book is None:
        return ReadableJsonResponse({"error": "Kniha nenalezena"}, status=404)
    return ReadableJsonResponse(serialize_book(book))
