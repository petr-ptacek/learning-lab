import json
from http import HTTPStatus

from django.http import HttpRequest, JsonResponse
from django.urls import reverse

from books.data.books import BOOKS


class ReadableJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault("json_dumps_params", {"ensure_ascii": False})
        super().__init__(data, **kwargs)


def find_book(book_id: int):
    book, book_index = next(
        iter(
            [(book, index) for index, book in enumerate(BOOKS) if book["id"] == book_id]
        ),
        (None, None),
    )

    return book, book_index


def serialize_book(book, request: HttpRequest | None = None):
    url = reverse("books:book_detail", kwargs={"book_id": book["id"]})

    if request:
        url = request.build_absolute_uri(url)

    return {**book, "url": url}


def load_data_from_request(request: HttpRequest):
    data = None
    error_response = None

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return data, ReadableJsonResponse(
            {"error": "Telo requestu neni platni JSON"}, status=HTTPStatus.BAD_REQUEST
        )

    if not isinstance(data, dict):
        return data, ReadableJsonResponse(
            {"error": "Telo requestu neni JSON object"}, status=HTTPStatus.BAD_REQUEST
        )

    return data, error_response
