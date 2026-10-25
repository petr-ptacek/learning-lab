import math

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.urls import reverse
from django.utils.http import urlencode

from books.data import BOOKS


def _serialize_book(book):
    return {**book, "url": reverse("books:detail", kwargs={"book_id": book["id"]})}


def _parse_int_param(request: HttpRequest, name: str, default=None):
    value = request.GET.get(name)
    return int(value) if value else default


def get_books(request: HttpRequest):
    try:
        page = _parse_int_param(request, "page", default=1)
    except ValueError:
        return JsonResponse(
            {"error": "Parametr page musí být celé číslo"},
            status=400,
        )

    try:
        page_size = _parse_int_param(request, "page_size", default=2)
    except ValueError:
        return JsonResponse(
            {"error": "Parametr page_size musí být celé číslo"},
            status=400,
        )

    if page_size < 1 or page_size > 5:
        return JsonResponse({"error": "page_size musí být 1 až 5"}, status=400)

    total_pages = math.ceil(len(BOOKS) / page_size)

    if page < 1 or page > total_pages:
        return JsonResponse({"error": "Stránka neexistuje"}, status=404)

    results = [
        _serialize_book(book)
        for book in BOOKS[(page - 1) * page_size : page * page_size]
    ]

    next_url = (
        f"{reverse('bonus:get_books')}?{urlencode({'page': page + 1, 'page_size': page_size})}"
        if page + 1 <= total_pages
        else None
    )

    previous_url = (
        f"{reverse('bonus:get_books')}?{urlencode({'page': page - 1, 'page_size': page_size})}"
        if page - 1 != 0
        else None
    )

    return JsonResponse(
        {
            "count": len(BOOKS),
            "page": page,
            "num_pages": total_pages,
            "results": results,
            "next": next_url,
            "previous": previous_url,
        }
    )
