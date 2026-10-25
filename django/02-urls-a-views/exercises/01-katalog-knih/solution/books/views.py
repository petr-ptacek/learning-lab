from django.http import HttpRequest, JsonResponse
from django.urls import reverse

from books.data import BOOKS


def _serialize_book(book):
    return {**book, "url": reverse("books:detail", kwargs={"book_id": book["id"]})}


def _parse_int_param(request: HttpRequest, name: str):
    value = request.GET.get(name)
    return int(value) if value else None


class UnicodeJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)


def _filter_books_by(author=None, year_from=None, year_to=None):
    result = []

    for book in BOOKS:
        pass_author_filter = bool(
            not isinstance(author, str)
            or (book["author"] and (author.casefold() in book["author"].casefold()))
        )

        pass_year_from_filter = bool(
            not isinstance(year_from, int) or book["year"] >= year_from
        )

        pass_year_to_filter = bool(
            not isinstance(year_to, int) or book["year"] <= year_to
        )

        if pass_author_filter and pass_year_from_filter and pass_year_to_filter:
            result.append(book)

    return result


def book_detail(request: HttpRequest, book_id: int):
    books = list(filter(lambda book: book["id"] == book_id, BOOKS))
    book = books[0] if books else None

    if not book:
        return UnicodeJsonResponse({"error": "Kniha nenalezena"}, status=404)

    book = _serialize_book(book)

    return UnicodeJsonResponse(book)


def book_list(request: HttpRequest):
    query_params = {
        "author": request.GET.get("author", ""),
    }

    for name in ("year_from", "year_to"):
        try:
            query_params[name] = _parse_int_param(request, name)
        except ValueError:
            return UnicodeJsonResponse(
                {"error": f"Parametr {name} musí být celé číslo"},
                status=400,
            )

    books = [_serialize_book(book) for book in _filter_books_by(**query_params)]
    return UnicodeJsonResponse({"count": len(books), "results": books})


def test(request: HttpRequest, some_id):
    print(type(some_id))
    return JsonResponse({"id": some_id})
