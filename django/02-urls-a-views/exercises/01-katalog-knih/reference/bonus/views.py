import math

from django.urls import reverse
from django.utils.http import urlencode

from books.data import BOOKS
from books.views import ReadableJsonResponse, parse_int_param, serialize_book


def int_param(request, name, default):
    value = parse_int_param(request, name)
    return default if value is None else value


def page_url(page, page_size):
    query = urlencode({"page": page, "page_size": page_size})
    return f"{reverse('bonus:books')}?{query}"


def book_list(request):
    try:
        page = int_param(request, "page", default=1)
        page_size = int_param(request, "page_size", default=2)
    except ValueError:
        return ReadableJsonResponse(
            {"error": "page a page_size musí být celá čísla"}, status=400
        )
    if not 1 <= page_size <= 5:
        return ReadableJsonResponse({"error": "page_size musí být 1 až 5"}, status=400)

    num_pages = math.ceil(len(BOOKS) / page_size)
    if not 1 <= page <= num_pages:
        return ReadableJsonResponse({"error": "Stránka neexistuje"}, status=404)

    start = (page - 1) * page_size
    return ReadableJsonResponse(
        {
            "count": len(BOOKS),
            "page": page,
            "num_pages": num_pages,
            "next": page_url(page + 1, page_size) if page < num_pages else None,
            "previous": page_url(page - 1, page_size) if page > 1 else None,
            "results": [
                serialize_book(book) for book in BOOKS[start : start + page_size]
            ],
        }
    )
